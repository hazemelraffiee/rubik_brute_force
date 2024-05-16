import copy
import numpy as np
from functools import cached_property
import tkinter as tk
import string

def generate_anticlockwise(clockwise):
    anticlockwise = [0] * 54
    for i in range(54):
        anticlockwise[clockwise[i]] = i
    return tuple(anticlockwise)

# Mapping from color to digit
CUSTOM_BASE_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase + "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"
BASE = len(CUSTOM_BASE_CHARS)

COLOR_TO_DIGIT = {'Y': 0, 'R': 1, 'G': 2, 'O': 3, 'B': 4, 'W': 5}
DIGIT_TO_COLOR = {v: k for k, v in COLOR_TO_DIGIT.items()}

CENTER_INDICES = [4, 13, 22, 31, 40, 49]
CENTER_COLORS = ['Y', 'R', 'G', 'O', 'B', 'W']

def encode_state(state):
    # Remove the center stickers
    state_without_centers = [state[i] for i in range(54) if i not in CENTER_INDICES]
    
    # Encode the state as a base-6 integer
    encoded = 0
    for char in state_without_centers:
        encoded = encoded * 6 + COLOR_TO_DIGIT[char]
    
    # Convert the base-6 integer to a custom base string
    result = []
    while encoded > 0:
        result.append(CUSTOM_BASE_CHARS[encoded % BASE])
        encoded //= BASE
    return ''.join(result[::-1]) or '0'

def decode_state(encoded_state):
    # Convert the custom base string back to a base-6 integer
    decoded = 0
    for char in encoded_state:
        decoded = decoded * BASE + CUSTOM_BASE_CHARS.index(char)
    
    # Convert the base-6 integer back to the original state string without centers
    state_without_centers = []
    for _ in range(48):
        state_without_centers.append(DIGIT_TO_COLOR[decoded % 6])
        decoded //= 6
    
    # Insert the center stickers back
    state = []
    center_idx = 0
    for i in range(54):
        if i in CENTER_INDICES:
            state.append(CENTER_COLORS[center_idx])
            center_idx += 1
        else:
            state.append(state_without_centers.pop(0))
    return ''.join(state)


class RubiksCube:

    root = None
    next_canvas_y = 0  # Keep track of where the next canvas should start in y
    sc = 50  # scale for each sticker

    SOLVED = np.array('Y,Y,Y,Y,Y,Y,Y,Y,Y,R,R,R,R,R,R,R,R,R,G,G,G,G,G,G,G,G,G,O,O,O,O,O,O,O,O,O,B,B,B,B,B,B,B,B,B,W,W,W,W,W,W,W,W,W'.split(','))

    @cached_property
    def encoded_state(self):
        return encode_state(self.cube)
    
    def does_move_make_sense(self, new_move):
        # get the history of moves that are not indifferent
        history_moves = copy.copy(self.history_moves)
        for move in reversed(history_moves):
            if move in RubiksCube.INDIFFERENT_MOVES[new_move]:
                history_moves.pop()
            else:
                break
        
        # Check if the new move is the reverse of the last move
        if history_moves and new_move == RubiksCube.REVERSE_MOVES[history_moves[-1]]:
            return False
        
        # Check if the new move is the same as the last two moves
        if len(history_moves) >= 2 and new_move == history_moves[-1] == history_moves[-2]:
            return False
        
        return True
    
    def __init__(self, cube=None, state=None, history_moves=None):
        if cube is None and state is None:
            # Initialize the cube with distinct identifiers for each position.
            cube = self.SOLVED
        elif state is not None:
            cube = decode_state(state)
        self.cube = np.array(cube)
        self.history_moves = history_moves if history_moves is not None else []

    def rotate(self, rotation):
        shift_matrix = self.MOVES[rotation]
        new_state = self.cube[shift_matrix]
        new_cube = RubiksCube(
            cube=new_state.tolist(),
            history_moves=self.history_moves + [rotation]
        )
        return new_cube

    def __str__(self):
        # Improved visual display method
        U = self.cube[0:9]
        F = self.cube[9:18]
        R = self.cube[18:27]
        B = self.cube[27:36]
        L = self.cube[36:45]
        D = self.cube[45:54]
        return (f"\n"
                f"\t  {' '.join(U[0:3])}\n"
                f"\t  {' '.join(U[3:6])}\n"
                f"\t  {' '.join(U[6:9])}\n"
                f"\n"
                f"{' '.join(L[0:3])}  {' '.join(F[0:3])}  {' '.join(R[0:3])}  --  {' '.join(B[0:3])}\n"
                f"{' '.join(L[3:6])}  {' '.join(F[3:6])}  {' '.join(R[3:6])}  --  {' '.join(B[3:6])}\n"
                f"{' '.join(L[6:9])}  {' '.join(F[6:9])}  {' '.join(R[6:9])}  --  {' '.join(B[6:9])}\n"
                f"\n"
                f"\t  {' '.join(D[0:3])}\n"
                f"\t  {' '.join(D[3:6])}\n"
                f"\t  {' '.join(D[6:9])}\n")

    def display_cube(self):
        if RubiksCube.root is None:
            RubiksCube.root = tk.Tk()
            RubiksCube.root.title("Rubik's Cube Visualization")

        canvas = tk.Canvas(RubiksCube.root, width=12 * self.sc, height=9 * self.sc)
        canvas.pack(side='top', fill='both', expand=True)

        colors = {'Y': 'yellow', 'R': 'red', 'G': 'green', 'O': 'orange', 'B': 'blue', 'W': 'white'}

        def draw_face(face, row, col):
            for i in range(3):
                for j in range(3):
                    idx = i * 3 + j
                    x0 = (col + j) * self.sc
                    y0 = (row + i) * self.sc
                    x1 = x0 + self.sc
                    y1 = y0 + self.sc
                    color = colors[face[idx]]
                    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='black')
                    # Adding text label
                    canvas.create_text(x0 + self.sc/2, y0 + self.sc/2, text=face[idx], fill='black', font=('Arial', int(self.sc/5)))

        U = self.cube[0:9]
        F = self.cube[9:18]
        R = self.cube[18:27]
        B = self.cube[27:36]
        L = self.cube[36:45]
        D = self.cube[45:54]

        draw_face(U, 0, 3)  # U
        draw_face(R, 3, 6)  # R
        draw_face(F, 3, 3)  # F
        draw_face(D, 6, 3)  # D
        draw_face(L, 3, 0)  # L
        draw_face(B, 3, 9)  # B

        RubiksCube.root.update()

    __front_clockwise = np.array([
        0, 1, 2, 3, 4, 5, 44, 41, 38, 15, 12, 9, 16, 13, 10, 17, 14, 11, 6, 19, 20, 7, 22, 23, 8, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 45, 39, 40, 46, 42, 43, 47, 24, 21, 18, 48, 49, 50, 51, 52, 53
    ])
    __front_anticlockwise = np.array(generate_anticlockwise(__front_clockwise))

    __up_clockwise = np.array([
        2, 5, 8, 1, 4, 7, 0, 3, 6, 18, 19, 20, 12, 13, 14, 15, 16, 17, 27, 28, 29, 21, 22, 23, 24, 25, 26, 36, 37, 38, 30, 31, 32, 33, 34, 35, 9, 10, 11, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53
    ])
    __up_anticlockwise = np.array(generate_anticlockwise(__up_clockwise))

    __right_clockwise = np.array([
        0, 1, 11, 3, 4, 14, 6, 7, 17, 9, 10, 47, 12, 13, 50, 15, 16, 53, 24, 21, 18, 25, 22, 19, 26, 23, 20, 27, 28, 2, 30, 31, 5, 33, 34, 8, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 29, 48, 49, 32, 51, 52, 35
    ])
    __right_anticlockwise = np.array(generate_anticlockwise(__right_clockwise))

    __down_clockwise = np.array([
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 42, 43, 44, 18, 19, 20, 21, 22, 23, 15, 16, 17, 27, 28, 29, 30, 31, 32, 24, 25, 26, 36, 37, 38, 39, 40, 41, 33, 34, 35, 51, 48, 45, 52, 49, 46, 53, 50, 47
    ])
    __down_anticlockwise = np.array(generate_anticlockwise(__down_clockwise))

    __back_clockwise = np.array([
        20, 23, 26, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 53, 21, 22, 52, 24, 25, 51, 33, 30, 27, 34, 31, 28, 35, 32, 29, 2, 37, 38, 1, 40, 41, 0, 43, 44, 45, 46, 47, 48, 49, 50, 36, 39, 42
    ])
    __back_anticlockwise = np.array(generate_anticlockwise(__back_clockwise))

    __left_clockwise = np.array([
        35, 1, 2, 32, 4, 5, 29, 7, 8, 0, 10, 11, 3, 13, 14, 6, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 51, 30, 31, 48, 33, 34, 45, 42, 39, 36, 43, 40, 37, 44, 41, 38, 9, 46, 47, 12, 49, 50, 15, 52, 53
    ])
    __left_anticlockwise = np.array(generate_anticlockwise(__left_clockwise))

    F = 'F'
    Fi = 'Fi'
    U = 'U'
    Ui = 'Ui'
    R = 'R'
    Ri = 'Ri'
    D = 'D'
    Di = 'Di'
    B = 'B'
    Bi = 'Bi'
    L = 'L'
    Li = 'Li'

    MOVES = {
        F: __front_clockwise,
        Fi: __front_anticlockwise,
        U: __up_clockwise,
        Ui: __up_anticlockwise,
        R: __right_clockwise,
        Ri: __right_anticlockwise,
        D: __down_clockwise,
        Di: __down_anticlockwise,
        B: __back_clockwise,
        Bi: __back_anticlockwise,
        L: __left_clockwise,
        Li: __left_anticlockwise
    }

    REVERSE_MOVES = {
        F: Fi,
        Fi: F,
        U: Ui,
        Ui: U,
        R: Ri,
        Ri: R,
        D: Di,
        Di: D,
        B: Bi,
        Bi: B,
        L: Li,
        Li: L
    }

    INDIFFERENT_MOVES = {
        F: (B, Bi),
        Fi: (B, Bi),
        B: (F, Fi),
        Bi: (F, Fi),
        R: (L, Li),
        Ri: (L, Li),
        L: (R, Ri),
        Li: (R, Ri),
        U: (D, Di),
        Ui: (D, Di),
        D: (U, Ui),
        Di: (U, Ui)
    }

if __name__ == "__main__":
    cube = RubiksCube()
    cube.display_cube()
    cube.rotate(RubiksCube.U).display_cube()
    tk.mainloop()

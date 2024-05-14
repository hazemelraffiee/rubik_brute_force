import tkinter as tk

def generate_anticlockwise(clockwise):
        anticlockwise = [0] * 54
        for i in range(54):
            anticlockwise[clockwise[i]] = i
        return tuple(anticlockwise)

class RubiksCube:

    root = None
    next_canvas_y = 0  # Keep track of where the next canvas should start in y
    sc = 50  # scale for each sticker

    SOLVED = list('Y' * 9 + 'R' * 9 + 'G' * 9 + 'O' * 9 + 'B' * 9 + 'W' * 9)
    
    def __init__(self, cube=None):
        if cube is None:
            # Initialize the cube with distinct identifiers for each position.
            cube = self.SOLVED
        self.cube = cube

    def rotate(self, shift_matrix):
        # Apply the shift matrix to rotate the cube
        return RubiksCube([self.cube[i] for i in shift_matrix])
    
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

    front_clockwise = [
        0, 1, 2, 3, 4, 5, 44, 41, 38, 15,
        12, 9, 16, 13, 10, 17, 14, 11, 6,
        19, 20, 7, 22, 23, 8, 25, 26, 27,
        28, 29, 30, 31, 32, 33, 34, 35, 36,
        37, 45, 39, 40, 46, 42, 43, 47, 24,
        21, 18, 48, 49, 50, 51, 52, 53
    ]
    front_anticlockwise = generate_anticlockwise(front_clockwise)

    up_clockwise = [
        2, 5, 8,
        1, 4, 7,
        0, 3, 6,
        
        18, 19, 20,
        12, 13, 14,
        15, 16, 17,
        
        27, 28, 29,
        21, 22, 23,
        24, 25, 26,
        
        36, 37, 38,
        30, 31, 32,
        33, 34, 35,
        
        9, 10, 11,
        39, 40, 41,
        42, 43, 44,
        
        45, 46, 47,
        48, 49, 50,
        51, 52, 53
    ]
    up_anticlockwise = generate_anticlockwise(up_clockwise)

    right_clockwise = [
        0, 1, 11,
        3, 4, 14,
        6, 7, 17,  # Up face swaps right column with Front

        9, 10, 47,
        12, 13, 50,
        15, 16, 53,  # Front face swaps right column with Down

        24, 21, 18,
        25, 22, 19,
        26, 23, 20,  # Right face itself rotates CW

        27, 28, 2,
        30, 31, 5,
        33, 34, 8,   # Back face swaps right column with Up (needs inverting)

        36, 37, 38,
        39, 40, 41,
        42, 43, 44,  # Left face unchanged

        45, 46, 29,
        48, 49, 32,
        51, 52, 35  # Down face swaps right column with Back
    ]
    right_anticlockwise = generate_anticlockwise(right_clockwise)

    down_clockwise = [
        0, 1, 2,
        3, 4, 5,
        6, 7, 8,   # Up face unchanged

        9, 10, 11,
        12, 13, 14,
        42, 43, 44,  # Front face

        18, 19, 20,
        21, 22, 23,
        15, 16, 17,  # Right face

        27, 28, 29,
        30, 31, 32,
        24, 25, 26,  # Back face

        36, 37, 38,
        39, 40, 41,
        33, 34, 35,  # Left face

        51, 48, 45,
        52, 49, 46,
        53, 50, 47   # Down face itself rotates CW
    ]
    down_anticlockwise = generate_anticlockwise(down_clockwise)


    back_clockwise = [
        20, 23, 26,
        3, 4, 5,
        6, 7, 8,   # Up face unchanged except top row

        9, 10, 11,
        12, 13, 14,
        15, 16, 17,  # Front face unchanged

        18, 19, 53,
        21, 22, 52,
        24, 25, 51,  # Right face, bottom row moved

        33, 30, 27,
        34, 31, 28,
        35, 32, 29,  # Back face rotates CW

        2, 37, 38,
        1, 40, 41,
        0, 43, 44,  # Left face, top row moved

        45, 46, 47,
        48, 49, 50,
        36, 39, 42  # Down face, bottom row moved
    ]
    back_anticlockwise = generate_anticlockwise(back_clockwise)

    left_clockwise = [
        # Up face: left column moves to Back face right column (inverted)
        35, 1, 2,
        32, 4, 5,
        29, 7, 8,

        # Front face: left column moves to Up face left column
        0, 10, 11,
        3, 13, 14,
        6, 16, 17,

        # Right face unchanged
        18, 19, 20,
        21, 22, 23,
        24, 25, 26,

        # Back face: right column moves to Down face left column (inverted)
        27, 28, 51,
        30, 31, 48,
        33, 34, 45,

        # Left face (O) itself rotates CW
        42, 39, 36,
        43, 40, 37,
        44, 41, 38,

        # Down face: left column moves to Front face left column
        9, 46, 47,
        12, 49, 50,
        15, 52, 53
    ]

    left_anticlockwise = generate_anticlockwise(left_clockwise)



if __name__ == "__main__":
    cube = RubiksCube()
    cube.display_cube()
    cube.rotate(RubiksCube.up_clockwise).display_cube()
    tk.mainloop()
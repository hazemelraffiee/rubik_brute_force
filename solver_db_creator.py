from datetime import datetime
import hashlib
import sqlite3
from rubik_cube import RubiksCube


def hash_state(state):
    """Generate a hash for the cube state."""
    return hashlib.sha256(state.encode()).hexdigest()

def initialize_db(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cube_states (
            hash TEXT PRIMARY KEY,
            reverse_move TEXT,
            steps INTEGER
        )
    ''')
    conn.commit()

def insert_states(conn, states):
    c = conn.cursor()
    c.executemany('''
        INSERT OR IGNORE INTO cube_states (hash, reverse_move, steps)
        VALUES (?, ?, ?)
    ''', states)
    print('flushing...')
    conn.commit()
    
def state_exists(conn, state):
    state_hash = hash_state(state)
    c = conn.cursor()
    c.execute('SELECT 1 FROM cube_states WHERE hash = ?', (state_hash,))
    exists = c.fetchone() is not None
    return exists

def brute_force_solver(conn, batch_size=100000):
    initialize_db(conn)
    cube = RubiksCube()
    initial_state = ','.join(cube.cube)
    insert_states(conn, [(hash_state(initial_state), None, 0)])

    moves = {
        'F': RubiksCube.front_clockwise,
        'Fi': RubiksCube.front_anticlockwise,
        'U': RubiksCube.up_clockwise,
        'Ui': RubiksCube.up_anticlockwise,
        'R': RubiksCube.right_clockwise,
        'Ri': RubiksCube.right_anticlockwise,
        'D': RubiksCube.down_clockwise,
        'Di': RubiksCube.down_anticlockwise,
        'B': RubiksCube.back_clockwise,
        'Bi': RubiksCube.back_anticlockwise,
        'L': RubiksCube.left_clockwise,
        'Li': RubiksCube.left_anticlockwise
    }
    reverse_moves = {
        'F': 'Fi',
        'Fi': 'F',
        'U': 'Ui',
        'Ui': 'U',
        'R': 'Ri',
        'Ri': 'R',
        'D': 'Di',
        'Di': 'D',
        'B': 'Bi',
        'Bi': 'B',
        'L': 'Li',
        'Li': 'L'
    }

    states_to_process = [(cube, 0)]
    batch = []

    last_printed = None

    while states_to_process:
        current_cube, current_steps = states_to_process.pop(0)
        if current_steps != last_printed:
            timestamp = datetime.now()
            print(f'{timestamp} == Current Steps: {current_steps}')
            last_printed = current_steps

        for move, matrix in moves.items():
            new_cube = current_cube.rotate(matrix)
            new_state = ','.join(new_cube.cube)
            state_hash = hash_state(new_state)
            if not state_exists(conn, new_state):
                batch.append((state_hash, reverse_moves[move], current_steps + 1))
                states_to_process.append((new_cube, current_steps + 1))

        if len(batch) >= batch_size:
            insert_states(conn, batch)
            batch.clear()

    # Insert any remaining states in the batch
    if batch:
        insert_states(conn, batch)

# Run the brute-force solver
conn = sqlite3.connect('rubiks_cube.db')
brute_force_solver(conn)
conn.close()

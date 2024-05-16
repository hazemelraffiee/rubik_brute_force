from datetime import datetime
import multiprocessing
import sqlite3
import threading
import queue
from rubik_cube import RubiksCube
from concurrent.futures import ThreadPoolExecutor, as_completed

def initialize_db(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS cube_states (
            state TEXT PRIMARY KEY,
            move TEXT,
            steps INTEGER
        )
    ''')
    conn.commit()
    c.execute('CREATE INDEX IF NOT EXISTS idx_state ON cube_states(state)')
    conn.commit()

def insert_states(batch):
    conn = sqlite3.connect('rubiks_cube.db')
    c = conn.cursor()
    c.executemany('''
        INSERT OR IGNORE INTO cube_states (state, move, steps)
        VALUES (?, ?, ?)
    ''', batch)
    conn.commit()
    conn.close()
    
def process_cube_state(cube: RubiksCube, current_steps, lock):
    batch = []
    new_states = []
    for move in RubiksCube.MOVES:
        if not cube.does_move_make_sense(move):
            continue

        new_cube = cube.rotate(move)
        # if the new state appears in the history states, continue
        with lock:
            batch.append((new_cube.encoded_state, RubiksCube.REVERSE_MOVES[move], current_steps + 1))
            new_states.append((new_cube, current_steps + 1))
    return batch, new_states

def db_handler_thread(q, batch_size):
    batch = []
    while True:
        item = q.get()
        if item is None:
            break
        batch.append(item)
        if len(batch) >= batch_size:
            insert_states(batch)
            batch.clear()
    # Insert any remaining states in the batch
    if batch:
        insert_states(batch)

def brute_force_solver(batch_size=5000, max_workers=multiprocessing.cpu_count()):
    conn = sqlite3.connect('rubiks_cube.db')
    initialize_db(conn)
    conn.close()
    
    solved_cube = RubiksCube()
    initial_state = solved_cube.encoded_state

    # Check if the initial state is already in the database
    conn = sqlite3.connect('rubiks_cube.db')
    c = conn.cursor()
    c.execute('SELECT state FROM cube_states WHERE state = ?', (initial_state,))
    if c.fetchone() is None:
        insert_states([(initial_state, None, 0)])
    conn.close()

    # Load all states from the database that have been processed
    conn = sqlite3.connect('rubiks_cube.db')
    c = conn.cursor()
    c.execute('SELECT state, steps FROM cube_states')
    states_to_process = [(RubiksCube(state=state), steps) for state, steps in c.fetchall() if steps > 0]
    conn.close()

    if not states_to_process:
        states_to_process = [(solved_cube, 0)]
    
    lock = threading.Lock()
    last_printed = None

    q = queue.Queue()

    db_thread = threading.Thread(target=db_handler_thread, args=(q, batch_size))
    db_thread.start()

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []

        while states_to_process or futures:
            while states_to_process and len(futures) < max_workers * 2:
                current_cube, current_steps = states_to_process.pop(0)
                if current_steps != last_printed:
                    timestamp = datetime.now()
                    print(f'{timestamp} == Current Steps: {current_steps}')
                    print(f'{timestamp} == States to Process: {len(states_to_process)}')
                    last_printed = current_steps

                future = executor.submit(process_cube_state, current_cube, current_steps, lock)
                futures.append(future)

            for future in as_completed(futures):
                new_batch, new_states = future.result()
                for state in new_batch:
                    q.put(state)
                states_to_process.extend(new_states)
                futures.remove(future)

        # Final flush of remaining futures
        for future in as_completed(futures):
            new_batch, new_states = future.result()
            for state in new_batch:
                q.put(state)
            states_to_process.extend(new_states)

    # Signal the DB handler to stop
    q.put(None)
    db_thread.join()

# Run the brute-force solver
brute_force_solver()

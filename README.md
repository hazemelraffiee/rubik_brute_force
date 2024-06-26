# Rubik's Cube Solver

## Overview

This repository contains a Python-based Rubik's Cube solver that includes several key components:

- **Rubik's Cube Simulation (`rubik_cube.py`)**: A class-based representation of a Rubik's Cube that supports encoding and decoding states, displaying the cube, and performing rotations.
- **Unit Tests (`test_rubik.py`)**: A suite of tests to ensure the correctness of the cube rotations and encoding/decoding functionality.
- **Brute Force Solver (`solver_db_creator.py`)**: A script to generate a database of cube states and their respective moves using a brute-force approach.

## Features

- **Rubik's Cube Simulation**:
  - Encodes cube states into a compact string representation.
  - Decodes string representations back into cube states.
  - Supports displaying the cube visually using Tkinter.
  - Implements rotations for all six faces in both clockwise and anti-clockwise directions.
  
- **Unit Tests**:
  - Tests each rotation to ensure the cube returns to its initial state after performing a rotation 400 times.
  - Tests the cube's behavior after 100 random rotations and their inverses.
  
- **Brute Force Solver**:
  - Initializes an SQLite database to store cube states and moves.
  - Uses multi-threading to efficiently generate new cube states.
  - Processes cube states and stores them in the database for further analysis.

## Requirements

- Python 3.6+
- Tkinter for GUI visualization
- `pipenv` for managing dependencies and virtual environment

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/rubiks_cube_solver.git
   cd rubiks_cube_solver
   ```

2. Install `pipenv` if you haven't already:
   ```bash
   pip install pipenv
   ```

3. Install the required packages using `pipenv`:
   ```bash
   pipenv install
   ```

4. Activate the virtual environment:
   ```bash
   pipenv shell
   ```

## Usage

### Running the Rubik's Cube Simulation

You can run the Rubik's Cube simulation and visualize the cube:

```bash
python rubik_cube.py
```

This will open a Tkinter window displaying the cube. The initial state and a rotated state will be displayed.

### Running the Unit Tests

To run the unit tests and ensure that everything is working correctly:

```bash
python -m unittest discover
```

### Running the Brute Force Solver

To generate the database of cube states and their moves, run:

```bash
python solver_db_creator.py
```

This script will initialize the database, process cube states, and store them in the database using multi-threading for efficiency.

## Code Structure

- **`rubik_cube.py`**: Contains the `RubiksCube` class with methods for encoding, decoding, rotating, and displaying the cube.
- **`test_rubik.py`**: Contains unit tests for the `RubiksCube` class.
- **`solver_db_creator.py`**: Contains the brute-force solver logic that generates and stores cube states in an SQLite database.

## Contributing

Contributions are welcome! If you find a bug or have a feature request, please open an issue. If you would like to contribute code, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

Thanks to the contributors and the open-source community for their invaluable support and resources.
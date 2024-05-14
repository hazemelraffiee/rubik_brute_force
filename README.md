# Rubik's Cube Brute Force Solver

This project implements a Python-based brute force solver for the Rubik's Cube, designed to find the shortest path to a solved state. Using efficient database operations and hashing, it systematically explores all possible moves to discover the optimal solution.

## Features

- **Optimized State Storage**: Uses SHA-256 hashing to store and compare cube states efficiently.
- **Batch Database Operations**: Performs batch inserts and queries to speed up the brute force search.
- **Comprehensive Move Set**: Implements all standard Rubik's Cube moves and their reversals.
- **Shortest Path Discovery**: Tracks and updates the shortest path to the solved state.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Implementation Details](#implementation-details)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/hazemelraffiee/rubik_brute_force.git
    cd rubik_brute_force
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
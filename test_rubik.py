import random
import unittest
from rubik_cube import RubiksCube
from parameterized import parameterized


ROTATIONS = {
    "front_clockwise": RubiksCube.front_clockwise,
    "front_anticlockwise": RubiksCube.front_anticlockwise,
    "up_clockwise": RubiksCube.up_clockwise,
    "up_anticlockwise": RubiksCube.up_anticlockwise,
    "right_clockwise": RubiksCube.right_clockwise,
    "right_anticlockwise": RubiksCube.right_anticlockwise,
    "back_clockwise": RubiksCube.back_clockwise,
    "back_anticlockwise": RubiksCube.back_anticlockwise,
    "left_clockwise": RubiksCube.left_clockwise,
    "left_anticlockwise": RubiksCube.left_anticlockwise,
    "down_clockwise": RubiksCube.down_clockwise,
    "down_anticlockwise": RubiksCube.down_anticlockwise
}


class TestRubiksCube(unittest.TestCase):

    @parameterized.expand([(name, rotation) for name, rotation in ROTATIONS.items()])
    def test_rotations(self, name, rotation):
        cube = RubiksCube()
        initial_state = str(cube)

        # Apply the same rotation 400 times
        for _ in range(400):
            cube = cube.rotate(rotation)
        
        # Check if the cube returned to its initial state
        self.assertEqual(str(cube), initial_state, f"Failed on rotation: {name}")

    def test_100_random_rotations(self):
        cube = RubiksCube()
        initial_state = str(cube)

        rotations = list(ROTATIONS.items())
        performed_rotations = []

        # Perform 100 random rotations
        for _ in range(100):
            rotation_name, rotation_matrix = random.choice(rotations)
            cube = cube.rotate(rotation_matrix)
            performed_rotations.append(rotation_name)

        # Reverse the performed rotations in the reverse order
        for rotation_name in reversed(performed_rotations):
            anti_rotation_name = rotation_name.replace('anticlockwise', 'TEMP').replace('clockwise', 'anticlockwise').replace('TEMP', 'clockwise')
            anti_rotation_matrix = ROTATIONS[anti_rotation_name]
            cube = cube.rotate(anti_rotation_matrix)

        # Check if the cube returned to its initial state
        self.assertEqual(str(cube), initial_state, "Cube did not return to initial state after 100 random rotations and their reverses.")


if __name__ == '__main__':
    unittest.main()

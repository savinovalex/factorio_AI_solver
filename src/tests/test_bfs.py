import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + '/build')
import numpy as np

import bfs_module
from game_env.state import State

field = np.array([[0, 0, 0, 5],
                  [5, 5, 0, 0],
                  [0, 0, 0, 5],
                  [0, 5, 5, 0],
                  [0, 0, 0, 0],])

legs = bfs_module.find_path_legs(field, (0, 0), (4, 3))
state = State(field)
state.apply_path_legs(legs)
print(state)



def test_empty():
    field = np.array([[0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0],
                      [0, 0, 0, 0], ])


    assert [(0, 0, 1), (0, 1, 1), (0, 2, 1), (0, 3, 2), (1, 3, 2), (2, 3, 2), (3, 3, 2), (4, 3, 2)] == \
           bfs_module.find_path_legs(field, (0, 0), (4, 3))

def test_walls():
    field = np.array([[0, 5, 0, 0],
                      [0, 0, 5, 0],
                      [0, 0, 0, 5],
                      [0, 0, 0, 5],
                      [0, 0, 0, 0], ])

    assert [(0, 0, 2), (1, 0, 1), (1, 1, 2), (2, 1, 1), (2, 2, 2), (3, 2, 2), (4, 2, 1), (4, 3, 1)] == \
           bfs_module.find_path_legs(field, (0, 0), (4, 3))

def test_walls_reversed():
    field = np.array([[0, 5, 0, 0],
                      [0, 0, 5, 0],
                      [0, 0, 0, 5],
                      [0, 0, 0, 5],
                      [0, 0, 0, 0], ])

    assert [(4, 3, 3), (4, 2, 3), (4, 1, 3), (4, 0, 4), (3, 0, 4), (2, 0, 4), (1, 0, 4), (0, 0, 4)] == \
           bfs_module.find_path_legs(field, (4, 3), (0, 0))

def test_with_repr():
    field = np.array([[0, 0, 0, 5],
                      [5, 5, 0, 0],
                      [0, 0, 0, 5],
                      [0, 5, 5, 0],
                      [0, 0, 0, 0], ])

    legs = bfs_module.find_path_legs(field, (0, 0), (4, 3))
    state = State(field)
    state.apply_path_legs(legs)

    s = """
>>|#
##|.
|<<#
|##.
>>>>
"""

    assert s.strip() == str(state)

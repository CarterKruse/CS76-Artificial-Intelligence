# test_sensorless.py
# A testing file for the A* search for the sensorless problem.
# Carter Kruse (September 27, 2023)

from SensorlessProblem import SensorlessProblem
from Maze import Maze

from uninformed_search import bfs_search
from astar_search import astar_search

# Null Heurisitic - Useful for testing A* search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

# Test Problems
    # Comment out the tests that you do not want to run.
test_maze1 = Maze("sensorless1.maz")
test_problem = SensorlessProblem(test_maze1)

# test_maze2 = Maze("sensorless2.maz")
# test_problem = SensorlessProblem(test_maze2)

# # # # #

# Using BFS to create a simple test.
# result = bfs_search(test_problem)
# print(result)

# # # # #

# This test should explore a lot of nodes. (It's just a uniform-cost search.)
result = astar_search(test_problem, null_heuristic)
print(result)

# This should do a bit better. (It uses the sensorless heurisitic.)
result = astar_search(test_problem, test_problem.sensorless_heuristic)
print(result)

# Use the terminal/console to create a graphical display of the solution.
test_problem.animate_path(result.path)

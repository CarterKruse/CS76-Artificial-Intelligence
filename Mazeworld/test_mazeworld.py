# test_mazeworld.py
# A testing file for the A* search for the mazeworld problem, specifically multi-robot coordination.
# Carter Kruse (September 27, 2023)

from MazeworldProblem import MazeworldProblem
from Maze import Maze

from uninformed_search import bfs_search
from astar_search import astar_search

# Null Heurisitic - Useful for testing A* search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0

# Test Problems
    # Comment out the tests that you do not want to run.
# test_maze3 = Maze("maze3.maz")
# test_problem = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

# test_maze4 = Maze("maze4.maz")
# test_problem = MazeworldProblem(test_maze4, (20, 2, 19, 2, 18, 2))

test_maze5 = Maze("maze5.maz")
test_problem = MazeworldProblem(test_maze5, (20, 2, 19, 2, 18, 2, 17, 2))

# test_maze6 = Maze("maze6.maz")
# test_problem = MazeworldProblem(test_maze6, (21, 0, 20, 0, 19, 0))

# test_maze7 = Maze("maze7.maz")
# test_problem = MazeworldProblem(test_maze7, (46, 8, 46, 0))

# test_maze8 = Maze("maze8.maz")
# test_problem = MazeworldProblem(test_maze8, (38, 9))

# # # # #

# Checking the 'get_successors()' method.
# print(test_problem.get_successors(test_problem.start_state))

# Using BFS to create a simple test.
# result = bfs_search(test_problem)
# print(result)

# # # # #

# This test should explore a lot of nodes. (It's just a uniform-cost search.)
result = astar_search(test_problem, null_heuristic)
print(result)

# This should do a bit better. (It uses the Manhattan heurisitic.)
result = astar_search(test_problem, test_problem.manhattan_heuristic)
print(result)

# Use the terminal/console to create a graphical display of the solution.
test_problem.animate_path(result.path)

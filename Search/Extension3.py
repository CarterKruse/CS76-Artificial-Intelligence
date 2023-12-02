# Extension3.py
# A testing file (with visualizations) for the BFS, DFS, and IDS search for various problems.
# Carter Kruse (September 18, 2023)

from FoxesProblem import FoxesProblem
from uninformed_search import bfs_search, dfs_search, ids_search

# Create a few test problems.
problem_list = []
problem_list.append(FoxesProblem((3, 3, 1)))
problem_list.append(FoxesProblem((5, 5, 1)))
problem_list.append(FoxesProblem((5, 4, 1)))

# Run the searches.
# Each of the search algorithms should return a SearchSolution object,
# even if the goal was not found. If goal not found, 'len()' of the path
# in the solution object should be 0.

# print(bfs_search(problem331))
# print(dfs_search(problem331))
# print(ids_search(problem331))

# print(bfs_search(problem541))
# print(dfs_search(problem541))
# print(ids_search(problem541))

for problem in problem_list:
    print(problem, end = '\n---\n')
    for state in bfs_search(problem).path:
        print("State: " + str(state))
        print(f"{'C ' * state[0] : <20}", end = '||')
        print(f"{'C ' * (problem.start_state[0] - state[0]) : >20}", end = '')
        print()
        print(f"{'F ' * state[1] : <20}", end = '||')
        print(f"{'F ' * (problem.start_state[1] - state[1]) : >20}", end = '')
        print('\n' + '_' * 41 + '\n')
    print()

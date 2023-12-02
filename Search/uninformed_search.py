# uninformed_search.py
# Contains the BFS, DFS, and IDS search algorithms, in general form.
# Carter Kruse (September 18, 2023)

from collections import deque
from SearchSolution import SearchSolution

# The SearchNode class is useful to wrap state objects, pointing to parent nodes.
class SearchNode:
    # Each SearchNode except the root has a parent node and wraps a state object.
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent

# BFS Search
# This function is not recursive, though it performs memoizing (with a visited set) to prevent loops/cycle.
def bfs_search(search_problem):
    # Initialize the solution, given the search problem and BFS.
    solution = SearchSolution(search_problem, "BFS")

    # Determine the initial state of the search problem, using an instance variable.
    initial_state = search_problem.start_state

    # Create a SearchNode and initialize the frontier.
    initial_node = SearchNode(initial_state)
    frontier = deque([initial_node])

    # Initialize the explored set to keep track of visited states.
    explored = set()

    # Add the initial state to the explored set.
    explored.add(initial_state)

    # While the frontier (queue) contains values...
    while frontier:
        # Pop the leftmost node from the frontier.
        current_node = frontier.popleft()

        # Increment the counter.
        solution.nodes_visited += 1

        # Check if the current state is the goal state.
        if search_problem.is_goal_state(current_node.state):
            # If so, construct the solution path and return the solution.
            solution.path = construct_solution_path(current_node)
            return solution
        
        # Generate the successor states and add them to the frontier.
            # This could be broken down into determining the appropriate actions/transitions.
        for next_state in search_problem.get_successors(current_node.state):
            # Check if the next state is not in the explored set.
            if next_state not in explored:
                # Add the state to the explored set to prevent redundancy.
                explored.add(next_state)

                # Create a new SearchNode with the appropriate parent and add it to the frontier.
                next_node = SearchNode(next_state, parent = current_node)
                frontier.append(next_node)

    # If the frontier is empty and no solution is found, return the solution (empty path).
    return solution

# Backchaining
def construct_solution_path(current_node):
    # Backtrack from the current node (presumably the goal node) to construct the solution path.
    path = []

    # Cycle through until the root (start node) is reached.
    while current_node is not None:
        # Append the 'state' to the path. The 'append' function is faster than 'insert'.
        path.append(current_node.state)

        # Update the pointer of the current node.
        current_node = current_node.parent
    
    # We should reverse the path at the end, as we use the 'append' function.
    return path[::-1]

# DFS Search
# This function is recursive and performs path checking rather than memoizing (no visited set)
# to be memory efficient. The solution is passed along to each new recursive call so that statistics
# like the number of nodes visited or recursion depth might be recorded.
def dfs_search(search_problem, depth_limit = 100, node = None, solution = None):
    # If no node object is given, we create a new search from the starting state.
    if node is None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")
    
    # Increment the counter.
    solution.nodes_visited += 1

    # BASE CASE #1: The current state is the goal state.
    if search_problem.is_goal_state(node.state):
        # If so, construct the solution path and return the solution.
        solution.path = construct_solution_path(node)
        return solution
    
    # BASE CASE #2: The depth limit has been reached.
    if depth_limit <= 0:
        # No solution found within the limit, so we return the (empty) solution.
        return solution 
    
    # RECURSIVE CASE
    # Generate the successor states.
    for next_state in search_problem.get_successors(node.state):
        # Create a new SearchNode with the appropriate parent.
        next_node = SearchNode(next_state, parent = node)

        # Check if this state is within the current DFS path.
        if not is_state_in_path(next_node.state, node):
            # Recursively explore using DFS, decreasing the depth limit and updating the node.
            result = dfs_search(search_problem, depth_limit - 1, next_node, solution)

            # Rather than check if the result is not 'none', we check the path length, as we return a solution.
            if len(result.path) != 0:
                return result
    
    return solution # No solution found (in this branch).

# Path Checking - Returns Boolean
# This function is used to check if a state is already in the path from the current node to the root node.
def is_state_in_path(state, node):
    while node is not None:
        # Check if the states are equivalent.
        if state == node.state:
            return True
        
        # Update the pointer of the current node.
        node = node.parent
    
    return False

# IDS Search
# This function loops around a depth-limited dfs. The aim is to find the shortest path with little memory.
def ids_search(search_problem, depth_limit = 100):
    solution = SearchSolution(search_problem, "IDS")

    # Cycle through the depths for depth-limited search.
    for depth in range(depth_limit):
        result = dfs_search(search_problem, depth)

        # Updating the nodes visited instance variable for the given DFS search.
        # If the aim is to recover the total number of nodes visited for all depths, change to +=
        solution.nodes_visited = result.nodes_visited

        # Rather than check if the result is not 'none', we check the path length, as we return a solution.
        if len(result.path) != 0:
            # Updating the instance variable of the solution, given as a SearchSolution object.
            solution.path = result.path
            return solution
    
    return solution # No solution found.

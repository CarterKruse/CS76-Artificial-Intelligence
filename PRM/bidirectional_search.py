# bidirectional_search.py
# Carter Kruse (November 14th)

from collections import deque
from SearchSolution import SearchSolution

# The SearchNode class is useful to wrap state objects, pointing to parent nodes.
class SearchNode:
    # Each SearchNode except the root has a parent node and wraps a state object.
    def __init__(self, state, parent = None):
        self.state = state
        self.parent = parent

# Bidirectional Search
    # This function is not recursive, though it performs memoizing (with a visited set) to prevent loops/cycle.
def bidirectional_search(search_problem):
    # Initialize the solution, given the search problem and BFS (bidirectional).
    solution = SearchSolution(search_problem, "BFS (bidirectional)")

    # Determine the initial and goal states of the search problem, using instance variables.
    initial_state = search_problem.start_state
    goal_state = search_problem.goal_state

    # Create SearchNodes and initialize the frontiers
    initial_node = SearchNode(initial_state)
    goal_node = SearchNode(goal_state)

    forward_frontier = deque([initial_node])
    backward_frontier = deque([goal_node])

    # Initialize the explored sets to keep track of visited states.
    forward_explored = set()
    backward_explored = set()

    # Add the initial/goal states to the explored sets.
    forward_explored.add(initial_state)
    backward_explored.add(goal_state)

    # While the frontiers (queues) contain values...
    while forward_frontier and backward_frontier:
        # Increment the counter.
        solution.nodes_visited += 1

        # Pop the leftmost node from the frontier.
        current_forward_node = forward_frontier.popleft()

        # Add the state to the explored set to prevent redundancy.
        forward_explored.add(current_forward_node.state)

        # Check if the current state is in the set of backward explored.
        if current_forward_node.state in backward_explored:
            # Determine which backward node matches the state of the current forward node.
            backward_node = next((node for node in backward_frontier if node.state == current_forward_node.state), None)

            # If so, construct the solution path and return the solution.
            solution.path = construct_solution_path(current_forward_node, backward_node)
            return solution
        
        # Generate the successor states and add them to the frontier.
        for next_state in search_problem.get_successors(current_forward_node.state):
            # Check if the next state is not in the explored set.
            if next_state not in forward_explored:
                # Create a new SearchNode with the appropriate parent and add it to the frontier.
                next_forward_node = SearchNode(next_state, parent = current_forward_node)
                forward_frontier.append(next_forward_node)
        
        # Pop the leftmost node from the frontier.
        current_backward_node = backward_frontier.popleft()

        # Add the state to the explored set to prevent redundancy.
        backward_explored.add(current_backward_node.state)

        # Check if the current state is in the set of forward explored.
        if current_backward_node.state in forward_explored:
            # Determine which forward node matches the state of the current backward node.
            forward_node = next((node for node in forward_frontier if node.state == current_backward_node.state), None)

            # If so, construct the solution path and return the solution.
            solution.path = construct_backward_solution_path(current_backward_node, forward_node)
            return solution
        
        # Generate the successor states and add them to the frontier.
        for next_state in search_problem.get_successors(current_backward_node.state):
            # Check if the next state is not in the explored set.
            if next_state not in backward_explored:
                # Create a new SearchNode with the appropriate parent and add it to the frontier.
                next_backward_node = SearchNode(next_state, parent = current_backward_node)
                backward_frontier.append(next_backward_node)

    # If the frontier is empty and no solution is found, return the solution (empty path).
    return solution

# Backchaining
def construct_solution_path(current_forward_node, backward_node):
    # Backtrack from the current node to construct the solution path.
    forward_path = []

    # Cycle through until the root (start node) is reached.
    while current_forward_node is not None:
        # Append the 'state' to the path. The 'append' function is faster than 'insert'.
        forward_path.append(current_forward_node.state)

        # Update the pointer of the current node.
        current_forward_node = current_forward_node.parent
    
    # Backtrack from the current node to construct the solution path.
    backward_path = []

    # Cycle through until the root (goal node) is reached.
    while backward_node is not None:
        # Append the 'state' to the path. The 'append' function is faster than 'insert'.
        backward_path.append(backward_node.state)

        # Update the pointer of the current node.
        backward_node = backward_node.parent
    
    # We should reverse the path at the end, as we use the 'append' function.
    return forward_path[::-1] + backward_path[1:]

# Backchaining
def construct_backward_solution_path(current_backward_node, forward_node):
    # Backtrack from the current node to construct the solution path.
    backward_path = []

    # Cycle through until the root (goal node) is reached.
    while current_backward_node is not None:
        # Append the 'state' to the path. The 'append' function is faster than 'insert'.
        backward_path.append(current_backward_node.state)

        # Update the pointer of the current node.
        current_backward_node = current_backward_node.parent
    
    # Backtrack from the current node to construct the solution path.
    forward_path = []

    # Cycle through until the root (start node) is reached.
    while forward_node is not None:
        # Append the 'state' to the path. The 'append' function is faster than 'insert'.
        forward_path.append(forward_node.state)

        # Update the pointer of the current node.
        forward_node = forward_node.parent
    
    # We should reverse the path at the end, as we use the 'append' function.
    return forward_path[::-1] + backward_path[1:]

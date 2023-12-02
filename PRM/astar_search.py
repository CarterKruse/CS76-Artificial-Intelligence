# astar_search.py
# Carter Kruse (November 14th)

from heapq import heappush, heappop
from SearchSolution import SearchSolution

# The AstarNode class is useful to wrap state objects, pointing to parent nodes.
class AstarNode:
    # Each AstarNode except the root has a parent node and wraps a state object.
    def __init__(self, state, heuristic, parent = None, transition_cost = 0):
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost

    def priority(self):
        # The priority is the sum of the heuristic and transition cost.
            # The transition cost represents the actual cost from the start node.
            # The heuristic represents the estimated cost to the goal node.
        return self.heuristic + self.transition_cost
    
    # Comparison Operator
    # This is needed for 'heappush' and 'heappop' to work with nodes.
    def __lt__(self, other):
        return self.priority() < other.priority()

# Backchaining
# Take the current node and follow its parents back as far as possible.
# Get the states from the nodes, and reverse the resulting list of states.
def construct_solution_path(current_node):
    # Backtrack from the current node (presumably the goal node) to construct the solution path.
    path = []

    # Cycle through until the root (start node) is reached.
    while current_node: # OR while current_node is not None:
        # Append the 'state' to the path. The 'append' function is faster than 'insert'.
        path.append(current_node.state)

        # Update the pointer of the current node.
        current_node = current_node.parent

    # We should reverse the path at the end, as we use the 'append' function.
    return path[::-1] # OR path.reverse()

# A* Search
def astar_search(search_problem, heuristic_function):
    # Initialize the solution, given the search problem and heuristic.
    solution = SearchSolution(search_problem, "A*" + " " + "(" + heuristic_function.__name__ + ")")

    # Determine the initial state of the search problem, using an instance variable.
    initial_state = tuple(search_problem.start_state)

    # Create an AstarNode with the appropriate initial state and heurisitic function.
    initial_node = AstarNode(initial_state, heuristic_function(initial_state))

    # Initialize the priority queue (ordered by cost) and push the initial node.
    priority_queue = []
    heappush(priority_queue, initial_node)

    # Creating the 'visited_cost' dictionary and updating it with the initial state.
    visited_cost = {}
    visited_cost[initial_state] = initial_node.priority()

    # While the priority queue contains values...
    while priority_queue:
        # Pop the node from the priority queue.
        current_node = heappop(priority_queue)

        # Increment the counter.
        solution.nodes_visited += 1

        # If the current state is already within the dictionary and has a higher priority, skip over it.
        if current_node.state in visited_cost and current_node.priority() > visited_cost[current_node.state]:
            continue

        # Check if the current state is the goal state.
        if search_problem.is_goal_state(current_node.state):
            # If so, construct the solution path and return the solution.
            solution.path = construct_solution_path(current_node)
            
            # The solution cost may be considered the "fuel" cost or the transition cost of the current node.
            solution.cost = len(set(robot_locations[1:] for robot_locations in solution.path))
            # solution.cost = current_node.transition_cost
            
            return solution

        # Generate the successor states and add them to the priority queue.
            # This could be broken down into determining the appropriate actions/transitions.
        for next_state in search_problem.get_successors(current_node.state):
            # Create a new AstarNode with the appropriate 
            next_node = AstarNode(next_state, heuristic_function(next_state), parent = current_node, transition_cost = current_node.transition_cost + 1)
            
            # If the next state has not been visited or is in the frontier with a higher cost...
            if next_state not in visited_cost or next_node.priority() < visited_cost[next_state]:
                # Update the dictionary with the appropriate priority/cost.
                visited_cost[next_state] = next_node.priority()

                # Push the next node to the heap.
                heappush(priority_queue, next_node)
    
    # If the frontier is empty and no solution is found, return the solution.
    return solution

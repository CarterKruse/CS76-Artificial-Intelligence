# GraphProblem.py
# Carter Kruse (November 14th)

from heuristics import total_angular_distance

class GraphProblem:
    def __init__(self, graph, start_state, goal_state):
        self.graph = graph
        self.start_state = start_state
        self.goal_state = goal_state
    
    # Determine the successors (neighbors) for a given state (node).
    def get_successors(self, state):
        return list(self.graph[state])
    
    # Test if the state is at the goal.
    def is_goal_state(self, state):
        return state == self.goal_state
    
    # Calculate the angular heuristic.
    def angular_heuristic(self, state):
        return total_angular_distance(state, self.goal_state)
    
    def __str__(self):
        # You may add further information about the problem state (if necessary).
        string =  "Graph Problem: " + str(self.start_state) + ' -> ' + str(self.goal_state)
        return string

# Extension2.py
# A file defining the problem set-up, along with the goal state and successors method.
# Carter Kruse (September 18, 2023)

import random
from uninformed_search import bfs_search, dfs_search, ids_search

class FoxesProblem:
    def __init__(self, start_state = (3, 3, 1, 2)):
        self.start_state = start_state
        self.goal_states = [(0, 0, 0, n) for n in range(start_state[3] + 1)]

        # The total number of chickens/foxes is determined based on the start state.
        self.chickens = self.start_state[0]
        self.foxes = self.start_state[1]
        self.max_eaten = self.start_state[3]
    
    # Determine the succcessor states for a given state.
    def get_successors(self, state):
        # Initialize the list of successors, which starts out as empty.
        successors_list = []

        # Enumerate the possible moves for the simple problem, according to which side the boat is on.
        if state[2] == 0:
            possible_moves = [(0, 1, 1), (1, 0, 1), (0, 2, 1), (2, 0, 1), (1, 1, 1)]
        else:
            possible_moves = [(0, -1, -1), (-1, 0, -1), (0, -2, -1), (-2, 0, -1), (-1, -1, -1)]
        
        # Introduce randomness to allow for consecutive iterations to be independent of a deterministic outcome.
        random.shuffle(possible_moves)

        # Cycle through the list of possible moves.
        for move in possible_moves:
            # Creating the next state, according to the appropriate transition.
            next_state = (state[0] + move[0], state[1] + move[1], state[2] + move[2], state[3])

            # Determine the number of chickens eaten by modifying the 'is_safe' method.
            chickens_eaten = self.is_safe(next_state)

            # Check if a given state (determined by an initial state and transition) is safe.
                # The tuple (-1, -1) is considered to be an error state, or false, which does not allow for ANY safe move.
            if chickens_eaten != (-1, -1):
                successors_list.append((next_state[0] - chickens_eaten[0], next_state[1], next_state[2], next_state[3] - (chickens_eaten[0] + chickens_eaten[1])))

        return successors_list
    
    # Test if a given state is safe (before adding to successor list).
    def is_safe(self, state):
        # Rather than modify the instance variable, which would mess up further iterations (in a loop),
        # we calculate the total number of chickens left using the encoded information.
            # The difference between the 'max_eaten' and the 'state[3]' is the number of chickens eaten.
        total_chickens = self.chickens - (self.max_eaten - state[3])

        # Capacity Constraints: Check that there are not too many chickens/foxes.
        if state[0] < 0 or state[0] > total_chickens or state[1] < 0 or state[1] > self.foxes:
            return (-1, -1)
        
        # We do not need to consider checking the number of boats, because it is never out of bounds.
        
        # Eating Constraints: Check to see what number of the chickens are eaten (outnumbered) by the foxes.
        # We consider the case where there are no chickens on a given side, which is okay.

        # The 'lost' variables encode the number of chickens lost on the corresponding sides of the river.
        (lost_1, lost_0) = (0, 0)
        
        if state[0] < state[1] and state[0] != 0:
            lost_1 = state[0]
        if total_chickens - state[0] < self.foxes - state[1] and total_chickens - state[0] != 0:
            lost_0 = total_chickens - state[0]
        
        if lost_1 + lost_0 <= state[3]:
            return (lost_1, lost_0)
        else:
            return (-1, -1)
    
    # Test if the state is at the goal.
    def is_goal_state(self, state):
        for goal_state in self.goal_states:
            if state == goal_state:
                return True
        return False
    
    def __str__(self):
        string =  "Foxes & Chickens Problem (Extended): " + str(self.start_state)
        return string

# Test Code
if __name__ == "__main__":
    # Create a few test problems.
    problem3310 = FoxesProblem((3, 3, 1, 0))
    problem3312 = FoxesProblem((3, 3, 1, 2))
    problem3313 = FoxesProblem((3, 3, 1, 3))

    # Run the searches.
    # Each of the search algorithms should return a SearchSolution object,
    # even if the goal was not found. If goal not found, 'len()' of the path
    # in the solution object should be 0.

    # print(bfs_search(problem3310))
    # print(dfs_search(problem3310))
    # print(ids_search(problem3310))

    # print(bfs_search(problem3312))
    # print(dfs_search(problem3312))
    # print(ids_search(problem3312))

    # print(bfs_search(problem3313))
    # print(dfs_search(problem3313))
    # print(ids_search(problem3313))

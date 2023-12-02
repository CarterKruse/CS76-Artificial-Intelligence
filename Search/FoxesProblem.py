# FoxesProblem.py
# A file defining the problem set-up, along with the goal state and successors method.
# Carter Kruse (September 18, 2023)

import random

class FoxesProblem:
    def __init__(self, start_state = (3, 3, 1)):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)

        # The total number of chickens/foxes is determined based on the start state.
        self.chickens = self.start_state[0]
        self.foxes = self.start_state[1]
    
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
            next_state = (state[0] + move[0], state[1] + move[1], state[2] + move[2])

            # Check if a given state (determined by an initial state and transition) is safe.
            if self.is_safe(next_state):
                successors_list.append(next_state)

        return successors_list
    
    # Test if a given state is safe (before adding to successor list).
    def is_safe(self, state):
        # Capacity Constraints: Check that there are not too many chickens/foxes.
        if state[0] < 0 or state[0] > self.chickens or state[1] < 0 or state[1] > self.foxes:
            return False
        
        # We do not need to consider checking the number of boats, because it is never out of bounds.
        
        # Eating Constraints: Check that none of the chickens are eaten (outnumbered) by the foxes.
        # We consider the case where there are no chickens on a given side, which is okay.
        if state[0] < state[1] and state[0] != 0:
            return False
        if self.chickens - state[0] < self.foxes - state[1] and self.chickens - state[0] != 0:
            return False
        
        return True
    
    # Test if the state is at the goal.
    def is_goal_state(self, state):
        if state == self.goal_state:
            return True
        return False
    
    def __str__(self):
        string =  "Foxes & Chickens Problem: " + str(self.start_state)
        return string

# Test Code
if __name__ == "__main__":
    test = FoxesProblem((3, 3, 1))
    print(test.get_successors((3, 3, 1)))
    print(test)

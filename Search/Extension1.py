# Extension1.py
# A file defining the problem set-up, along with the goal state and sucessors method.
# Carter Kruse (September 18, 2023)

import random
from uninformed_search import bfs_search, dfs_search, ids_search

class FoxesProblem:
    def __init__(self, start_state = (3, 3, 1), capacity = 5):
        self.start_state = start_state
        self.goal_state = (0, 0, 0)

        # Defining the capacity of the boat.
        self.capacity = capacity

        # The total number of chickens/foxes is determined based on the start state.
        self.chickens = self.start_state[0]
        self.foxes = self.start_state[1]
    
    # Determine the succcessor states for a given state.
    def get_successors(self, state):
        # Initialize the list of successors, which starts out as empty.
        successors_list = []

        # Using a clever for loop, we enumerate all of the possible moves for the advanced problem,
        # according to which side the boat is on. This allows for ANY capacity constraint.
        possible_moves = []
        proposed_moves = [(c, f, 1) for c in range(self.chickens + 1) for f in range(self.foxes + 1)]

        # Cycle through the proposed moves to see what is valid.
        for move in proposed_moves:
            # Check if the capacity constraint (of the boat) are met, and at least one animal is in the boat to move it.
            if move[0] + move[1] <= self.capacity and (move[0] != 0 or move[1] != 0):
               # Check that none of the chickens are eaten (outnumbered) on the boat itself.
               if move[0] <= move[1] or move[1] == 0:
                    # Add the proposed move to the list of possible moves.
                    possible_moves.append(move)
        
        # Introduce randomness to allow for consecutive iterations to be independent of a deterministic outcome.
        random.shuffle(possible_moves)

        # Cycle through the list of possible moves.
        for move in possible_moves:
            # Creating the next state, according to the appropriate transition.
            if state[2] == 0:
                next_state = (state[0] + move[0], state[1] + move[1], state[2] + move[2])
            else:
                next_state = (state[0] - move[0], state[1] - move[1], state[2] - move[2])

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
        string =  "Foxes & Chickens Problem (Extended): " + str(self.start_state) + " Capacity: " + str(self.capacity)
        return string

# Test Code
if __name__ == "__main__":
    # Create a few test problems.
    problem331cap2 = FoxesProblem((3, 3, 1), capacity = 2)
    problem331cap3 = FoxesProblem((3, 3, 1), capacity = 3)
    problem541cap5 = FoxesProblem((5, 4, 1), capacity = 5)

    # Run the searches.
    # Each of the search algorithms should return a SearchSolution object,
    # even if the goal was not found. If goal not found, 'len()' of the path
    # in the solution object should be 0.

    print(bfs_search(problem331cap2))
    print(dfs_search(problem331cap2))
    print(ids_search(problem331cap2))

    print(bfs_search(problem331cap3))
    print(dfs_search(problem331cap3))
    print(ids_search(problem331cap3))

    print(bfs_search(problem541cap5))
    print(dfs_search(problem541cap5))
    print(ids_search(problem541cap5))

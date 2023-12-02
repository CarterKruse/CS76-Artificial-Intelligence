# SensorlessProblem.py
# A file defining the problem set-up, along with the goal state and successors method.
# Carter Kruse (September 27, 2023)

from Maze import Maze
from time import sleep
import random
import math

class SensorlessProblem:
    # Constructor
    def __init__(self, maze):
        self.maze = maze
        self.start_state = [] # The various possible (valid) robot locations, contained within a state.

        # Initially, every single legal position is added.
        for x in range(self.maze.width):
            for y in range(self.maze.height):
                if self.maze.is_floor(x, y):
                    self.start_state.append((x, y))    
    
    # Determine the successor states (as a list) for a given state.
        # Consider the valid moves from the current state and update the robot's position accordingly.
    def get_successors(self, state):
        # Initialize the list/set of successors, which starts out as empty.
            # A set is used to ensure that repeats are not allowed.
        successors_list = set([])

        # Enumerate the possible "moves" for the robot, according to the problem set-up.
        possible_moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Introduce randomness to allow for consecutive iterations to be independent of a deterministic outcome.
        random.shuffle(possible_moves)

        # Cycle through the list of possible moves.
        for move in possible_moves:
            # Creating the next state.
            next_state = set([])

            # Cycle through the list of coordinates in the state.
            for coordinate_pair in state:
                # Unpack the coordinate pair and move values.
                x, y = coordinate_pair
                dx, dy = move

                # Create a new x and y coordinate pair based on the transition.
                new_x, new_y = x + dx, y + dy

                # If the position is not a wall or out of bounds...
                if self.maze.is_floor(new_x, new_y):
                    # Add the new position to the set of possible states.
                    next_state.add((new_x, new_y))
                else:
                    # Otherwise, do not update the coordinate pair.
                        # Add the same position to the set of possible states.
                    next_state.add(coordinate_pair)
            
            # Add all the possible robot locations given an action.
            successors_list.add(tuple(next_state))
        
        return tuple(successors_list)

    # Test if the state is at the goal.
    def is_goal_state(self, state):
        # If the state space is singular, then the robot has been located.
        return len(state) == 1
    
    # Calculate the sensorless heuristic for the sensorless problem.
    def sensorless_heuristic(self, state):
        return len(state) - 1 # math.log2(len(state))
    
    def __str__(self):
        # You may add further information about the problem state (if necessary).
        string = "Blind Robot Problem: " + "Start State: " + str(self.start_state)
        return string
    
    # Given a sequence of states, (including robot turn), modify the maze and print it out.
        # (Be careful, this does modify the maze!)
    def animate_path(self, path):
        # Reset the robot locations in the maze.
        self.maze.robotloc = tuple(item for sublist in self.start_state for item in sublist)

        # Cycle through each state within the path.
        for state in path:
            # Print the problem set-up.
            print(str(self))

            # Update the locations of the robot.
            self.maze.robotloc = tuple(item for sublist in state for item in sublist)
            sleep(0.2)
            
            # Print the updated maze with the robot locations.
            print(str(self.maze))

# Test Code
    # Optional: Add to this to verify that the code works as expected.
if __name__ == "__main__":
    test_maze1 = Maze("sensorless1.maz")
    test_problem = SensorlessProblem(test_maze1)

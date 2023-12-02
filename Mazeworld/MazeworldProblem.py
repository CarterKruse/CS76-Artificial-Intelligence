# MazeworldProblem.py
# A file defining the problem set-up, along with the goal locations and successors method.
# Carter Kruse (September 27, 2023)

from Maze import Maze
from time import sleep
import random

class MazeworldProblem:
    # Constructor
    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_locations = goal_locations

        # The initial state is determined according to the maze characteristics.
        self.start_state = (0,) + tuple(maze.robotloc)

        # The number of robots is determined according to the goal locations.
        self.num_robots = len(goal_locations) // 2
    
    # Determine the successor states (as a list) for a given state.
        # Consider the valid moves from the current state and update the robot's position accordingly.
    def get_successors(self, state):
        # Initialize the list of successors, which starts out as empty.
        successors_list = []

        # Enumerate the possible "moves" for each of the robots, according to the problem set-up.
        possible_moves = [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]

        # Introduce randomness to allow for consecutive iterations to be independent of a deterministic outcome.
        random.shuffle(possible_moves)

        # Cycle through the list of possible moves.
        for move in possible_moves:
            # Creating the next state, according to the appropriate transition.
            next_state = (int((state[0] + 1) % self.num_robots),)

            # Creating a list to modify the position of a specific robot.
            state_list = list(state[1:])

            # The robot to move is given by 'state[0]', and modifications are given as follows.
            state_list[(2 * state[0])] += move[0]
            state_list[(2 * state[0]) + 1] += move[1]
            
            # Creating the next state based on the robot to move and the locations of the robots.
                # The first robot moves, then the second, and so on.
            next_state += tuple(state_list)

            # Check if a given state (determined by an initial state and transition) is safe.
            if self.is_safe(next_state):
                successors_list.append(next_state)
        
        return successors_list

    # Test if a given state is safe (before adding to successor list).
    def is_safe(self, state):
        robot_locations = set()

        for i in range(1, len(state), 2):
            # Wall/Floor Constraints: Check if the robots are on a floor space.
                # The boundary constraints are checked within the 'is_floor()' method.
            if not self.maze.is_floor(state[i], state[i + 1]):
                return False
            
            # Collision Constraints: Check if the robots are in collision with each other.
                # The 'has_robot()' method is not used, as this does not allow for no movement.
            if (state[i], state[i + 1]) not in robot_locations:
                robot_locations.add((state[i], state[i + 1]))
            else:
                return False
        
        return True
    
    # Test if the state is at the goal.
    def is_goal_state(self, state):
        if state[1:] == self.goal_locations:
            return True
        return False
    
    # Calculate the Manhattan heuristic for the Mazeworld problem.
    def manhattan_heuristic(self, state):
        total_distance = 0
        
        for i in range(1, len(state), 2):
            # Determine the position of the robot and it's associated goal position.
            robot_position = (state[i], state[i + 1])
            goal_position = (self.goal_locations[i - 1], self.goal_locations[i])

            # Add the Manhattan distance for a given robot to the total distance.
            total_distance += abs(robot_position[0] - goal_position[0]) + abs(robot_position[1] - goal_position[1])
        
        return total_distance
    
    def __str__(self):
        # You may add further information about the problem state (if necessary).
        string =  "Mazeworld Problem: " + "Start State: " + str(self.start_state) + " -- " \
            + "Goal State: " + str(self.goal_locations)
        return string
    
    # Given a sequence of states, (including robot turn), modify the maze and print it out.
        # (Be careful, this does modify the maze!)
    def animate_path(self, path):
        # Reset the robot locations in the maze.
        self.maze.robotloc = tuple(self.start_state[1:])

        # Cycle through each state within the path.
        for state in path:
            # Print the problem set-up.
            print(str(self))

            # Update the locations of the robot.
            self.maze.robotloc = tuple(state[1:])
            sleep(0.2)
            
            # Print the updated maze with the robot locations.
            print(str(self.maze))

# Test Code
    # Optional: Add to this to verify that the code works as expected.
if __name__ == "__main__":
    test_maze3 = Maze("maze3.maz")
    test_problem = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))

    print(test_problem.get_successors((0, 1, 0, 1, 2, 2, 1)))
    print(test_problem.is_safe((0, 1, 0, 1, 1, 2, 1)))
    print(test_problem.is_goal_state((0, 1, 4, 1, 3, 1, 2)))

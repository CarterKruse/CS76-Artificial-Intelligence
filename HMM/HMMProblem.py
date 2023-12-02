# HMMProblem.py
# A file defining the problem set up, along with testing for the HMM for 4x4 mazes.
# Carter Kruse (November 6, 2023)

from HMM import HMM
from Maze import Maze
from time import time

import random
import numpy as np
import matplotlib.pyplot as plt

class HMMProblem:
    # Constructor
    def __init__(self, maze, path):
        # Initialize the maze, possible colors, and maze_colors.
        self.maze = maze
        self.possible_colors = ['r', 'g', 'y', 'b']
        self.maze_colors = self.create_maze_colors()

        # Determine if the path is pre-set, or a path length is given.
        if type(path) is int:
            # Construct a random path using the path length.
            self.path = self.create_random_path(path)
        else:
            self.path = path
    
    def create_maze_colors(self):
        # Initialize an empty dictionary holding the colors of the map.
        maze_colors = {}

        # Cycle through the cells of the maze.
        for i in range(self.maze.width):
            for j in range(self.maze.height):
                # Check to make sure the location is a floor.
                if self.maze.is_floor(i, j):
                    # Update the maze color at the location to be a random choice.
                    maze_colors[(i, j)] = random.choice(self.possible_colors)
                else:
                    # Otherwise, the maze color is not relevant.
                    maze_colors[(i, j)] = '0'
        
        return maze_colors
    
    def create_random_path(self, path_length):
        # Initialize an empty path.
        path = []

        # Enumerate the possible moves of the robot, one for each time step.
        possible_moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Set the location of the robot, according to the maze.
        location = [self.maze.robotloc[0], self.maze.robotloc[1]]

        # Cycle through the pre-determined length of the path.
        for _ in range(path_length):
            # Select a random move from the choice of possible moves.
            move = random.choice(possible_moves)

            # Create a new location, according to the move.
            new_location = (location[0] + move[0], location[1] + move[1])
            
            # Check if the location is a floor.
            if test_maze.is_floor(new_location[0], new_location[1]):
                # Update the path, and the current location of the robot.
                path.append(new_location)
                location = new_location
            # Otherwise, the robot remains in the same place.
            else:
                path.append(tuple(location))
        
        return path
    
    def move_robot(self, new_location):
        # Check to make sure the location is a floor.
        if self.maze.is_floor(new_location[0], new_location[1]):
            # Update the robot location, according to the specified parameter.
            self.maze.robotloc[0], self.maze.robotloc[1] = new_location[0], new_location[1]
        
        # Determine the actual color of the maze at the given location.
        actual_color = self.maze_colors[self.maze.robotloc[0], self.maze.robotloc[1]]

        # Determine the other colors that are possible, beyond that that is the actual one.
        other_colors = [color for color in self.possible_colors if color != actual_color]

        # Simulate the sensor, by determining the sensor color according to a random value.
        sensor_color = None
        random_value = random.random()

        # The probability values are set in accordance to the problem set up.
        if random_value < 0.88:
            sensor_color = actual_color
        elif random_value < 0.92:
            sensor_color = other_colors[0]
        elif random_value < 0.96:
            sensor_color = other_colors[1]
        else:
            sensor_color = other_colors[2]
        
        # Return the actual color at the location, along with the sensor reading.
        return actual_color, sensor_color
    
    def solution(self):
        # Initialize the locations (maze), (actual) colors, and sensor readings.
        locations = [str(self.maze)]
        colors = '0'
        sensors = '0'

        # Cycle through each location in the path.
        for location in self.path:
            # Determine the actual and sensor color after the robot move.
            actual_color, sensor_color = self.move_robot(location)

            # Update the locations array with a string representation of the maze.
            locations.append(str(self.maze))

            # Add the actual and sensor colors to the arrays (given as strings).
            colors += actual_color
            sensors += sensor_color
        
        # Run the HMM algorithm on the maze, with the given sensors and maze colors.
        hmm = HMM(self.maze, sensors[1:], self.maze_colors)

        # Filtering Only
        start = time()
        filter_path = hmm.filter()
        filter_time = time() - start

        # Forward-Backward Smoothing
        start = time()
        smooth_path = hmm.smooth()
        smooth_time = time() - start

        # Initializing confidence arrays.
        filter_max_values = []
        smooth_max_values = []

        # Print the maze, readings, colors, and distributions.
        for i, distribution in enumerate(filter_path):
            print('Iteration ' + str(i))
            print(self.path[:i])
            print('----------')
            print('Actual Color: ' + colors[i])
            print('Sensor Color: ' + sensors[i])
            print()
            print('Robot Location: ')
            print(locations[i])
            print('Distribution: ')
            print(distribution)
            print()
            print('Smooth Distribution: ')
            print(smooth_path[i])
            print()

            # Append the maximum values of each 2D array.
            filter_max_values.append(distribution.max())
            smooth_max_values.append(smooth_path[i].max())
        
        ## BONUS 2 ##
        # Visualization
        plt.subplot(1, 2, 1)
        plt.imshow(filter_path[-1], cmap = 'OrRd', interpolation = 'nearest')
        plt.title('Filter')
        plt.xticks([])
        plt.yticks([])
        
        plt.subplot(1, 2, 2)
        plt.imshow(smooth_path[-1], cmap = 'OrRd', interpolation = 'nearest')
        plt.title('Smooth')
        plt.xticks([])
        plt.yticks([])
        
        plt.subplots_adjust(wspace = 0.5)
        plt.savefig('new_comparison.png')
        plt.show()

        plt.plot(filter_max_values, label = 'Filter')
        plt.plot(smooth_max_values, label = 'Smooth')
        plt.legend()
        plt.title('Confidence Values')
        plt.xlabel('Iteration')
        plt.ylabel('Confidence')

        plt.savefig('new_confidence_values.png')
        plt.show()
        
        ## BONUS 1 ##
        print('-----Time Analysis-----')
        print('Filtering Only: ' + str(filter_time))
        print('Forward-Backward Smoothing: ' + str(smooth_time))
        print()

# Test Code
    # Optional: Add to this to verify that the code works as expected.
if __name__ == '__main__':
    random.seed(0)

    test_maze = Maze('maze1.maz')
    test_problem = HMMProblem(test_maze, 12)

    # test_maze = Maze('maze1.maz')
    # path = [(1, 0), (1, 1), (1, 2), (2, 2), (1, 2), (1, 3)]
    # test_problem = HMMProblem(test_maze, path)

    # test_maze = Maze('maze2.maz')
    # path = [(1, 1), (1, 0), (1, 0), (1, 1), (1, 2), (1, 3), (1, 2)]
    # test_problem = HMMProblem(test_maze, path)

    ## BONUS 3 ##
    # test_maze = Maze('maze3.maz')
    # path = [(1, 0), (1, 1), (1, 2), (2, 2), (1, 2), (1, 3), (2, 3), (3, 3), (3, 4)]
    # test_problem = HMMProblem(test_maze, path)

    # test_maze = Maze('maze4.maz')
    # test_problem = HMMProblem(test_maze, 15)

    test_problem.solution()

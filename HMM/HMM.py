# HMM.py
# A file containing the filtering algorithm, along with the transition and sensor models.
# Carter Kruse (November 6, 2023)

import numpy as np

# HMM - Hidden Markov Model
    # Objective: Solve a Mazeworld problem using filtering and forward-backward smoothing.
class HMM:
    # Constructor
    def __init__(self, maze, sensors, maze_colors):
        # Initialize the maze, sensor readings, and colors.
        self.maze = maze
        self.sensors = sensors
        self.maze_colors = maze_colors

        # Construct a dictionary with the color frequency values.
        self.color_frequency = {'r': 0, 'g': 0, 'y': 0, 'b': 0}

        # Update the color frequency dictionary according to the maze.
        for color in maze_colors.values():
            if color != '0':
                self.color_frequency[color] += 1
    
    def initialize_state(self):
        # Initialize the state with an array of all zeros.
        state = np.zeros((self.maze.width, self.maze.height))

        # Update the array, according to certain constraints.
        for i in range(self.maze.width):
            for j in range(self.maze.height):
                # Check to make sure the location is a floor.
                if self.maze.is_floor(i, j):
                    # Determine the probability by the number of open positions.
                    state[j, i] = 1 / len(self.maze_colors)
        
        return state
    
    def filter(self):
        # Initialize the state.
        state = self.initialize_state()

        # Add the start state to the sequence.
        sequence = [np.flipud(state)]

        # Cycle through the sensor readings.
        for color in self.sensors:
            # Apply the transition, followed by the sensor model.
            state = self.apply_transition(state)
            state *= self.sensor_model(color)

            # Normalize the state, which represents a probability distribution.
            state = state / np.sum(state)

            # Add the state to the sequence.
            sequence.append(np.flipud(state))
        
        # Return the probability distributions given sensor readings.
        return sequence
    
    ## BONUS 1 ##
    def smooth(self):
        # Initialize the states.
        forward_state = self.initialize_state()
        backward_state = self.initialize_state()

        # Add the start states to the sequences.
        forward_sequence = [np.flipud(forward_state)]
        backward_sequence = [np.flipud(backward_state)]

        # Cycle through the sensor readings.
        for color in self.sensors:
            # Apply the transition, followed by the sensor model.
            forward_state = self.apply_transition(forward_state)
            forward_state *= self.sensor_model(color)

            # Normalize the state, which represents a probability distribution.
            forward_state = forward_state / np.sum(forward_state)

            # Add the state to the sequence.
            forward_sequence.append(np.flipud(forward_state))
        
        # Cycle through the sensor readings, in reverse order
        for color in self.sensors[::-1]:
            # Apply the sensor model, followed by the transition.
            backward_state *= self.sensor_model(color)
            backward_state = self.apply_transition(backward_state)

            # Normalize the state, which represents a probability distribution.
            backward_state = backward_state / np.sum(backward_state)

            # Add the state to the sequence.
            backward_sequence.append(np.flipud(backward_state))
        
        # Reverse the sequence, to consider iteration from 0 to n.
        backward_sequence.reverse()
        
        # Construct a new sequence to represent the smoothed distributions.
        sequence = []

        # Iterate through the states in the forward sequence.
        for i, state in enumerate(forward_sequence):
            # Apply the backward sequence values to the state.
            smooth_state = state * backward_sequence[i]

            # Normalize the state, which represents a probability distribution.
            smooth_state = smooth_state / np.sum(smooth_state)

            # Add the state to the sequence.
            sequence.append(smooth_state)
        
        # Return the forward-backward smoothed probability distributions given sensor readings.
        return sequence
    
    def apply_transition(self, state):
        # Reshape the state to be a (1, n^2) matrix.
        state = np.reshape(state, (1, self.maze.width * self.maze.height))

        # Use matrix multiplication to apply the transition model.
        state = np.matmul(state, np.transpose(self.transition_model()))

        # Reshape the state back to be an (n, n) matrix.
        state = np.reshape(state, (self.maze.width, self.maze.height))
        
        return state
    
    def sensor_model(self, color):
        # Construct an empty matrix to represent the sensor model.
        matrix = np.zeros((self.maze.width, self.maze.height))

        # Cycle through the cells of the maze.
        for i in range(self.maze.width):
            for j in range(self.maze.height):
                # Check to make sure the location is a floor.
                if self.maze.is_floor(i, j):
                    # Update the sensor model, according to whether the color matches.
                    if self.maze_colors[(i, j)] == color:
                        matrix[j, i] = 0.88 / self.color_frequency[color]
                    else:
                        matrix[j, i] = 0.04 / self.color_frequency[self.maze_colors[(i, j)]]
        
        # Return the probability matrix/distribution.
        return matrix
    
    def transition_model(self):
        # Construct an empty matrix to represent the transition model.
        matrix = np.zeros((self.maze.width * self.maze.height, self.maze.width * self.maze.height))
        
        # Cycle through the cells of the maze.
        for j in range(self.maze.height):
            for i in range(self.maze.width):
                # Determine the 'current' cell.
                current = self.maze.width * j + i

                # Compute the possible moves from a given location.
                moves = self.get_moves((i, j))

                # Iterate through the possible moves.
                for move in moves:
                    # Update the 'next' cell, according to each move.
                    next = self.maze.width * move[1] + move[0]

                    # Update the transition model, according to the 'current' and 'next' locations.
                    matrix[next, current] += 1 / len(moves)
        
        # Return the probability matrix/distribution.
        return matrix
    
    def get_moves(self, location):
        # Initialize an empty list of possible moves from a given location.
        moves_list = []

        # Enumerate the possible moves.
        possible_moves = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Cycle through all of the possible moves.
        for move in possible_moves:
            # Update the location, according to the original location and the move.
            new_location = (location[0] + move[0], location[1] + move[1])

            # Check if the location is a floor.
            if self.maze.is_floor(new_location[0], new_location[1]):
                moves_list.append(new_location)
            # Otherwise, do not move the robot.
            else:
                moves_list.append(tuple(location))
                
        return moves_list
    
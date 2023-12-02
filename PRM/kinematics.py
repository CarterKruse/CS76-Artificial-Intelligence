# kinematics.py
# Carter Kruse (November 14th)

import numpy as np
from heuristics import angular_distance
import matplotlib.pyplot as plt
from shapely.geometry import LineString, Polygon

# Forward Kinematics
def forward_kinematics(angles, lengths):
    # Initialize the points array, along with the (x, y) location.
    points = [[0.0, 0.0]]
    x, y = 0.0, 0.0
    
    # Cycle through the angles/lengths.
    for i in range(len(angles)):
        # Update the (x, y) location according to the angles.
        x += lengths[i] * np.cos(np.sum(angles[:i + 1]))
        y += lengths[i] * np.sin(np.sum(angles[:i + 1]))

        # Add the point to the list.
        points.append([x, y])
    
    # Return the list of points.
    return np.array(points)

# Is Collision
def is_collision(angles, lengths, obstacles):
    # Calculate the points according to the forward kinematics model.
    points = forward_kinematics(angles, lengths)

    # Construct a line string from the points.
    arm = LineString(points)
    
    # Cycle through the obstacles.
    for obstacle in obstacles:
        # Check if the line string intersects the obstacle.
        if arm.intersects(obstacle):
            return True
    
    return False

# Interpolation
def interpolation(vertex_1, vertex_2, num_points = 20):
    # Ensure the dimensions match.
    assert len(vertex_1) == len(vertex_2)

    # Determine the length of the vector.
    vertex_length = len(vertex_1)

    # Determine the direction of interpolation (circular).
    directions = [1 for _ in range(num_points)]

    # Cycle through the angles.
    for i in range(vertex_length):
        # Calculate the difference between the angles (mod 2pi).
        difference = (vertex_2[i] - vertex_1[i]) % (2 * np.pi)

        # Reverse the direction if the distance is far.
        if difference > np.pi:
            directions[i] = -1
    
    # Perform interpolation (linear/circular) along each dimension.
    interpolated_points = []

    # Cycle through the number of points.
    for k in range(num_points):
        # Initialize an empty list.
        l = []

        # Cycle through the angles.
        for i in range(vertex_length):
            # Construct the interpolated point by adding a piece of the angular distance (with direction).
            l.append((vertex_1[i] + directions[i] * angular_distance(vertex_1[i], vertex_2[i]) * (k / num_points)) % (2 * np.pi))
        
        # Add the list to the interpolated points.
        interpolated_points.append(tuple(l))
    
    # Return the interpolated points.
    return interpolated_points

## BONUS ##

# Compute Trajectory
def compute_trajectory(x, y, v, w, total_time, dt):
    # Determine the number of steps to take.
    num_steps = int(total_time / dt)

    # Initialize an empty path of points and times.
    path = []
    times = []

    # Cycle through the different time steps.
    for step in range(num_steps):
        path.append([x + v * step * dt * np.cos(w * step * dt),
                     y + v * step * dt * np.sin(w * step * dt)])
        times.append(step * dt)
    
    return path, times

# Plot Trajectory
def plot_trajectory(ax, path):
    # Extract the x and y coordinates.
    x_coordinates = [point[0] for point in path]
    y_coordinates = [point[1] for point in path]

    # Plot the path.
    plt.plot(x_coordinates, y_coordinates, marker = 'o', linestyle = '-', markersize = 5)

    # Titles & Labels
    plt.title('Path of Particle')
    plt.xlabel('X')
    plt.ylabel('Y')

    # Grid
    plt.grid(True)

    # Make the axes equal in units.
    plt.axis('equal')

def detect_collision(points, obstacles):
    # Construct a line string from the points.
    arm = LineString(points)
    
    # Cycle through the obstacles.
    for obstacle in obstacles:
        # Check if the line string intersects the obstacle.
        if arm.intersects(obstacle):
            return True
    
    return False

# Test Code
    # Optional: Add to this to verify that the code works as expected.
if __name__ == "__main__":
    # VALID
    angles = [0.1 * i for i in range(1, 5)]
    lengths = [1.0 for _ in range(4)]
    obstacles = [Polygon([(0.5, 2.0), (1.5, 0.5), (1.5, 2.0)]),
                 Polygon([(2.5, 0.2), (3.0, 0.5), (2.6, 0.8)])]
    
    print('Points: ' + str(forward_kinematics(angles, lengths)))
    print()
    print('Collision: ' + str(is_collision(angles, lengths, obstacles)))
    print()

    # INVALID
    angles = [0.05 * i for i in range(1, 5)]
    lengths = [1.0 for _ in range(4)]
    obstacles = [Polygon([(0.5, 2.0), (1.5, 0.5), (1.5, 2.0)]),
                 Polygon([(2.5, 0.2), (3.0, 0.5), (2.6, 0.8)])]
    
    print('Points: ' + str(forward_kinematics(angles, lengths)))
    print()
    print('Collision: ' + str(is_collision(angles, lengths, obstacles)))
    print()

    # Interpolation
    print('Interpolated Points: ' + str(interpolation([0.1, 0.2, 0.3, 0.4], [0.3, 0.2, 0.2, 0.4], 5)))
    print()

# multi_robot.py
# Carter Kruse (November 14th)

import numpy as np
import time
import matplotlib.pyplot as plt
from shapely.geometry import LineString

# Compute Trajectory
def compute_trajectory(x, y, v, w, total_time, dt):
    # Determine the number of steps to take.
    num_steps = int(total_time / dt)

    # Initialize an empty path of points and times.
    path = []

    # Cycle through the different time steps.
    for step in range(num_steps):
        # Add the corresponding points to the path.
        path.append([x + v * step * dt * np.cos(w * step * dt),
                     y + v * step * dt * np.sin(w * step * dt)])
    
    # Return the calculated path/trajectory.
    return path

# Plot Trajectory
def plot_trajectory(path):
    # Extract the x and y coordinates.
    x_coordinates = [point[0] for point in path]
    y_coordinates = [point[1] for point in path]

    # Plot the path.
    plt.plot(x_coordinates, y_coordinates, marker = 'o', linestyle = '-', markersize = 3)

    # Titles & Labels
    plt.title('Path of Particle')
    plt.xlabel('X')
    plt.ylabel('Y')

    # Grid
    plt.grid(True)

    # Make the axes equal in units.
    plt.axis('equal')

# Detect Collision
def detect_collision(points, obstacles):
    # Construct a line string from the points.
    arm = LineString(points)
    
    # Cycle through the obstacles.
    for obstacle in obstacles:
        # Check if the line string intersects the obstacle.
        if arm.intersects(obstacle):
            return True
    
    return False

# Moving Average
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size) / window_size, mode = 'valid')

# Plot Multiple
def plot_multiple():
    # Multi Robot (& Time Analysis)
    robot_paths = []
    times = []

    # Initialize the start time.
    start_time = time.time()

    i = 0
    while i < 1000:
        # Compute the trajectory, for a random (x, y), velocity, and angular velocity.
        path = compute_trajectory(x = np.random.uniform(-3, 3), y = np.random.uniform(-3, 3), v = np.random.uniform(-3, 3), w = np.random.uniform(0, 2 * np.pi), total_time = 1, dt = 0.1)
        
        # If there is not a collision with previous paths...
        if not detect_collision(path, robot_paths):
            i += 1

            ## Add the robot path to the list.
            robot_paths.append(LineString(path))

            # Plot the trajectory
            plot_trajectory(path)

            # Add the time to find a solution to the list.
            end_time = time.time()
            times.append(end_time - start_time)

            # Reset the start time.
            start_time = time.time()
    
    plt.show()
    return times

def time_analysis(times, window_size = 20):
    # Calculate the moving average.
    rolling_average = moving_average(times, window_size)
    
    # Plot the original data.
    plt.plot(times, color = 'blue', label = 'Original Data')

    # Plot the moving average.
    plt.plot(np.arange(window_size - 1, len(times)), rolling_average, color = 'red', label = f'Moving Average ({window_size} Points)')

    # Labels
    plt.xlabel('Iteration')
    plt.ylabel('Time')
    plt.legend()

    plt.show()

# Test Code
    # Optional: Add to this to verify that the code works as expected.
if __name__ == "__main__":
    # Simple Version (1 Robot)
    path = compute_trajectory(x = 0, y = 0, v = 1, w = np.pi / 4, total_time = 1, dt = 0.1)
    print("Path: ", path)
    print()

    # Show the trajectory of the robot in space.
    plot_trajectory(path)
    plt.show()

    times = plot_multiple()
    time_analysis(times)

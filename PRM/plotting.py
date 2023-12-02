# plotting.py
# Carter Kruse (November 14th)

from kinematics import forward_kinematics, is_collision
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# Plot Chain
def plot_chain(angles, lengths):
    # Calculate the points according to the forward kinematics model.
    points = forward_kinematics(angles, lengths)
    x, y = zip(*points)

    # Display the chain, with the linkage points.
    plt.plot(x, y, color = 'black')
    plt.scatter(x, y, color = 'black', s = 7)

# Plot Obstacles
def plot_obstacles(obstacles):
    # Cycle through the obstacles.
    for obstacle in obstacles:
        # Plot the exterior of the obstacle (red).
        x, y = obstacle.exterior.xy
        plt.plot(x, y, color = 'red')

# Show Plot
def show_plot(ax, angles, lengths, obstacles):
    # Check if there is a collision, update the background color.
    if is_collision(angles, lengths, obstacles):
        ax.set_facecolor('lightcoral')
    else:
        ax.set_facecolor('white')
    
    # Plot the chain and obstacles.
    plot_chain(angles, lengths)
    plot_obstacles(obstacles)

    # Make the axes equal in units.
    plt.axis('equal')

# Test Code
    # Optional: Add to this to verify that the code works as expected.
if __name__ == "__main__":
    # VALID
    angles = [0.1 * i for i in range(1, 5)]
    lengths = [1.0 for _ in range(4)]
    obstacles = [Polygon([(0.5, 2.0), (1.5, 0.5), (1.5, 2.0)]),
                 Polygon([(2.5, 0.2), (3.0, 0.5), (2.6, 0.8)])]
    
    
    ax = plt.axes()
    show_plot(ax, angles, lengths, obstacles)
    plt.show()

    # INVALID
    angles = [0.05 * i for i in range(1, 5)]
    lengths = [1.0 for _ in range(4)]
    obstacles = [Polygon([(0.5, 2.0), (1.5, 0.5), (1.5, 2.0)]),
                 Polygon([(2.5, 0.2), (3.0, 0.5), (2.6, 0.8)])]
    
    
    ax = plt.axes()
    show_plot(ax, angles, lengths, obstacles)
    plt.show()

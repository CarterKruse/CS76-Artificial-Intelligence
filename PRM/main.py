# main.py
# Carter Kruse (November 14th)

import numpy as np
import random
import time

from GraphProblem import GraphProblem
from kinematics import interpolation
from plotting import show_plot
from graph import add_vertex, construct_vertex_set, construct_edge_set

from uninformed_search import bfs_search
from bidirectional_search import bidirectional_search
from astar_search import astar_search

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from shapely.geometry import Polygon
import scipy.spatial

# Constants
R = 4
LENGTHS = [1.0 for _ in range(R)]
OBSTACLES = []

APPROX_NEIGHBORS = False

# Randomization
random.seed(0)
np.random.seed(0)

# Initialize
def initialize():
    # Define the x and y bounds with half-step intervals.
    x_bounds = [i for i in np.arange(-R, R, 0.5)]
    y_bounds = [i for i in np.arange(-R, R, 0.5)]

    # Create a series of 4 * R random obstacles.
    for _ in range(4 * R):
        # Generate random x and y values within the specified bounds.
        x = random.choice(x_bounds)
        y = random.choice(y_bounds)

        # Check to make sure the obstacles are not at the starting location.
        if (x, y) == (0.0, 0.0) or (x + 0.5, y) == (0.0, 0.0) or (x + 0.25, y + 0.5) == (0.0, 0.0):
            continue

        # Create a polygon using the specified form of a triangle.
        polygon = Polygon([(x, y), (x + 0.5, y), (x + 0.25, y + 0.5)])
        OBSTACLES.append(polygon)

# Build Graph
def build_graph(graph, samples, start_state, goal_state):
    # Initialize the start time.
    start_time = time.time()

    # Construct the vertex set, according to the specifications.
    construct_vertex_set(graph, samples, num_samples = 300 * R - 200, size = R, lengths = LENGTHS, obstacles = OBSTACLES)

    # Add the start state and goal state as vertices.
    add_vertex(graph, start_state, samples)
    add_vertex(graph, goal_state, samples)

    # Construct a spatial tree for the approximate nearest neighbors.
    tree = scipy.spatial.KDTree(samples)

    # Construct the edge set, according to the specifications.
    construct_edge_set(graph, samples, tree, lengths = LENGTHS, obstacles = OBSTACLES, k_nearest = 30, approx = APPROX_NEIGHBORS)

    # Calculate the end time.
    end_time = time.time()

    print()
    print('Time (Build Graph): ' + str(end_time - start_time))

# Find Solution
def find_solution(graph, start_state, goal_state):
    # Create the problem, with the graph, start state, and goal state.
    graph_problem = GraphProblem(graph, start_state, goal_state)

    # Initialize the start time.
    start_time = time.time()

    # solution = bfs_search(graph_problem)
    # solution = bidirectional_search(graph_problem)
    solution = astar_search(graph_problem, graph_problem.angular_heuristic)

    # Calculate the end time.
    end_time = time.time()

    print('Time (Search): ' + str(end_time - start_time))
    print()

    # Print the solution.
    print(solution)

    # Initalize the path.
    path = []

    # Construct the path, by interpolation between points.
    for i in range(len(solution.path) - 1):
        path.extend(interpolation(solution.path[i], solution.path[i + 1]))

    # Add the goal state to the solution path.
    path.append(goal_state)

    return path

# Show Result
def show_result(path):
    # Create a figure and axis for the animation.
    fig, ax = plt.subplots()

    # Create the animation.
    animation = FuncAnimation(fig, update, fargs = (ax, path), frames = len(path), interval = 100)

    # Show the plot.
    plt.show()

# Update
def update(frame, ax, path):
    ax.clear()

    # Determine the angles for the current frame.
    angles = path[frame]

    # Update the plot for each frame of the animation.
    show_plot(ax, angles, LENGTHS, OBSTACLES)

## MAIN ALGORITHM ##

initialize()
graph = {}
samples = []

# Set the start and goal states, representing a configuration of angles.
if R == 2:
    start_state = tuple([0.5, 5.0])
    goal_state = tuple([2.0, 1.0])
elif R == 3:
    start_state = tuple([1.0, 0.5, 5.0])
    goal_state = tuple([4.0, 1.0, 1.0])
elif R == 4:
    start_state = tuple([0.1, 0.2, 0.3, 0.4])
    goal_state = tuple([5.0, 1.0, 5.0, 0.5])
else:
    print('Use a different R value.')
    exit(0)

build_graph(graph, samples, start_state, goal_state)
path = find_solution(graph, start_state, goal_state)
show_result(path)

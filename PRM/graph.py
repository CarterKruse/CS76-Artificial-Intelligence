# graph.py
# Carter Kruse (November 14th)

import numpy as np
from kinematics import is_collision, interpolation
from heuristics import total_angular_distance
from plotting import show_plot

import matplotlib.pyplot as plt
from shapely.geometry import Polygon

# Generate Random Configurations
def generate_random_configuration(size):
    # Construct a random configuration of angles with a given size.
    angles = np.random.uniform(0, 2 * np.pi, size)

    # Return the angles.
    return angles

# Add Vertex
def add_vertex(graph, vertex, samples):
    # If the vertex is not the in the graph...
    if vertex not in graph:
        # Add the vertex to the graph.
        graph[vertex] = set()

        # Add the vertex to the samples.
        samples.append(vertex)

# Add Edge
def add_edge(graph, vertex_1, vertex_2):
    # If both vertices are in the graph...
    if vertex_1 in graph and vertex_2 in graph:
        # If the vertices are not equivalent.
        if vertex_1 != vertex_2:
            # Add an edge between the vertices.
            graph[vertex_1].add(vertex_2)
            graph[vertex_2].add(vertex_1)

# Construct Vertex Set
def construct_vertex_set(graph, samples, num_samples, size, lengths, obstacles):
    i = 0
    # Construct the vertex set of the graph.
    while i < num_samples:
        # Create a random configuration of angles.
        angles = generate_random_configuration(size)

        # Check to make sure there is not a collision for the configuration.
        if not is_collision(angles, lengths, obstacles):
            # Convert the angles to a tuple to be placed in the dictionary.
            vertex = tuple(angles)

            # Add the vertex to the graph.
            add_vertex(graph, vertex, samples)
            i += 1
            
# Construct Edge Set
def construct_edge_set(graph, samples, tree, lengths, obstacles, k_nearest, approx):
    # Construct the edge set of the graph.
    for vertex in graph:
        if not approx:
            # Initialize the dictionary of vertex distances.
            vertex_distances = {}

            # Cycle through vertices of the graph.
            for v in graph:
                # Check if two vertices are the same.
                if v != vertex:
                    # Determine the total angular distance.
                    vertex_distances[v] = total_angular_distance(v, vertex)
            
            # Sort the vertices by the total angular distance (lambda function).
            sorted_vertices = sorted(vertex_distances.keys(), key = lambda v: vertex_distances[v])

            # Determine the K nearest vertices.
            for i in range(k_nearest):
                # Make sure there is a safe path between the vertices.
                if is_safe(lengths, obstacles, vertex, sorted_vertices[i]):
                    # Add an edge to the graph corresponding to the pairing.
                    add_edge(graph, vertex, sorted_vertices[i])
        else:
            # Use the SciPy implementation for approximate nearest neighbors.
            distances, neighbors = tree.query([vertex], k = k_nearest + 1, distance_upper_bound = np.inf)

            # Exclude the vertex itself.
            neighbors = neighbors[0][1:]

            # Cycle through the approximate K nearest neighbors.
            for n in neighbors:
                # Determine the vertex according to the samples.
                neighbor = samples[n]

                # Make sure there is a safe path between the vertices.
                if is_safe(lengths, obstacles, vertex, neighbor):
                    # Add an edge to the graph corresponding to the pairing.
                    add_edge(graph, vertex, neighbor)

# Is Safe
def is_safe(lengths, obstacles, vertex_1, vertex_2):
    # Cycle through the points in the interpolation between vertices.
    for point in interpolation(vertex_1, vertex_2):
        # Check if there is a collision with the obstacles.
        if is_collision(point, lengths, obstacles):
            return False
    
    return True

# Test Code
    # Optional: Add to this to verify that the code works as expected.
if __name__ == "__main__":
    num_segments = 4

    angles_1 = generate_random_configuration(num_segments)
    angles_2 = generate_random_configuration(num_segments)

    print()
    print('Random Configuration #1: ' + str(angles_1))
    print('Random Configuration #2: ' + str(angles_2))
    print()
    
    lengths = [1.0 for _ in range(num_segments)]
    obstacles = [Polygon([(0.5, 2.0), (1.5, 0.5), (1.5, 2.0)]),
                Polygon([(2.5, 0.2), (3.0, 0.5), (2.6, 0.8)])]
    
    print('Safe: ' + str(is_safe(lengths, obstacles, angles_1, angles_2)))
    print()
    
    ax = plt.axes()
    show_plot(ax, angles_1, lengths, obstacles)
    plt.show()

    ax = plt.axes()
    show_plot(ax, angles_2, lengths, obstacles)
    plt.show()
    
# heuristics.py
# Carter Kruse (November 14th)

import numpy as np

# Angular Distance
def angular_distance(theta_1, theta_2):
    # Calculate the angular distance between two angles (in radians).
    distance = abs(theta_1 - theta_2) % (2 * np.pi)

    # Return the shortest distance (circular).
    return min(distance, 2 * np.pi - distance)

# Total Angular Distance
def total_angular_distance(angles_1, angles_2):
    total_distance = 0

    # Calculate the angular distance for each set of angles.
    for i in range(len(angles_1)):
        total_distance += angular_distance(angles_1[i], angles_2[i])
    
    # Return the total combined angular distance.
    return total_distance

# Test Code
    # Optional: Add to this to verify that the code works as expected.
if __name__ == "__main__":
    print('Angular Distance: ' + str(angular_distance(1, 5)))
    print('Total Angular Distance: ' + str(total_angular_distance([0.1, 0.2, 0.3, 0.4], [0.3, 0.2, 0.2, 0.4])))
    print()

# Mazeworld
### Carter Kruse (September 27, 2023)

### README
The following provides instructions on how to run the code.

### Mulit-Robot Coordination
To implement A* search for the Mazeworld Problem (using a null heuristic and a Manhattan heuristic), run `python3 test_mazeworld.py`. This will output the results and create a terminal/console GUI.

### Sensorless Problem (Blind Robot, Pacman Physics)
To implement A* search for the Sensorless Problem (using a null heuristic and a sensorless heuristic), run `python3 test_sensorless.py`. This will output the results and create a terminal/console GUI.

The aim is to find the state of a sensorless robot in the fewest possible moves.

### Comments
The files `test_mazeworld.py` and `test_sensorless.py` may be modified (as desired) to run according to different mazes (or state configurations).

The mazes are written in ASCII text, which is handled by the `Maze.py` file. The maze files should be in the same folder as the test script.

A* search is generalized to allow for any search problem (in this case, MazeworldProblem and SensorlessProblem), along with a heuristic of choice.

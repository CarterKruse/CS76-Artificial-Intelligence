# PRM
### Carter Kruse (November 14, 2023)

### README
The following provides instructions on how to run the code.

### PRM
To implement the probabilistic road map (PRM) for various problems, run `python3 main.py`. This will output the reuslt and create an animation using `matplotlib`.

### Comments
The `main.py` file may be modified (as desired) to run according to different configurations, including the number of segments in the chain (`R`), the lengths of the segments, whether *approximate* K neighbors is used, the obstacles in the environment, the start/goal states, etc.

Please read the file carefully before making changes, as this may drastically impact the results of the program.

---

The files `astar_search.py`, `bidirectional_search.py`, `GraphProblem.py`, `SearchSolution.py`, and `uninformed_search.py` are used as dependencies for the `main.py` script, and have no testing code.

The files `graph.py`, `heurisitcs.py`, `kinematics.py`, and `plotting.py` are used as dependencies for the `main.py` script, though testing code is provided in these files. If you wish to test any of the files, please run `python3 [filename]`.

The `multi_robot.py` file is a bonus file that is to be considered for extra credit, which is outlined in the report.

### Extra
*IMPORTANT* - The bonus files that are to be considered for extra credit points are outlined in the report, and included within the primary assignment.

# Sudoku
### Carter Kruse (October 24, 2023)

### README
The following provides instructions on how to run the code.

### Sudoku
To implement the SAT solver (using CNF), run `python3 solve.py`. This will output the results and create a terminal/console GUI.

### Comments
The file `solve.py` may be modified (as desired) to run according to the different algorithms. To display the solution to the Sudoku problem uncomment the following line:

```python
display_sudoku_solution(sol_file_name)
```

To change the SAT problem, modify the `puzzle_name` accordingly. To update the `p_value` and `max_flips` parameters, along with the algorithm type (`gsat` or `walksat`), modify the following line. The `h_value` is used for an advanced algorithm, set it to 0 to maintain the standard algorithm.

```python
result = sat.sat(p_value, max_flips, algo, h_value)
```

### Extra
*IMPORTANT* - The bonus files that are to be considered for extra credit points are outlined in the report, and included within the primary assignment.

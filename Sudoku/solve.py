# solve.py
# Solves a SAT problem using CNF.
# Carter Kruse (October 24, 2023)

from Sudoku import Sudoku
from SAT import SAT
from datetime import datetime
import random

def display_sudoku_solution(file_name):
    test_sudoku = Sudoku()
    test_sudoku.read_solution(file_name)
    print(test_sudoku)

if __name__ == '__main__':
    # For testing, always initialize the pseudo-random number generator.
    random.seed(1) # This outputs the same sequence of values.

    start_time = datetime.now()
    
    # Options: all_cells, map_coloring, one_cell, puzzle1, puzzle1_modified, puzzle2, puzzle2_modified,
        # queens, resolution, rows_and_cols, rows, rules
    puzzle_name = 'data/rules'
    cnf_file_name = puzzle_name + '.cnf'
    sol_file_name = puzzle_name + '.sol'

    sat = SAT(cnf_file_name)
    result = sat.sat(p_value = 0.3, max_flips = 100000, algo = 'walksat', h_value = 0)

    if result:
        sat.write_solution(sol_file_name)
        display_sudoku_solution(sol_file_name)
    
    print('Time: ' + str(datetime.now() - start_time))

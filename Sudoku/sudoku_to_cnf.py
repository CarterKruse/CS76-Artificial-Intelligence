# sudoku_to_cnf.py
# Converts a standard Sudoku board to CNF form.
# Carter Kruse (October 24, 2023)

from Sudoku import Sudoku
import sys

if __name__ == '__main__':
    test_sudoku = Sudoku()

    test_sudoku.load(sys.argv[1])
    print(test_sudoku)

    puzzle_name = sys.argv[1][:-4]
    cnf_file_name = puzzle_name + '.cnf'

    test_sudoku.generate_cnf(cnf_file_name)
    print('Output File: ' + cnf_file_name)

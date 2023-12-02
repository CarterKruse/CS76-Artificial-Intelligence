# CSP
### Carter Kruse (October 15, 2023)

### README
The following provides instructions on how to run the code.

### CSP
To implement the constraint satisfaction for various problems, run `python3 map_color.py`, `python3 circuit_board.py`, or `python3 usa.py`. This will output the results and create a terminal/console GUI.

### Comments
The file `n_queens.py` may be modified (as desired) to run according to a different size of chessboard, along with the corresponding number of queens.

---

The file `circuit_board.py` may be modified (as desired) to run according to the different components and size of the circuit board. The following provides an example

```pseudo
components = [['aaa', 'aaa'],
             ['bbbbb', 'bbbb.'],
             ['cc', 'cc', 'cc'],
             ['eeeeee.'],
             ['.d', 'dd']]
n, m = 10, 3
```

The parameters `n` and `m` are used to specify the width and height of the board, respectively. The components are designed from a base layer up, and thus each section must be the same length. In this case, `['bbbbb', 'bbbb.']` and `['.d', 'dd']` correspond to the non-rectangular components

```pseudo
bbbb.    dd
bbbbb    .d
```

### Extra
*IMPORTANT* - The bonus files that are to be considered for extra credit points are outlined in the report, and included within the primary assignment.

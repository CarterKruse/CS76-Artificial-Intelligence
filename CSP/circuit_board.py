# circuit_board.py
# Carter Kruse (October 15, 2023)

from CSP import CSP
import time

class circuit_board:
    def __init__(self, n, m, components):
        # set the width, height, and components
        self.width = n
        self.height = m
        self.components = components

        # set the domain, according to the problem set-up
        self.domain = {}
        for var in range(len(components)):
            # initialize an empty list of locations
            locations = []

            # cycle through the possible x, y locations
            for x in range(self.width - len(self.components[var][0]) + 1):
                for y in range(self.height - len(self.components[var]) + 1):
                    locations.append((x, y))

            self.domain[var] = locations
        
        # set the binary constraints in a graph
        self.graph = {}
        for i in range(len(components)):
            self.graph[i] = [j for j in range(len(components)) if j != i]

        self.domain_copy = self.domain

    def is_consistent(self, value, var, assignment, csp):
        # create a grid to keep track of overlapping components
        grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

        # cycle through the variables in assignment
        for variable in assignment:
            # extract the x, y coordinates
            x_start, y_start = assignment[variable]

            # cycle through the x, y locations
            for y in range(y_start, y_start + len(self.components[variable])):
                for x in range(x_start, x_start + len(self.components[variable][0])):
                    # determine the character at a given location
                    character = self.components[variable][y - y_start][x - x_start]

                    # handle the case where a character is not the empty space
                    if character != '.':
                        grid[self.height - y - 1][x] += 1

                        if grid[self.height - y - 1][x] > 1:
                            return False

        return True

    def show_result(self, assignment):
        # print the result
        grid = []
        
        # cycle through the height, width
        for _ in range(self.height):
            row = []
            for _ in range(self.width):
                row.append('.')
            
            grid.append(row)
        
        # # # # #

        # cycle through the variables in assignment
        for variable in assignment:
            # extract the x, y coordinates
            x_start, y_start = assignment[variable]

            # cycle through the x, y locations
            for y in range(y_start, y_start + len(self.components[variable])):
                for x in range(x_start, x_start + len(self.components[variable][0])):
                    # determine the character at a given location
                    character = self.components[variable][y - y_start][x - x_start]

                    # handle the case where a character is not the empty space
                    if character != '.':
                        grid[self.height - y - 1][x] = character
        
        # cycle through the height, width
        for j in range(self.height):
            for i in range(self.width):
                # display the grid
                print(grid[j][i], end = '')
            print()

if __name__ == '__main__':
    components = [['aaa', 'aaa'],
                  ['bbbbb', 'bbbbb'],
                  ['cc', 'cc', 'cc'],
                  ['eeeeeee']]
    n, m = 10, 3
    
    for inference in [True, False]:
        for MRV in [True, False]:
            for LCV in [True, False]:
                print('Inference: ' + str(inference) + ' -- MRV: ' + str(MRV) + ' -- LCV: ' + str(LCV))

                csp = circuit_board(n, m, components)
                search = CSP(inference, MRV, LCV)

                start = time.time()
                solution = search.backtracking_search(csp)
                end = time.time()

                print()
                print('Solution: ' + str(solution))
                print('(Time: {:.3g} Seconds)'.format(end - start))
                print()
                if solution is not None:
                    csp.show_result(solution)
                    print()

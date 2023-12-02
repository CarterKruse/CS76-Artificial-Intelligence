# n_queens.py
# Carter Kruse (October 15, 2023)

from CSP import CSP
import time

class n_queens:
    def __init__(self, n):
        # set the number of queens
        self.n = n

        # set the domain, according to the problem set-up
        self.domain = {}
        for var in range(self.n):
            self.domain[var] = [(i, j) for i in range(self.n) for j in range(self.n)]
        
        # set the binary constraints in a graph
        self.graph = {}
        for i in range(self.n):
            self.graph[i] = [j for j in range(self.n) if j != i]

        self.domain_copy = self.domain
    
    def is_consistent(self, value, var, assignment, csp):
        # cycle through the neighbors of a variable, according to the graph
        for neighbor in csp.graph[var]:
            # check if the position of a queen is not appropriate
            if neighbor in range(len(assignment) - 1) and any(val == value for val in self.attacked_positions(assignment[neighbor])):
                return False
        
        return True
    
    def attacked_positions(self, value):
        # create a set of potential positions
        potential = set()

        # extract the x, y coordinates
        x, y = value

        # horizontal, vertical constraints
        for i in range(self.n):
            potential.add((x, i))
            potential.add((i, y))
        
        # diagonal constraints
        for i in range(self.n):
            potential.add((x - i, y - i))
            potential.add((x - i, y + i))
            potential.add((x + i, y - i))
            potential.add((x + i, y + i))
        
        # create a list of attacked (valid) locations
        attacked = []

        # cycle through the positions
        for position in potential:
            # check the bounds of the position, according to the chessboard
            if position[0] >= 0 and position[0] < self.n and position[1] >= 0 and position[1] < self.n:
                attacked.append(position)

        return attacked
    
    def show_result(self, assignment):
        # print the result
        for j in range(self.n):
            for i in range(self.n):
                if (i, j) in assignment.values():
                    print('Q', end = '')
                else:
                    print('.', end = '')
            print()

if __name__ == '__main__':
    for inference in [True, False]:
        for MRV in [True, False]:
            for LCV in [True, False]:
                print('Inference: ' + str(inference) + ' -- MRV: ' + str(MRV) + ' -- LCV: ' + str(LCV))

                csp = n_queens(6)
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

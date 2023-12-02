# map_color.py
# Carter Kruse (October 15, 2023)

from CSP import CSP
import time

class map_color:
    def __init__(self):
        # set the domain, according to the problem set-up
        self.domain = {}
        for var in range(7):
            self.domain[var] = [1, 2, 3]
        
        # set the binary constraints in a graph
        self.graph = {0: [1, 2],
                      1: [0, 2, 3],
                      2: [0, 1, 3, 4, 5],
                      3: [1, 2, 4],
                      4: [2, 3, 5],
                      5: [2, 4],
                      6: []}
        
        # dictionaries used for final output
        self.territory = ['WA', 'NT', 'SA', 'Q', 'NSW', 'V', 'T']
        self.color = {1: 'Red', 2: 'Green', 3: 'Blue'}

        self.domain_copy = self.domain
    
    def is_consistent(self, value, var, assignment, csp):
        # cycle through the neighbors of a variable, according to the graph
        for neighbor in csp.graph[var]:
            # check if the colors are the same
            if neighbor in range(len(assignment) - 1) and assignment[neighbor] == value:
                return False
        
        return True
    
    def show_result(self, assignment):
        # print the result
        for var in assignment:
            print(str(self.territory[var]) + ': ' + str(self.color[assignment[var]]))

if __name__ == '__main__':
    for inference in [True, False]:
        for MRV in [True, False]:
            for LCV in [True, False]:
                print('Inference: ' + str(inference) + ' -- MRV: ' + str(MRV) + ' -- LCV: ' + str(LCV))
                
                csp = map_color()
                search = CSP(inference, MRV, LCV)

                start = time.time()
                solution = search.backtracking_search(csp)
                # solution = search.min_conflicts_search(csp)
                end = time.time()

                print()
                print('Solution: ' + str(solution))
                print('(Time: {:.3g} Seconds)'.format(end - start))
                print()
                if solution is not None:
                    csp.show_result(solution)
                    print()
    
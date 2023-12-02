# cs1_sections.py
# Carter Kruse (October 15, 2023)

from CSP import CSP
import time
import random

class cs1_sections:
    def __init__(self):
        # initialize the random seed
        random.seed(0)

        # set the times and leaders
        self.times = ['M 4:00', 'M 5:00', 'M 6:00', 'T 7:00', 'W 12:30', 'F 5:00']
        self.leaders = [['Leader' + str(i)] + random.sample(self.times, random.randint(1, len(self.times))) for i in range(6)]

        # set the domain, according to the problem set-up
        self.domain = {}
        for leader in self.leaders:
            self.domain[leader[0]] = leader[1:]
        
        # set the binary constraints in a graph
        self.graph = {}
        for i in self.domain:
            self.graph[i] = [j for j in self.domain if j != i]
        
        self.domain_copy = self.domain
    
    def is_consistent(self, value, var, assignment, csp):
        # cycle through the neighbors of a variable, according to the graph
        for neighbor in csp.graph[var]:
            # check if the times are the same
            if neighbor in assignment and assignment[neighbor] == value:
                return False
        
        return True
    
    def show_result(self, assignment):
        # print the result
        for var in assignment:
            print(str(var) + ': ' + str(assignment[var]))

if __name__ == '__main__':
    for inference in [True, False]:
        for MRV in [True, False]:
            for LCV in [True, False]:
                print('Inference: ' + str(inference) + ' -- MRV: ' + str(MRV) + ' -- LCV: ' + str(LCV))
                
                csp = cs1_sections()
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
    
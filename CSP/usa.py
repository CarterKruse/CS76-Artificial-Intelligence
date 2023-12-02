# usa.py
# Carter Kruse (October 15, 2023)

from CSP import CSP
import time
import ast

class usa:
    def __init__(self):
        # set the domain, according to the problem set-up
        self.domain = {}
        for var in range(51):
            self.domain[var] = [1, 2, 3, 4]
        
        # open the file
        with open('usa.txt', 'r') as file:
            # read the contents
            file_content = file.read()

            try:
                # set the binary constraints in a graph
                self.graph = ast.literal_eval(file_content)

                # handle the case where the graph is not a dictionary
                if not isinstance(self.graph, dict):
                    self.graph = None
                    raise ValueError('The content of the file is not a dictionary.')
            
            # handle the case where there is an error loading the data
            except (SyntaxError, ValueError) as error:
                self.graph = None
                print('Error loading data. ' + str(error))
        
        # dictionaries used for final output
        self.state = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
        self.color = {1: 'Red', 2: 'Green', 3: 'Blue', 4: 'Yellow'}

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
            print(str(self.state[var]) + ': ' + str(self.color[assignment[var]]))

if __name__ == '__main__':
    for inference in [True, False]:
        for MRV in [True, False]:
            for LCV in [True, False]:
                print('Inference: ' + str(inference) + ' -- MRV: ' + str(MRV) + ' -- LCV: ' + str(LCV))

                csp = usa()
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
    
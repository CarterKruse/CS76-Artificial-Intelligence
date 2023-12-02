# SearchSolution.py
# Designed to format the output of search, for a given problem.
# Carter Kruse (September 27, 2023)

class SearchSolution:
    def __init__(self, problem, search_method):
        self.problem_name = str(problem)
        self.search_method = search_method
        self.path = []
        self.nodes_visited = 0
        self.cost = 0

    def __str__(self):
        string = "----\n\n"
        string += "{:s}\n"
        string += "Attempted with search method {:s}\n"

        if len(self.path) > 0:
            string += "Number of Nodes Visited: {:d}\n"
            string += "Solution Length: {:d}\n"
            string += "Cost: {:d}\n"
            string += "Path: {:s}\n"

            string = string.format(self.problem_name, self.search_method, self.nodes_visited, len(self.path), self.cost, str(self.path))
        else:
            string += "No solution found after visiting {:d} nodes.\n"
            string = string.format(self.problem_name, self.search_method, self.nodes_visited)

        return string

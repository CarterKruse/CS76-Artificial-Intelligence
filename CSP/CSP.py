# CSP.py
# Carter Kruse (October 15, 2023)

from collections import deque
import random

class CSP:
    def __init__(self, inference, MRV, LCV):
        self.inference = inference
        self.MRV = MRV
        self.LCV = LCV
        random.seed(0)
    
    # function BACKTRACKING_SEARCH(csp) returns a solution, or failure
    def backtracking_search(self, csp):
        # return BACKTRACK({ }, csp)
        return self.backtrack({}, csp)
    
    # function BACKTRACK(assignment, csp) returns a solution, or failure
    def backtrack(self, assignment, csp):
        # if assignment is complete then return assignment
        if self.is_complete(assignment, csp):
            return assignment
        
        # var ← SELECT-UNASSIGNED-VARIABLE(csp)
        var = self.MRV_heuristic(assignment, csp)

        # for each value in ORDER-DOMAIN-VALUES(var, assignment, csp) do
        for value in self.LCV_heuristic(var, assignment, csp):
            # add variable to assignment
            assignment[var] = value
            
            # if value is consistent with assignment then
            if csp.is_consistent(value, var, assignment, csp):
                # add {var = value} to assignment
                assignment[var] = value

                # inferences ← INFERENCE(csp, var, assignment)
                inferences = self.AC_3(csp, var, assignment)

                # if inferences  ̸= failure then
                if inferences != False:
                    # result ← BACKTRACK(assignment, csp)
                    result = self.backtrack(assignment, csp)

                    # if result  ̸= failure then
                    if result != None:
                        # return result
                        return result
            
            # remove {var = value} and inferences from assignment
            del assignment[var]
            self.recover_domain(assignment, csp)
        
        # return failure
        return None
    
    # function IS_COMPLETE(assignment, csp) returns false the assignment is complete and true otherwise
    def is_complete(self, assignment, csp):
        return len(assignment) == len(csp.graph)
    
    # function RECOVER_DOMAIN(assignment, csp) reverts the domain vars not in the assignment
    def recover_domain(self, assignment, csp):
        for var in csp.graph:
            if var not in assignment:
                csp.domain[var] = csp.domain_copy[var]
    
    # function AC_3(csp, Yi, assignment) returns false if an inconsistency is found and true otherwise
    def AC_3(self, csp, Yi, assignment):
        if self.inference == False:
            return True
        
        # queue ← a queue of arcs, initially all the arcs in csp
        arcs = deque()
        for Yj in csp.graph[Yi]:
            if Yj not in assignment:
                arcs.append((Yi, Yj))
        
        # while queue is not empty do
        while len(arcs) != 0:
            # (Xi, Xj) ← POP(queue)
            Xi, Xj = arcs.popleft()

            # if REVISE(csp, Xi, Xj) then
            if self.revise(csp, Xi, Xj):
                # if size of Di = 0 then return false
                if len(csp.domain[Xi]) == 0:
                    return False
                
                # for each Xk in Xi.NEIGHBORS - {Xj} do
                for Xk in csp.graph[Xi]:
                    if Xk is not Xj:
                        # add (Xk, Xi) to queue
                        arcs.append((Xk, Xi))
        
        # return true
        return True

    # function REVISE(csp, Xi, Xj) returns true iff we revise the domain of Xi
    def revise(self, csp, Xi, Xj):
        # revised ← false
        revised = False

        # for each x in Di do
        for x in csp.domain[Xi]:
            count = 0

            for y in csp.domain[Xj]:
                if x == y:
                    count += 1
            
            # if no value y in Dj allows (x, y) to satisfy the constraint between Xi and Xj then
            if count == len(csp.domain[Xj]):
                # delete x from Di
                csp.domain[Xi].remove(x)

                # revised ← true
                revised = True
        
        # return revised
        return revised
    
    # function MRV_HEURISTIC(assignment, csp) returns unassigned variables, either sorted or not
    def MRV_heuristic(self, assignment, csp):
        # unassigned_vars ← all variables in the graph that are not in the assignment
        unassigned_vars = [var for var in csp.graph if var not in assignment]

        if self.MRV:
            # sorted_vars ← unassigned_vars sorted based on minimum remaining values
            sorted_vars = sorted(unassigned_vars, key = lambda var: len(csp.domain[var]))
        else:
            sorted_vars = unassigned_vars
        
        # return minimum of sorted_vars
        return sorted_vars[0]
    
    # function LCV_HEURISTIC(var, assignment, csp) returns domain, either sorted or not
    def LCV_heuristic(self, var, assignment, csp):
        # unsorted_domain ← the domain for var in csp
        unsorted_domain = csp.domain[var]

        if self.LCV:
            # sorted_domain ← unsorted_domain sorted based on least constraining value
            sorted_domain = sorted(unsorted_domain, key = lambda val: self.constraints_imposed(val, var, assignment, csp))
        else:
            sorted_domain = unsorted_domain
        
        # return sorted_domain
        return sorted_domain
    
    # function CONSTRAINTS_IMPOSED(value, var, assignment, csp) returns the number of constraints
    def constraints_imposed(self, value, var, assignment, csp):
        # constraints ← 0
        constraints = 0

        # for each neighbor in var.NEIGHBORS do
        for neighbor in csp.graph[var]:
            # constraints += the number of constraints imposed
            if neighbor not in assignment:
                constraints += sum([1 for val in csp.domain[neighbor] if val == value])
        
        # return constraints
        return constraints
    
    ## !!! BONUS !!! ##
    # function MIN_CONFLICTS_SEARCH(csp, max_steps) returns a solution, or failure
    def min_conflicts_search(self, csp, max_steps = 1000000):
        # current ← an initial complete assignment for csp
        current = self.initialize_assignment(csp)

        # for i = 1 to max_steps do
        for _ in range(max_steps):
            # if current is a solution for csp then return current
            if len([var for var in csp.graph if not csp.is_consistent(current[var], var, current, csp)]) == 0:
                return current
            
            # var ← a randomly chosen conflicted variable from csp.VARIABLES
            var = self.choose_conflicted_variable(current, csp)

            # value ← the value v for var that minimizes CONFLICTS(var, current, csp)
            value = self.min_conflicts_value(var, current, csp)

            # set var = value in current
            current[var] = value
        
        # return failure
        return None
    
    # function INITIALIZE_ASSIGNMENT(csp) returns a complete assignment for csp
    def initialize_assignment(self, csp):
        # assignment ← an empty assignment for csp
        assignment = {}

        # for each var in csp.VARIABLES
        for var in csp.graph:
            # assign a random value in var.DOMAIN to var
            assignment[var] = random.choice(csp.domain[var])
        
        # return assignment
        return assignment
    
    # function CHOOSE_CONFLICTED_VARIABLE(assignment, csp) returns a conflicted variable
    def choose_conflicted_variable(self, assignment, csp):
        # conflicted_vars ← a list of vars in csp.VARIABLES where the value is not consistent with the assignment
        conflicted_vars = [var for var in csp.graph if not csp.is_consistent(assignment[var], var, assignment, csp)]

        # return random choice of conflicted_vars
        return random.choice(conflicted_vars)
    
    # function MIN_CONFLICTS_VALUE(var, assignment, csp) returns the the value that minimizes CONFLICTS(var, value, assignment, csp)
    def min_conflicts_value(self, var, assignment, csp):
        # values ← list[value] in ORDER-DOMAIN-VALUES(var, assignment, csp)
        values = self.LCV_heuristic(var, assignment, csp)

        # sorted_values ← values sorted based on conflicts
        sorted_values = sorted(values, key = lambda val: self.conflicts(var, val, assignment, csp))

        # return minimum of sorted_vars
        return sorted_values[0]
    
    # function CONFLICTS(var, value, assignment, csp) returns the number of conflicts
    def conflicts(self, var, value, assignment, csp):
        # values ← list[value] in ORDER-DOMAIN-VALUES(var, assignment, csp)
        conflicts = 0

        # add variable to assignment
        assignment[var] = value

        # conflicts += the number of conflicts for neighbor in var.NEIGHBORS
        conflicts += sum([1 for neighbor in csp.graph[var] if neighbor in assignment and not csp.is_consistent(assignment[neighbor], neighbor, assignment, csp)])
        
        # remove {var = value}
        del assignment[var]

        # return conflicts
        return conflicts

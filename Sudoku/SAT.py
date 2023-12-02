# SAT.py
# Contains the methods with respect to the gsat and walksat algorithms.
# Carter Kruse (October 24, 2023)

import random

class SAT:
    # Constructor
    def __init__(self, file_name):
        # Instance Variables
        self.clauses = []
        self.variable_to_index = {}
        self.index_to_variable = {}
        self.index = 0
        self.model = {}

        # Open the file.
        file = open(file_name, 'r')

        # Cycle through the lines of the file.
        for line in file:
            # Add each line to the list of clauses.
            self.clauses.append(line.replace('\n', ''))
        
        # Close the file.
        file.close()

        # Cycle through the list of clauses.
        for clause in self.clauses:
            # Determine the specific variable/symbol in each clause.
            for variable in clause.split():
                # Update the variable/symbol to only be positive.
                var = variable.replace('-', '') if variable.startswith('-') else variable

                # If the variable is not already indexed...
                if var not in self.variable_to_index:
                    # Update the mappings/dictionaries, along with the index.
                    self.variable_to_index[var] = self.index
                    self.index_to_variable[self.index] = var
                    self.index += 1
    
    def sat(self, p_value, max_flips, algo, h_value):
        # Create a model with a random assignment of true/false.
        for index in range(self.index):
            # Each symbol in the clauses is represented.
            self.model[index] = random.choice([True, False])
        
        # Cycle continuously until 'max_flips' is reached.
        for k in range(max_flips):
            # If the model satisfies the clauses...
            if self.satisfies_clauses():
                print("Flips: " + str(k))

                # Return the model.
                return self.model
            
            # Select a random clause that is false in the model.
            if algo == 'walksat':
                # The 'random.choice()' is used to select from the false clauses.
                random_clause = random.choice(self.false_clauses())

                # The clause is mapped from the index to the appropriate variable and negation is disregarded.
                random_clause = [self.variable_to_index[var.replace('-', '')] if var.startswith('-') else self.variable_to_index[var] for var in random_clause.split()]
            
            # With a given probability, flip the value in the model.
            if random.random() < p_value:
                # The selected symbol is randomly selected from all symbols ('gsat') or the random clause ('walksat').
                random_index = random.randrange(self.index) if algo == 'gsat' else random.choice(random_clause)
                self.model[random_index] = not self.model[random_index]

            # Otherwise, flip whichever symbol in the clause maximizes the number of satisfied clauses.
            else:
                max_score = 0
                best_variables = []

                # Determine the set of symbols to iterate over, according to 'gsat' vs 'walksat'.
                loop_set = range(self.index) if algo == 'gsat' else random_clause
                for i in loop_set:
                    # Flip the symbol within the model.
                    self.model[i] = not self.model[i]

                    # Determine the score of the model.
                    current_score = self.score_model(h_value)

                    # Update the max score if appropriate, along with the best variables/symbols.
                    if current_score > max_score:
                        best_variables.clear()
                        max_score = current_score
                        best_variables.append(i)
                    
                    # Otherwise, simply update the best variables/symbols.
                    elif current_score == max_score:
                        best_variables.append(i)
                    
                    # Flip the symbol (back) within the model.
                    self.model[i] = not self.model[i]
                
                # BONUS: To enhance the walksat algorithm, we introduce a further aspect of randomness.
                if h_value != 0:
                    # If there are at least two 'best' variables/symbols...
                    if len(best_variables) >= 2:
                        # With a given probability, we make an additional flip in the model (at random).
                        if random.random() < h_value:
                            highest_variable = random.choice(best_variables)
                            self.model[highest_variable] = not self.model[highest_variable]
                
                # Flip the variable/symbol with the highest score (using a random choice).
                highest_variable = random.choice(best_variables)
                self.model[highest_variable] = not self.model[highest_variable]
    
    def score_model(self, h_value):
        score = 0

        # Cycle through the clauses.
        for clause in self.clauses:  
            # If the clause is satisfied, update the score.
            if self.satisfies(clause):
                # The 'h_value' is used only in an advanced algorithm.
                if h_value != 0:
                    score += 1 / len(clause)
                else:
                    score += 1
        
        return score
    
    def satisfies_clauses(self):
        # Cycle through the clauses.
        for clause in self.clauses:
            # If the clause is not satisfied, return false.
            if not self.satisfies(clause):
                return False
        
        return True
    
    def false_clauses(self):
        false_clauses = []

        # Cycle through the clauses.
        for clause in self.clauses:
            # If the clause is not satisfied, add to the set of false clauses.
            if not self.satisfies(clause):
                false_clauses.append(clause)
        
        return false_clauses
    
    def satisfies(self, clause):
        result = False

        # Determine the specific variable/symbol in each clause.
        for variable in clause.split():
            # If the variable is negated...
            if variable.startswith('-'):
                # The index is determined by the positive variable.
                index = self.variable_to_index[variable.replace('-', '')]
                
                # The result is determined opposite of expected.
                result = (result or (not self.model[index]))
            # Otherwise...
            else:
                index = self.variable_to_index[variable]
                result = (result or self.model[index])
        
        return result
    
    def write_solution(self, file_name):
        # Open the file to write to.
        file = open(file_name, 'w')

        # Cycle through the indices of the model.
        for index in self.model:
            # Determine the string based on true/false.
            string = self.index_to_variable[index] if self.model[index] else '-' + self.index_to_variable[index]
            
            # Write to the file.
            file.write(string + '\n')
        
        # Close the file.
        file.close()

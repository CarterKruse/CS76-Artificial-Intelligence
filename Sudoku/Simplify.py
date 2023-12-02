# Simplify.py
# Contains a class to simplify CNF files with known values.
# Carter Kruse (October 24, 2023)

class Simplify:
    def __init__(self, file_name):
        self.file_name = file_name
        self.known_values = [115, 259, 386, 418, 456, 548, 617, 772, 851, 895] # Puzzle 1
        # self.known_values = [123, 241, 329, 418, 456, 493, 548, 617, 696, 869, 895] # Puzzle 2
        # self.known_values = [115, 123, 157, 216, 241, 259, 265, 329, 338, 386, 418, 456, 493, 514, 548, 563, 591, 617, 652, 696, 726, 772, 788, 844, 851, 869, 895] # Puzzle Bonus
    
    def simplify(self):
        # Open the 'infile' and 'outfile' with the appropriate names.
        with open(self.file_name, 'r') as infile, open(self.file_name[:-4] + '_modified.cnf', 'w') as outfile:
            # Cycle through the lines of the 'infile'.
            for line in infile:
                # Strip each line of any whitespace.
                line = line.strip()

                # Boolean: Determines if this line is written in the 'outfile'.
                write_line = True

                # Cycle through the list of known values (constants).
                for cell in self.known_values:
                    # Determine the index of the known value.
                    index = line.find(str(cell))

                    # If the value is found, modify the results.
                    if index != -1:
                        # Check the boundary condition.
                        if index != 0:
                            # Check if the value is negative in the line.
                            if line[index - 1] == '-':
                                # If so, update the line by removing it.
                                line = (line[:index - 1] + line[index + 3:]).strip()
                            # Otherwise, do not write the line.
                            else:
                                write_line = False
                        else:
                            write_line = False
                
                # If the line is to be written, update the 'outfile'.
                if write_line:
                    outfile.write(line + '\n')
            
            # Include the known values back into the CNF file.
            for cell in self.known_values:
                outfile.write(str(cell) + '\n')
    
    def resolution(self):
        # Open the 'infile' and 'outfile' with the appropriate names.
        with open(self.file_name, 'r') as infile, open('data/resolution.cnf', 'w') as outfile:
            # Cycle through the lines of the 'infile'
            for line in infile:
                # Strip each line of any whitespace.
                line = line.strip()

                # Boolean: Determines if this line is written in the 'outfile'.
                write_line = True

                # Cycle through the elements of each line.
                for element in line.split():
                    # Check if the hundreds digit is okay.
                    if (abs(int(element)) % 1000) // 100 > 3:
                        write_line = False
                    # Check if the tens digit is okay
                    if (abs(int(element)) % 100) // 10 > 3:
                        write_line = False
                
                # If the line is to be written, update the 'outfile'.
                if write_line:
                    outfile.write(line + '\n')                        

if __name__ == "__main__":
    puzzle_name = 'data/puzzle1'
    # puzzle_name = 'data/puzzle2'
    # puzzle_name = 'data/puzzle_bonus'
    # puzzle_name = 'data/rules'

    cnf_file_name = puzzle_name + '.cnf'

    simplify = Simplify(cnf_file_name)
    simplify.simplify()
    # simplify.resolution()

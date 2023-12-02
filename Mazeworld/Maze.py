# Maze.py
# Maze objects are for loading and displaying mazes, and doing collision checks.
# Carter Kruse (September 27, 2023)

# Description
# Maze objects are not a good object to use to represent the state of a robot mazeworld
# search problem, since the locations of the walls are fixed and not part of the state.
# You should do something else to represent the state.

# However, each mazeworld problem might make use of a (single) maze object, modifying
# it as needed in the process of checking for legal moves.

# The test code at the bottom of this file shows how to load in and display a few maze
# data files (i.e. "maze1.maz", which you should find in this directory).

# The order in a tuple is (x, y) starting with zero at the bottom left.

# Maze File Format:
#  # is a wall
#  . is a floor
#  The command \robot x y adds a robot at a location.
#  The first robot added has index 0, and so forth.

from time import sleep

class Maze:
    # Internal Structure:
        # self.walls - Set of tuples with wall locations.
        # self.width - Number of columns.
        # self.rows
    
    def __init__(self, mazefilename):
        self.robotloc = []

        # Read the maze file into a list of strings.
        file = open(mazefilename)
        
        lines = []
        for line in file:
            line = line.strip()

            # Ignore blank lines.
            if len(line) == 0:
                pass
            elif line[0] == "\\":
                # There's only one command, \robot, so assume it is that.
                # print("command")

                params = line.split()
                (x, y) = (int(params[1]), int(params[2]))

                self.robotloc.append(x)
                self.robotloc.append(y)
            else:
                lines.append(line)
        
        file.close()

        self.width = len(lines[0])
        self.height = len(lines)

        self.map = list("".join(lines))
    
    def index(self, x, y):
        return (self.height - y - 1) * self.width + x
    
    # Returns true if the location is a floor.
    def is_floor(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        
        return self.map[self.index(x, y)] == "."
    
    def has_robot(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        
        for i in range(0, len(self.robotloc), 2):
            rx = self.robotloc[i]
            ry = self.robotloc[i + 1]

            if rx == x and ry == y:
                return True
            
        return False
    
    # This function is called only by __str__ that takes the map and the robot state
    # and generates a list of characters in order that they will will need to be
    # printed out in.
    def create_render_list(self):
        # print(self.robotloc)
        renderlist = list(self.map)

        robot_number = 0
        for index in range(0, len(self.robotloc), 2):
            x = self.robotloc[index]
            y = self.robotloc[index + 1]

            renderlist[self.index(x, y)] = robotchar(robot_number)
            robot_number += 1
        
        return renderlist
    
    def __str__(self):
        # Render robot locations into the map.
        renderlist = self.create_render_list()

        # Use the render list to construct a string, by adding newlines appropriately.
        s = ""
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                s += renderlist[self.index(x, y)]
            s += "\n"

        return s

def robotchar(robot_number):
    return chr(ord("A") + robot_number)

# Test Code
if __name__ == "__main__":
    test_maze1 = Maze("maze1.maz")
    print(test_maze1)

    test_maze2 = Maze("maze2.maz")
    print(test_maze2)

    test_maze3 = Maze("maze3.maz")
    print(test_maze3)

    # Maze 3
    print(test_maze3.robotloc)

    print(test_maze3.is_floor(2, 3))
    print(test_maze3.is_floor(-1, 3))
    print(test_maze3.is_floor(1, 0))

    print(test_maze3.has_robot(1, 0))

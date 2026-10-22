class Grid:
    def __init__(self):
        self.grid = [[0 for _ in range(30)] for _ in range(30)]

    def loadstate(self, pattern):
        # dictionary is not really used, understood it only after i wrote the func
        state = {
            1: "canoe.txt",
            2: "cloverleaf.txt",
            3: "hammerhead.txt",
            4: "checkedpattern1",
        }  # grids were created using chatgpt
        if pattern == 1:
            canoe = open("canoe.txt", "r")
            for row, line in enumerate(canoe.readlines()):
                for column, val in enumerate(line.strip()):
                    self.grid[row][column] = int(val)
        elif pattern == 2:
            cloverleaf = open("cloverleaf.txt", "r")
            for row, line in enumerate(cloverleaf.readlines()):
                for column, val in enumerate(line.strip()):
                    self.grid[row][column] = int(val)
        elif pattern == 3:
            hammerhead = open("hammerhead.txt", "r")
            for row, line in enumerate(hammerhead.readlines()):
                for column, val in enumerate(line.strip()):
                    self.grid[row][column] = int(val)
        else:
            checkedpattern1 = open("checkedpattern1.txt", "r")
            for row, line in enumerate(checkedpattern1.readlines()):
                for column, val in enumerate(line.strip()):
                    self.grid[row][column] = int(val)

    def printstate(self):
        for row in self.grid:
            print(
                " ".join(str(cell) for cell in row)
            )  # my own printstate, used chatgpt for the gif like

    def runstates(
        self, steps
    ):  # my func for the animation it cant do it as it will just output all steps at once
        neighbours = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]
        for step in range(steps):
            nextgrid = [[0 for _ in range(30)] for _ in range(30)]
            for row in range(30):
                for col in range(30):
                    aliveneighs = 0
                    for dx, dy in neighbours:
                        newrow = row + dx
                        newcol = col + dy
                        if newrow < 0 or newrow >= 30 or newcol < 0 or newcol >= 30:
                            continue
                        if self.grid[newrow][newcol] == 1:
                            aliveneighs += 1
                    if self.grid[row][col] == 1:
                        if aliveneighs < 2 or aliveneighs > 3:
                            nextgrid[row][col] = 0
                        else:
                            nextgrid[row][col] = 1
                    else:
                        if aliveneighs == 3:
                            nextgrid[row][col] = 1
            self.grid = nextgrid
            self.printstate()
            print(
                "-----------------------------------------------------------------------------------------------------------------------------"
            )

    # couldve fixed this runstate for animation but wanted to show my own idea first before using gpt idea for fixing code for animation
    def nextstate(
        self,
    ):  # like run states but better for animation as it does frame by frame and not outputting all at once
        neighbours = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]
        nextgrid = [[0 for _ in range(30)] for _ in range(30)]
        for row in range(30):
            for col in range(30):
                aliveneighs = 0
                for dx, dy in neighbours:
                    newrow = row + dx
                    newcol = col + dy
                    if newrow < 0 or newrow >= 30 or newcol < 0 or newcol >= 30:
                        continue
                    if self.grid[newrow][newcol] == 1:
                        aliveneighs += 1
                if self.grid[row][col] == 1:
                    if aliveneighs < 2 or aliveneighs > 3:
                        nextgrid[row][col] = 0
                    else:
                        nextgrid[row][col] = 1
                else:
                    if aliveneighs == 3:
                        nextgrid[row][col] = 1
        self.grid = nextgrid

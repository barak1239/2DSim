class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        """for 3x3 will create: none none none 
                               none none none
                               none none none"""

        self.eventmanager = None
        self.currturn = 0

    def addentity(self, entity: object) -> None:
        x, y = entity.x, entity.y

        if not (0 <= x < self.height and 0 <= y < self.width):
            raise ValueError(f"Invalid entity position: ({x}, {y})")

        if self.grid[x][y] is not None:
            raise ValueError(f"Cell ({x}, {y}) is already occupied")

        self.grid[x][y] = entity

    def remove(self, entity):
        self.grid[entity.x][entity.y] = None

class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        '''for 3x3 will create: none none none 
                               none none none
                               none none none'''
    def addentity(self, entity):
            self.grid[entity.x][entity.y] = entity
    def remove(self, entity):
            self.grid[entity.x][entity.y] = None
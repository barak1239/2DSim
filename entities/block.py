from .entity import Entity


class Block(Entity):
    def __init__(self, x, y):
        super().__init__(x, y)

    def update(self, grid, parameters):
        return None


class Rock(Block):
    def __init__(self, x, y):
        super().__init__(x, y)


class Tree(Block):
    def __init__(self, x, y):
        super().__init__(x, y)

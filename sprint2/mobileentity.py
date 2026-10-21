import random as rnd
import collections
from entity import Entity
from sprint2.block import Tree as Tree, Rock as Rock
from plant import Plant as Plant
class MobileEntity(Entity):
    def __init__(self, steps, x, y):
        super().__init__(x, y)
        self.steps = steps
    def look(self,range, grid):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        queue = collections.deque([(self.x, self.y, 0)])
        '''help of https://stackoverflow.com/questions/6124402/python-bfs-with-collections'''
        visited = {(self.x, self.y)}  # same as set()
        parent = {(self.x, self.y): None}
        while queue:
            x, y, dist = queue.popleft()
            if isinstance(grid.grid[x][y], self.foodtype):
                path = []
                while (x, y) != (self.x, self.y):
                    path.append((x, y))
                    x, y = parent[(x, y)]
                path.reverse()
                return path
            if dist >= range:
                continue
            for dx, dy in directions:
                newx = x + dx
                newy = y + dy
                if newx < 0 or newx >= grid.height or newy < 0 or newy >= grid.width:
                    continue
                if isinstance(grid.grid[newx][newy], (Rock, Tree)):
                    continue
                cell = grid.grid[newx][newy]
                if cell is not None and not isinstance(cell, self.foodtype):
                    if not(
                            (isinstance(self, Herb) and isinstance(cell, Herb))\
                            or (isinstance(self, Pred) and isinstance(cell, Plant))
                    ):
                        '''if not 2 herbs reproduction or pred destroys plant'''
                        continue
                if (newx, newy) in visited:
                    continue
                visited.add((newx, newy))
                parent[(newx, newy)] = (x, y)
                queue.append((newx, newy, dist + 1))
        # random when no food
        rnd.shuffle(directions)
        for dx, dy in directions:
            newx = self.x + dx
            newy = self.y + dy
            if 0 <= newx < grid.height and 0 <= newy < grid.width:
                cell = grid.grid[newx][newy]
                if (cell is None
                    or (isinstance(self, Herb) and isinstance(cell, Herb))
                    or (isinstance(self, Pred) and isinstance(cell, Plant))):
                        return [(newx, newy)]
        return

    def move(self, path, grid, T_cooldown,T_HERBIVORE):
        if not path:
            return
        newx, newy = path[0]
        food = grid.grid[newx][newy]
        if isinstance(self, Herb) and isinstance(food, Herb):
#reproduction
            if self.cooldown == 0 and food.cooldown == 0:
                if self.reproduce(grid,T_HERBIVORE):
                    self.cooldown = T_cooldown
                    food.cooldown = T_cooldown
                    return
            # no reproduction isn't possible= try another direction
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]
            rnd.shuffle(directions)
            for dx, dy in directions:
                newx = self.x + dx
                newy = self.y + dy
                if 0 <= newx < grid.height and 0 <= newy < grid.width:
                    if grid.grid[newx][newy] is None:
                        grid.remove(self)
                        self.x, self.y = newx, newy
                        grid.addentity(self)
                        return
            return  # no empty cell found
        # normal movement and eating
        if isinstance(food, self.foodtype):
            self.steps += food.steps
        grid.remove(self)
        self.x, self.y = newx, newy
        grid.addentity(self)

    def update(self, grid, range, T_cooldown, T_HERBIVORE):
        path = self.look(range, grid)
        self.move(path, grid, T_cooldown, T_HERBIVORE)
        self.steps -= 1
        if self.steps <= 0:
            grid.remove(self)
class Herb(MobileEntity):
    foodtype = Plant
    def __init__(self,steps,x,y):
        super().__init__(steps, x,y)
        self.cooldown = 0
    def reproduce(self,grid,T_HERBIVORE):
        if self.cooldown > 0:
            return

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]

        rnd.shuffle(directions)

        for dx, dy in directions:
            newx = self.x + dx
            newy = self.y + dy

            if 0 <= newx < grid.height and 0 <= newy < grid.width:
                if grid.grid[newx][newy] is None:
                    baby = Herb( T_HERBIVORE,newx, newy)
                    grid.addentity(baby)
                    return True #not my idea to return true/false here
        return False

    def update(self, grid, range, T_cooldown, T_HERBIVORE):
        if self.cooldown > 0:
            self.cooldown -= 1
        super().update(grid, range, T_cooldown, T_HERBIVORE)
class Pred(MobileEntity):
    foodtype = Herb
    def __init__(self,steps,x,y):
        super().__init__(steps, x,y)
import collections
import random as rnd

import consts

from .block import Block
from .entity import Entity


class MobileEntity(Entity):
    foodtypes = ()
    passthrough = ()

    def __init__(self, steps, x, y, reproduce):
        """
        Args:
            steps: number of steps until entity dies
            x:
            y:
        """
        super().__init__(x, y)
        self.steps = steps
        self.canreproduce = reproduce

    def check2reproduce(self, other) -> bool:
        """
        will check if they are same of the same entity and make sure nothing wrong can pass and crush the func
        Args:
            other: other entity

        Returns: bool

        """
        if not (isinstance(other, MobileEntity)):
            return False
        return type(self) == type(other) and self.canreproduce and other.canreproduce

    def readytoreproduce(self) -> bool:
        """
        we check if you are even able to reproduce the animal if so check what the cooldown is
        Returns: bool

        """

        return self.canreproduce and self.cooldown == 0

    def reproduce(self, grid, newbornsteps) -> bool:
        """
        new entity of the same type in an empty
        neighboring cell.

        Args:
            grid: grid.
            newbornsteps: the starting lifetime from yaml.

        Returns:
            bool of if baby created
        """
        if not self.readytoreproduce():
            return False

        directions = consts.DIRECTIONS.copy()
        rnd.shuffle(directions)

        for dx, dy in directions:
            newx = self.x + dx
            newy = self.y + dy

            if 0 <= newx < grid.height and 0 <= newy < grid.width:
                if grid.grid[newx][newy] is None:
                    baby = type(self)(newbornsteps, newx, newy)
                    grid.addentity(baby)
                    return True

        return False

    def look(self, sightrange: int, grid: object) -> list | None:
        """
        look in range for food to eat
        Args:
            sightrange: int for max range an animal can look at
            grid:

        Returns:
        path
        """
        directions = consts.DIRECTIONS.copy()
        queue = collections.deque([(self.x, self.y, 0)])
        """help of https://stackoverflow.com/questions/6124402/python-bfs-with-collections"""
        visited = {(self.x, self.y)}  # same as set()
        parent = {(self.x, self.y): None}
        while queue:
            x, y, dist = queue.popleft()
            if isinstance(grid.grid[x][y], self.foodtypes):
                path = []
                while (x, y) != (self.x, self.y):
                    path.append((x, y))
                    x, y = parent[(x, y)]
                path.reverse()
                return path
            if dist >= sightrange:
                continue
            for dx, dy in directions:
                newx = x + dx
                newy = y + dy
                if newx < 0 or newx >= grid.height or newy < 0 or newy >= grid.width:
                    continue
                if isinstance(grid.grid[newx][newy], (Block)):
                    continue
                cell = grid.grid[newx][newy]
                if cell is not None and not isinstance(cell, self.foodtypes):
                    if not (
                        self.check2reproduce(cell) or isinstance(cell, self.passthrough)
                    ):
                        """if not 2 herbs reproduction or pred destroys plant"""
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
                if (
                    cell is None
                    or self.check2reproduce(cell)
                    or isinstance(cell, self.passthrough)
                ):
                    return [(newx, newy)]
        return None

    def move(self, path: object, grid: object, T_cooldown: object, newbornsteps: object) -> None:
        """
        the actual movement of the animal
        Args:
            path: coordinates of the path to follow, or None
            if no valid path was found.
            grid: the simulation grid containing all entities.
            T_cooldown: const in yaml
            newbornsteps: const in yaml

        Returns: None
        """
        if not path:
            return
        newx, newy = path[0]
        other = grid.grid[newx][newy]
        if self.check2reproduce(other):
            # reproduction
            if self.readytoreproduce() and other.readytoreproduce():
                if self.reproduce(grid, newbornsteps):
                    self.cooldown = T_cooldown
                    other.cooldown = T_cooldown
                    return
            # no reproduction isn't possible= try another direction
            directions = consts.DIRECTIONS.copy()
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
        if other is not None:
            if isinstance(other, self.foodtypes):
                self.steps += other.steps

                if grid.eventmanager is not None:
                    grid.eventmanager.notifyObservers({
                        "type": "entity_eaten",
                        "eater": self,
                        "prey": other
                    })

            elif not isinstance(other, self.passthrough):
                raise ValueError(
                    f"Cannot move onto {type(other).__name__} "
                    f"at ({newx}, {newy})"
                )

            # Remove the eaten or destroyed entity before moving
            grid.remove(other)

        # Move to the destination
        grid.remove(self)
        self.x, self.y = newx, newy
        grid.addentity(self)

    def update(self, grid: object, parameters: object) -> None:
        """
        handles removing and adjusting entity lives (steps)
        Args:
            grid:
            parameters: dictionary of simulation settings loaded from
            config.yaml, including sight range, reproduction cooldown,
            and the initial lifetime of newborn entities.

        Returns: none
        """
        sight = parameters[self.sightkey]
        newbornsteps = parameters[self.lifetimekey]
        cooldown = parameters["T_COOLDOWN"]

        path = self.look(sight, grid)
        self.move(path, grid, cooldown, newbornsteps)

        self.steps -= 1
        if self.steps <= 0:
            grid.remove(self)

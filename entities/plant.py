import random as rnd

import consts

from .entity import Entity


class Plant(Entity):
    def __init__(self, steps, x, y):
        super().__init__(x, y)
        self.steps = steps

    def spawn(self, grid: object, plantsteps: int) -> None:
        """
        creates up to 10 new plants. return nothing but updates the grid
        Args:
            grid: the simulation grid containing all entities.

        Returns: nothing, just updates the grid with a new plantt

        """
        empty_cells = [
            (x, y)
            for x in range(grid.height)
            for y in range(grid.width)
            if grid.grid[x][y] is None
        ]
        spawn_count = min(consts.PLANTS_PER_SPAWN, len(empty_cells))
        for x, y in rnd.sample(empty_cells, spawn_count):
            newplant = Plant(plantsteps, x, y)
            grid.addentity(newplant)

    def update(self, grid, parameters) -> None:
        self.steps -= 1
        if self.steps <= 0:
            grid.remove(self)

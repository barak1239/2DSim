from .mobileentity import MobileEntity
from .plant import Plant


class Herb(MobileEntity):
    foodtypes = (Plant,)
    passthrough = ()
    sightkey = "R_HERBIVORE_SIGHT"
    lifetimekey = "T_HERBIVORE"

    def __init__(self, steps, x, y):
        super().__init__(steps, x, y, reproduce=True)
        self.cooldown = 0

    def update(self, grid: object, parameters: object) -> None:
        """
        handles removing and adjusting entity lives (steps)
        Args:
            grid:
            parameters:

        Returns: none

        """
        if self.cooldown > 0:
            self.cooldown -= 1

        super().update(grid, parameters)
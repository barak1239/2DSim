from .herb import Herb
from .mobileentity import MobileEntity
from .plant import Plant


class Pred(MobileEntity):
    foodtypes = (Herb,)
    passthrough = (Plant,)
    sightkey = "R_PREDATOR_SIGHT"
    lifetimekey = "T_PREDATOR"

    def __init__(self, steps, x, y):
        super().__init__(steps, x, y, reproduce=False)
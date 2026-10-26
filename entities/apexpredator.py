from .herb import Herb
from .mobileentity import MobileEntity
from .plant import Plant
from .predator import Pred


class ApexPredator(MobileEntity):
    foodtypes = (Herb, Pred)
    passthrough = (Plant,)
    sightkey = "R_APEX_PREDATOR_SIGHT"
    lifetimekey = "T_APEX_PREDATOR"

    def __init__(self, steps, x, y)->None:
        super().__init__(steps, x, y, reproduce=False)

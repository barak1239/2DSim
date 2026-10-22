from .mobileentity import MobileEntity, Herb , Pred
from .plant import Plant
class ApexPredator(MobileEntity):
    foodtypes = (Herb,Pred)
    passthrough = (Plant,)
    sightkey = "R_APEX_PREDATOR_SIGHT"
    lifetimekey = "T_APEX_PREDATOR"
    def __init__(self, steps, x, y):
        super().__init__(steps,x,y, reproduce= False)


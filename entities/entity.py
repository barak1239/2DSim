import random as rnd
import collections
from abc import ABC, abstractmethod


class Entity(ABC):
    def __init__(self, x, y):
        """
        Entity Constructor
        :param x: x coordinate
        :param y: y coordinate
        Args:
            x:
            y:
        """
        self.x = x
        self.y = y

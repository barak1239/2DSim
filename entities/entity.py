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
    @abstractmethod
    def update(self,grid, parameters)->None:
        """
        update the entity place and actions
        Args:
            grid:
            parameters: list of paramenters

        Returns:
        nothing as we update the board
        """
        pass
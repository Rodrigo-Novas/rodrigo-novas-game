"""Colors module."""

from abc import ABC
import random


class Colour(ABC):
    def return_colour(self):
        pass


class NormalColour(Colour):
    def __init__(self, red: int, green: int, blue: int):
        self.r = red
        self.g = green
        self.b = blue

    def return_colour(self):
        return (self.r, self.g, self.b)


class RandomColour(Colour):
    def __init__(self):
        self.r = random.randint(0, 254)
        self.g = random.randint(0, 254)
        self.b = random.randint(0, 254)

    def return_colour(self):
        return (self.r, self.g, self.b)

import pygame as pg
import random

from ant import Ant


class Base:
    def __init__(self, x, y):
        self.surface = pg.Surface((9, 9))
        self.color = (random.randint(128, 255), random.randint(128, 255), random.randint(128, 255))
        self.surface.fill(self.color)

        self.rect = self.surface.get_rect()
        self.rect.centerx, self.rect.centery = x, y

        self.energy = 100

        self.ants = [Ant(x, y, self.color, self)]

        for i in range(10):
            self.ants.append(Ant(x, y, self.color, self))
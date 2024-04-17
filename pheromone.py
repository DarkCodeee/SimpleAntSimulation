import pygame as pg


class Pheromone:
    def __init__(self, x, y, last, typee, parent, stage):
        self.surface = pg.Surface((2, 2))
        #self.surface.fill((128, 128, 128))
        self.surface.fill((255, 0, 0))
        self.rect = self.surface.get_rect()
        self.rect.centerx, self.rect.centery = x, y

        self.last = last
        self.typee = typee
        self.life_time = 100
        if typee == "explorer":
            self.surface.fill((255, 0, 0))
        elif typee == "go_food":
            self.life_time = 200
            self.surface.fill((0, 255, 255))
        self.parent = parent

        self.last_time = stage


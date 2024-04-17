import pygame as pg
import random

from pheromone import Pheromone
from food import PackFood


class Ant:
    def __init__(self, x, y, color, base):
        self.surface = pg.Surface((2, 2))
        self.surface.fill(color)

        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = x, y

        self.viewer_rect = pg.Rect(0, 0, 32, 32)
        self.viewer_rect.centerx, self.viewer_rect.centery = self.rect.centerx, self.rect.centery

        self.last_pheromone = None

        self.command_type = "explorer"

        self.stage = None

        self.base = base

        self.focus = None

    def update(self, pheromones: list, ants: list, pack_foods, stage):

        vector = random.choice(((0, 1), (1, 0), (0, -1), (-1, 0)))
        vector_2 = ((0, 1), (1, 0), (0, -1), (-1, 0))
        if self.command_type == "go_base":
            if isinstance(self.last_pheromone, Pheromone):
                new_rect = self.rect.copy()
                new_vectors = []
                if self.rect.x > self.last_pheromone.rect.x:
                    new_vectors.append([-1, 0])
                if self.rect.x < self.last_pheromone.rect.x:
                    new_vectors.append([1, 0])
                if self.rect.y > self.last_pheromone.rect.y:
                    new_vectors.append([0, -1])
                if self.rect.y < self.last_pheromone.rect.y:
                    new_vectors.append([0, 1])
                if len(new_vectors):
                    vector = random.choice(new_vectors)
                    new_rect.x += vector[0] * 2
                    new_rect.y += vector[1] * 2

                    if not all(new_rect.colliderect(ant.rect) for ant in ants):
                        self.rect.x += vector[0]
                        self.rect.y += vector[1]

                    if self.rect.colliderect(self.last_pheromone.rect):
                        self.last_pheromone = self.last_pheromone.last

                    if self.rect.colliderect(self.base.rect):
                        self.command_type = "explorer"

        if self.command_type == "go_food":
            if self.focus:
                if len(self.focus.foods):
                    food = self.focus.foods[0]
                else:
                    self.command_type = "explorer"
                    self.focus = None
                    return

                new_rect = self.rect.copy()
                new_vectors = []
                if self.rect.x > food.rect.x:
                    new_vectors.append([-1, 0])
                if self.rect.x < food.rect.x:
                    new_vectors.append([1, 0])
                if self.rect.y > food.rect.y:
                    new_vectors.append([0, -1])
                if self.rect.y < food.rect.y:
                    new_vectors.append([0, 1])
                if len(new_vectors):
                    vector = random.choice(new_vectors)
                    new_rect.x += vector[0] * 2
                    new_rect.y += vector[1] * 2

                    if not all(new_rect.colliderect(ant.rect) for ant in ants):
                        self.rect.x += vector[0]
                        self.rect.y += vector[1]

                for food in self.focus.foods[:]:
                    if self.rect.colliderect(food.rect):
                        self.command_type = "go_base"
                        self.focus.foods.remove(food)

        if self.command_type == "explorer":
            for pack_food in pack_foods:
                if self.viewer_rect.colliderect(pack_food.rect):
                    self.command_type = "go_food"
                    self.focus = pack_food
                    return

            new_rect = self.rect.copy()
            new_rect.x += vector[0] * 2
            new_rect.y += vector[1] * 2
            if not all(new_rect.colliderect(ant.rect) for ant in ants):
                self.rect.x += vector[0]
                self.rect.y += vector[1]

                self.rect.x = 0 if self.rect.x < 0 else self.rect.x
                self.rect.x = 1280 if self.rect.x > 1280 else self.rect.x

                self.rect.y = 0 if self.rect.y < 0 else self.rect.y
                self.rect.y = 720 if self.rect.y > 720 else self.rect.y

        if self.command_type != "go_base":
            if not any(self.rect.colliderect(pheromone.rect) for pheromone in pheromones):
                self.last_pheromone = Pheromone(self.rect.x, self.rect.y, self.last_pheromone, self.command_type, id(self), stage)
                pheromones.append(self.last_pheromone)
            self.viewer_rect.centerx, self.viewer_rect.centery = self.rect.centerx, self.rect.centery
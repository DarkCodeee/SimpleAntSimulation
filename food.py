import pygame as pg
import random
import math


class Food:
    def __init__(self, x, y):
        self.surface = pg.Surface((2, 2))
        self.surface.fill((235, 99, 148))
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = x, y


class PackFood:
    def __init__(self, centerx, centery):
        number_food = random.randint(15, 30)

        self.rect = pg.Rect(0, 0, number_food, number_food)
        self.rect.centerx, self.rect.centery = centerx, centery

        self.foods = [Food(centerx, centery)]
        while len(self.foods) < number_food:
            for i in self.foods:
                vector = random.choice(((0,1), (1, 0), (0, -1), (-1, 0)))
                new_rect = i.rect.copy()
                new_rect.x += vector[0]
                new_rect.y += vector[1]
                if abs(math.sqrt((new_rect.x - centerx)**2 + (new_rect.y - centery)**2)) <= number_food // 2:
                    if not all(new_rect == food.rect for food in self.foods):
                        self.foods.append(Food(new_rect.x, new_rect.y))
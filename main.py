import pygame as pg
import random

from base import Base
from food import PackFood

display = pg.display.set_mode((1280, 720), flags=pg.DOUBLEBUF)

bases = []
for i in range(10):
    base = Base(random.randint(10, 1270), random.randint(10, 720))
    if not any(base.rect.colliderect(i.rect) for i in bases):
        bases.append(base)

pack_foods = []
for i in range(100):
    pack_food = PackFood(random.randint(10, 1270), random.randint(10, 720))
    if not any(pack_food.rect.colliderect(i.rect) for i in pack_foods):
        if not any(pack_food.rect.colliderect(i.rect) for i in bases):
            pack_foods.append(pack_food)

pheromones = []

run = True
stage = 0
while run:
    display.fill((0, 0, 0))
    for e in pg.event.get():
        if e.type == pg.QUIT:
            run = False

    for pheromone in pheromones[:]:
        if stage - pheromone.last_time > pheromone.life_time:
            pheromones.remove(pheromone)
        else:
            break
    [[ant.update(pheromones, base.ants, pack_foods, stage) for ant in base.ants] for base in bases]

    [[display.blit(food.surface, food.rect) for food in pack_food.foods] for pack_food in pack_foods]
    [display.blit(pheromone.surface, pheromone.rect) for pheromone in pheromones]
    [[display.blit(ant.surface, ant.rect) for ant in base.ants] for base in bases]

    [display.blit(base.surface, base.rect) for base in bases]

    pg.display.update()

    pg.time.delay(10)
    stage += 1

pg.quit()

import math
import random
import sys
import pygame
from pygame.locals import *
import time
import json

from designs import *
from gradient import *
from helpers import *
from experimental import *

SCREEN_WIDTH = 680
SCREEN_HEIGHT = 680


CLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("©2022 Dragon tail")

def color_dif(c1, c2):
    dif = 0
    for n in [0, 1, 2]:
        dif += abs(c1[n] - c2[n])
    
    return dif

class dot(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()     

        self.color = (random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
        self.pos = pos

    def update(self, surface, dots):
        if random.randint(0, 0) == 0:
            for n in dots:
                if n != self:
                    dis = distance(self.pos, n.pos) * 400
                    affect =  dis - color_dif(self.color, n.color) ** 2

                    direction = calculate_angle(n.pos, self.pos)
                    change = rotating_position(0, affect * (0.001 / len(dots)), direction, [0, 0])

                    self.pos[0] += change[0]
                    self.pos[1] += change[1]
        
            self.pos[0] += 1000 / self.pos[0]
            self.pos[0] -= 1000 / (SURFACE.get_width() - self.pos[0])
            self.pos[1] += 1000 / self.pos[1]
            self.pos[1] -= 1000 / (SURFACE.get_height() - self.pos[1])

        pygame.draw.circle(surface, self.color, self.pos, 5)

DOTS = pygame.sprite.Group()

for n in range(1):
    DOTS.add(dot([random.randint(0, SURFACE.get_width()), random.randint(0, SURFACE.get_height())]))

RUNNING = True

while RUNNING:
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
        if event.type == KEYDOWN:
            if event.key == K_q:
                RUNNING = False

    SURFACE.fill((210, 225, 235))

    if check_released(0):
        DOTS.add(dot(list(pygame.mouse.get_pos())))

    for n in DOTS:
        n.update(SURFACE, DOTS)

    pygame.display.update()
    CLOCK.tick(40)
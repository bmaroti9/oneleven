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

pygame.init()


SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 710

print(pygame.font.get_fonts())

CLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("©2022 Dragon tail")


FONT1 = pygame.font.SysFont('andalemono', 50)
FONTS = pygame.font.get_fonts()


ALTITUDE = 0
SCROLL = 0
RUNNING = True

while RUNNING:
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
        if event.type == KEYDOWN:
            if event.key == K_q:
                RUNNING = False
        if event.type == pygame.MOUSEWHEEL:
            ALTITUDE += event.y * 50

    SURFACE.fill((0, 0, 0))

    x = ALTITUDE
    for n in FONTS:
        he = pygame.font.SysFont(str(n), 50)
        try:
            #blit_text(SURFACE, (250, 250, 250), "2022  HIHI   " + str(n), [10, x], he)
            blit_text(SURFACE, (250, 250, 250), "0123456789%      " + str(n), [10, x], he)
        except:
            continue
        x += 70
    

    pygame.display.update()
    CLOCK.tick(10)


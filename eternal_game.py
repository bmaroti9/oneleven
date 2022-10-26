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

SCREEN_WIDTH = 350
SCREEN_HEIGHT = 600


CLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("©2022 Dragon tail")

RUNNING = True

while RUNNING:
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
    
    SURFACE.fill((210, 225, 235))

    pygame.display.update()
    CLOCK.tick(40)
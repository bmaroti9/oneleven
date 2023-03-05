import math
import random
import sys
import pygame
from pygame.locals import *
import time
import json

from clouds import *
from designs import *
from gradient import *
from helpers import *
from experimental import *
from tiles import *

pygame.init()

FONT1 = pygame.font.SysFont('andalemono', 50)
FONT2 = pygame.font.SysFont("ubuntu", 30)
FONT3 = pygame.font.SysFont('nanumgothic', 25)
FONT4 = pygame.font.SysFont("ubuntu", 27)
FONT5 = pygame.font.SysFont('latinmodernmonoprop', 30)
FONT6 = pygame.font.SysFont('nanumgothic', 22)
FONT7 = pygame.font.SysFont("ubuntu", 36)

SCREEN_WIDTH = 1364
SCREEN_HEIGHT = 715

print(pygame.font.get_fonts())

CLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("©2022 Dragon tail")

RUNNING = True

BLUR_SURF = colour_rect = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))         

CLOUDMAP = Cloudmap(SURFACE)
TIME = Time()
EVENTMAP = Eventmap()
#TIME_MAP = Time_map()

BACK_COLOR = (240, 180, 230)

ALTITUDE = 0.01
SCROLL = 0
SMOOTH_SCROLL = 0
MAX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
FOCUS_TIME = 0

FOCUS_TIME = TIME.update(SURFACE, ALTITUDE)

TILE_SPACE = Tile_space()

for n in range(10):
    TILE_SPACE.add_tile(FOCUS_TIME + n * 650)

while RUNNING:
    SCROLLING = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
        if event.type == KEYDOWN:
            if event.key == K_q:
                RUNNING = False
            if event.key == K_0:
                set_theme(0)
            if event.key == K_1:
                set_theme(1)
            if event.key == K_2:
                set_theme(2)
        if event.type == pygame.MOUSEWHEEL:
            SCROLL += event.y * 40 #0.95
            if not MAX.__contains__(1):
                SCROLLING = 1
    
    if detect_click_rect(0, Rect(27, SURFACE.get_height() - 110, 140, SURFACE.get_height() - 25)):
        SCROLL = -ALTITUDE * 0.03093
        SMOOTH_SCROLL = 0
    elif check_released(0):
        #TILE_SPACE.add_tile(FOCUS_TIME)
        pass
        
    
    SCROLL = SCROLL * 0.973
    SMOOTH_SCROLL += (SCROLL - SMOOTH_SCROLL) * 0.4
    ALTITUDE += SMOOTH_SCROLL
    MAX.append(SCROLLING)

    del MAX[0]

    SURFACE.fill(get_colors()[0])
    print(MAX.__contains__(1))
    
    #ALTITUDE += TILE.update(SURFACE, FOCUS_TIME, TILE)
    HIHI = TILE_SPACE.update(SURFACE, FOCUS_TIME, MAX.__contains__(1))
    ALTITUDE += HIHI[0]
    SCROLL = SCROLL * HIHI[1]
    FOCUS_TIME = TIME.update(SURFACE, ALTITUDE)

    pygame.display.update()
    CLOCK.tick(40)

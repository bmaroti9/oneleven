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

CLOUDMAP = Cloudmap(SURFACE)
TIME = Time()
EVENTMAP = Eventmap()

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
            SCROLL += event.y * 34 #0.95
            if not MAX.__contains__(1):
                SCROLLING = 1
    
    if detect_click_rect(0, Rect(27, SURFACE.get_height() - 110, 140, SURFACE.get_height() - 25)):
        pass
    elif check_released(0):
        TILE_SPACE.add_tile(FOCUS_TIME + find_end_altitude(-SMOOTH_SCROLL))
        print(find_end_altitude(SMOOTH_SCROLL))
        
    #SCROLL = SCROLL * 0.965
    SMOOTH_SCROLL += (SCROLL - SMOOTH_SCROLL) * 0.4
    ALTITUDE += SMOOTH_SCROLL
    SCROLL -= sign_function(SCROLL)
    MAX.append(SCROLLING)

    del MAX[0]

    SURFACE.fill(get_colors()[0])

    if not MAX.__contains__(1) and abs(SMOOTH_SCROLL) > 0.1:
        x = find_end_altitude(SMOOTH_SCROLL)
        requested_altitude = TILE_SPACE.any_close(x, FOCUS_TIME)
        if requested_altitude != None:
            SCROLL += change_speed(SMOOTH_SCROLL, requested_altitude)
    
    TILE_SPACE.update(SURFACE, FOCUS_TIME, SMOOTH_SCROLL)
    FOCUS_TIME = TIME.update(SURFACE, ALTITUDE)

    pygame.display.update()
    CLOCK.tick(40)

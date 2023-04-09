import pygame
from pygame.locals import *
from datetime import datetime
import time

from clouds import *
from helpers import *
from tiles import *
from apps import *
from managers import *

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEWHEEL])

SCREEN_WIDTH = 1364
SCREEN_HEIGHT = 715

print(pygame.font.get_fonts())

CLOCK = pygame.time.Clock()

SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("©2022 Dragon tail")

ALTITUDE = 0.01
SCROLL = 0
SMOOTH_SCROLL = 0
MAX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
FOCUS_TIME = 0
RUNNING = True

TILE_SPACE = Tile_space()
DIRECTORY_MANAGER = Directory_manager()
DIRECTORY_MANAGER.load_directory(TILE_SPACE)

APPS = [Folder, Unloadable, Image_viewer]

#for n in range(10):
 #   TILE_SPACE.add_tile(FOCUS_TIME + n * 660, APPS[1])

while RUNNING:
    SCROLLING = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
        if event.type == KEYDOWN:
            if event.key == K_q:
                RUNNING = False
            elif event.key == K_0:
                set_theme(0)
            elif event.key == K_1:
                set_theme(1)
            elif event.key == K_2:
                set_theme(2)
            elif event.key == K_3:
                set_theme(3)
            elif event.key == K_9:
                random_theme()
        if event.type == pygame.MOUSEWHEEL:
            if abs(SCROLL) < 130:
                SCROLL += event.y * 28 #10
            if not MAX.__contains__(1):
                SCROLLING = 1

    SMOOTH_SCROLL += (SCROLL - SMOOTH_SCROLL) * 0.4
    ALTITUDE += SMOOTH_SCROLL
    SCROLL -= sign_function(SCROLL)
    MAX.append(SCROLLING)

    del MAX[0]

    SURFACE.fill(get_colors()[0])

    if not MAX.__contains__(1) and abs(SMOOTH_SCROLL) > 0.2:
        x = find_end_altitude(SMOOTH_SCROLL)
        requested_altitude = TILE_SPACE.any_close(x, ALTITUDE)
        if requested_altitude != None:
            SCROLL += change_speed(SMOOTH_SCROLL, requested_altitude)

    TILE_SPACE.update(SURFACE, ALTITUDE, SMOOTH_SCROLL)
    DIRECTORY_MANAGER.update(SURFACE, TILE_SPACE)

    pygame.display.update()
    CLOCK.tick(65)

import pygame
from pygame.locals import *
from datetime import datetime, date
import time

from clouds import *
from helpers import *
from tiles import *
from apps import *
from managers import *
from inputs import *
from settings import *

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEWHEEL])

SCREEN_WIDTH = 1440 * 1
SCREEN_HEIGHT = 900 * 1

print(pygame.font.get_fonts())

CLOCK = pygame.time.Clock()

#SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN, pygame.SCALED)
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.SCALED | pygame.FULLSCREEN)

SURFACE.fill(get_colors()[0])
blit_image(SURFACE, 'images/eternal_whole.png', [SURFACE.get_width() / 2, SURFACE.get_height() / 2], 0.5)
pygame.display.update()

pygame.time.delay(1500)
frame_set(CLOCK.tick(65))

pygame.display.set_caption("©2022-2023 Eternal")

full_set_initialize(SURFACE)
ALTITUDE = 0
SCROLL = 0
SMOOTH_SCROLL = 0
MAX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

events = pygame.event.get()
upload_event(events)

TILE_SPACE = Tile_space()
DIRECTORY_MANAGER = Directory_manager()
DIRECTORY_MANAGER.load_directory(TILE_SPACE)

frame_set(CLOCK.tick(65))

RUNNING = True
while RUNNING:
    SCROLLING = 0
    events = pygame.event.get()
    upload_event(events)
    for event in events:
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
            if abs(SCROLL) < 150:
                SCROLL += event.y * SURFACE.get_height() / 42
                SCROLL = SCROLL * (1 - (full_set_get()[1] * 0.0003))
            if not MAX.__contains__(1):
                SCROLLING = 1
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                full_set_change()

    z = reload()
    if z != None:
        ALTITUDE = z
        SCROLLING = 1
        SMOOTH_SCROLL = 0
        SCROLL = 0

    SMOOTH_SCROLL += (SCROLL - SMOOTH_SCROLL) * 0.3
    ALTITUDE += SMOOTH_SCROLL * frame_get()
    SCROLL -= sign_function(SCROLL)
    MAX.append(SCROLLING)

    del MAX[0]

    SURFACE.fill(get_colors()[0])

    if not MAX.__contains__(1) and abs(SCROLL) > 0.2:
        x = find_end_altitude(SMOOTH_SCROLL)
        requested_altitude = TILE_SPACE.any_close(x, ALTITUDE)
        if requested_altitude != None:
            SCROLL += change_speed(SMOOTH_SCROLL, requested_altitude)

    TILE_SPACE.update(SURFACE, ALTITUDE, SMOOTH_SCROLL)
    DIRECTORY_MANAGER.update(SURFACE, TILE_SPACE, ALTITUDE)

    pygame.display.update()
    frame_set(CLOCK.tick(140))

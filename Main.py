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

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEWHEEL])

SCREEN_WIDTH = 1364
SCREEN_HEIGHT = 715

print(pygame.font.get_fonts())

CLOCK = pygame.time.Clock()

SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("©2022 Dragon tail")

ALTITUDE = 0
SCROLL = -28
SMOOTH_SCROLL = 0
MAX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

events = pygame.event.get()
upload_event(events)

TILE_SPACE = Tile_space()
DIRECTORY_MANAGER = Directory_manager()
DIRECTORY_MANAGER.load_directory(TILE_SPACE)
print(generate_number_from_string('hihi', 255))
#TILE_SPACE.add_tile(getmtime('hihi.eml'), 'hihi.eml')

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
            if abs(SCROLL) < 200:
                SCROLL += event.y * 17 #10
                SCROLL = SCROLL * 0.93
            if not MAX.__contains__(1):
                SCROLLING = 1
    SMOOTH_SCROLL += (SCROLL - SMOOTH_SCROLL) * 0.4
    ALTITUDE += SMOOTH_SCROLL
    SCROLL -= sign_function(SCROLL)
    MAX.append(SCROLLING)

    z = reload()
    if z != None:
        ALTITUDE = z + 300
        SMOOTH_SCROLL = 0
        SCROLL = -28

    del MAX[0]

    SURFACE.fill(get_colors()[0])

    if not MAX.__contains__(1) and abs(SMOOTH_SCROLL) > 0.2:
        x = find_end_altitude(SMOOTH_SCROLL)
        requested_altitude = TILE_SPACE.any_close(x, ALTITUDE)
        if requested_altitude != None:
            SCROLL += change_speed(SMOOTH_SCROLL, requested_altitude)

    TILE_SPACE.update(SURFACE, ALTITUDE, SMOOTH_SCROLL)
    DIRECTORY_MANAGER.update(SURFACE, TILE_SPACE, ALTITUDE)

    pygame.display.update()
    CLOCK.tick(65)

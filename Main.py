import math
import random
import sys
import pygame
from pygame.locals import *
import time
import json

from cards import *
from designs import *
from gradient import *
from helpers import *
from experimental import *

pygame.init()

FONT1 = pygame.font.SysFont('andalemono', 50)
FONT2 = pygame.font.SysFont("ubuntu", 30)
FONT3 = pygame.font.SysFont('nanumgothic', 25)
FONT4 = pygame.font.SysFont("ubuntu", 27)
FONT5 = pygame.font.SysFont('latinmodernmonoprop', 30)
FONT6 = pygame.font.SysFont('nanumgothic', 22)
FONT7 = pygame.font.SysFont("ubuntu", 36)

SCREEN_WIDTH = 350
SCREEN_HEIGHT = 600

print(pygame.font.get_fonts())

CLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("©2022 Dragon tail")

RUNNING = True

BLUR_SURF = colour_rect = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))         

#CLOUDMAP = Cloudmap(SURFACE)
#TIME = Time()
#EVENTMAP = Eventmap()
TIME_MAP = Time_map()

ALTITUDE = 0
SCROLL = 0
SMOOTH_SCROLL = 0
MAX = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

while RUNNING:
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
        if event.type == KEYDOWN:
            if event.key == K_q:
                RUNNING = False
        if event.type == pygame.MOUSEWHEEL:
            SCROLL += event.y * 2.4 #0.95
    '''
    if detect_click_rect(0, Rect(27, SURFACE.get_height() - 110, 140, SURFACE.get_height() - 25)):
            SCROLL = - ALTITUDE * 0.0309
            SMOOTH_SCROLL = 0
    elif check_released(0):
        EVENTMAP.add_event("balint", -ALTITUDE * 5 + SURFACE.get_height()  // 2)
    '''  
    
    SCROLL = SCROLL * 0.97
    SMOOTH_SCROLL += (SCROLL - SMOOTH_SCROLL) * 0.5
    ALTITUDE += SMOOTH_SCROLL
    MAX.append(abs(SMOOTH_SCROLL))

    del MAX[0]

    SURFACE.fill((253, 119, 33))
    BLUR_SURF.fill((253, 119, 33))

    TIME_MAP.update(SURFACE, ALTITUDE)    

    '''
    CLOUDMAP.update(BLUR_SURF, ALTITUDE)
    SURFACE.blit(blurSurf(BLUR_SURF, max(abs(SMOOTH_SCROLL) * 0.6, 1)), (0, 0))
    EVENTMAP.update(SURFACE, ALTITUDE, max(MAX))
    TIME.update(SURFACE, ALTITUDE)
    #SCROLL += circle_scroll(SURFACE) ** 3 * 0.000005
    '''

    pygame.display.update()
    CLOCK.tick(40)

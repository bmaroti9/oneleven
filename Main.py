import math
import random
import sys
import pygame
from pygame.locals import *
import time
import json

from elements import *
from designs import *
from gradient import *
from helpers import *

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

CLOUDMAP = Cloudmap(SURFACE)
TIME = Time()
EVENTMAP = Eventmap()

ALTITUDE = 0
SCROLL = 0

while RUNNING:
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
        if event.type == KEYDOWN:
            if event.key == K_q:
                RUNNING = False
        if event.type == pygame.MOUSEWHEEL:
            SCROLL += event.y * 0.90
    
    if detect_click_rect(0, Rect(27, SURFACE.get_height() - 110, 140, SURFACE.get_height() - 25)):
            SCROLL = - ALTITUDE * 0.03
    elif check_released(0):
        EVENTMAP.add_event("balint", -ALTITUDE)
            
    ALTITUDE += SCROLL
    SCROLL = SCROLL * 0.97

    SURFACE.fill((180, 180, 180))

    #gradientRect_h(SURFACE, (172, 198, 180), (180, 180, 180), 
     #           Rect(0, 0, SURFACE.get_width(), SURFACE.get_height()))


    EVENTMAP.update(SURFACE, ALTITUDE)
    CLOUDMAP.update(SURFACE, ALTITUDE)
    TIME.update(SURFACE, ALTITUDE)

    pygame.display.update()
    CLOCK.tick(40)

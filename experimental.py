import math
import random
import sys
import pygame
from pygame.locals import *
import time
import json

from helpers import *

pygame.init()

LAST_POINT = [0, 0]
LAST_ANGLE = 0

def circle_scroll(surface):
    global LAST_POINT, LAST_ANGLE
    pos = pygame.mouse.get_pos()
    optimal_point = [surface.get_width() // 2, 400]
    
    pygame.draw.circle(surface, (200, 0, 0), optimal_point, 4)
    
    angle = calculate_angle(optimal_point, pos)
    off_center = rotating_position(0, 100, angle, pos)

    pygame.draw.line(surface, (250, 250, 0), pos, off_center, 2)
    pygame.draw.circle(surface, (0, 0, 250), off_center, 4)

    x = (calculate_angle(LAST_POINT, pos)) % 360
    change = x - LAST_ANGLE

    if 180 < change:
        change -= 360
    elif -180 > change:
        change += 360

    LAST_ANGLE = x
    LAST_POINT = off_center

    return change


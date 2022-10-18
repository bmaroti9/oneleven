import pygame
import math
from pygame.locals import*
import time
import random
import sys
import json
from gradient import blurSurf, sin_pos
from datetime import datetime


from helpers import *

pygame.init()

with open("times.txt", "r") as f:
    TIMES = json.load(f)

def rombus(rect, color, surface):
    width = rect[0] + rect[2]
    height = rect[1] + rect[3]
    height_half = rect[1] + rect[3] // 2
    width_half = rect[0] + rect[2] // 2
    points = [[width_half, rect[1]], [width, height_half], [width_half, height], [rect[0], height_half]]
    pygame.draw.polygon(surface, color, points)

def draw_rombuses(surface, color, width, height, pos_add):
    xnumber = surface.get_width() // width + 3
    ynumber = surface.get_height() // height + 3

    addon = -height // 2

    for y in range(ynumber):
        for x in range(xnumber):
            addon = -addon
            rombus([x * (width / 2 + 50),y * (height / 2 + 100) + \
                    addon - 500 + pos_add % (height + 200), width, height], color, surface)
            rombus([x * (width / 2 + 50) - 10, y * 
                    (height / 2 + 100) + addon - 505 + pos_add % (height + 200), width, height], 
                    transition_colors(color, (250, 250, 250), 0.4), surface)
import pygame
import math
from pygame.locals import*
import time
import random
import sys
import json
from gradient import blurSurf, sin_pos
from datetime import datetime
from screen_shake import *


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
    xnumber = surface.get_width() // width + 2
    ynumber = surface.get_height() // height + 2

    for y in range(ynumber):
        for x in range(xnumber):
            rombus([x * width - 52 + pos_add[0], (y - 1) * height - 25 + pos_add[1] % height, 
                    width, height], transition_colors(color, (0, 0, 0), 0.2), surface)
            
            rombus([x * width - 52 + pos_add[0], (y - 1) * height - 25 + pos_add[1] % height, 
                    width - 5, height - 8], color, surface)

class Time_map(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()        

        self.smooth_pos = 0
    
    def update(self, surface, altitude):
        self.smooth_pos += (altitude - self.smooth_pos) * 0.4

        draw_rombuses(surface, (227, 78, 30), 90, 130, [0, self.smooth_pos])

import math
import random
import sys
import pygame
from pygame.locals import *
import time
import json

from helpers import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        super().__init__()     

        self.text = text
        self.font = pygame.font.SysFont('comicsansms', 70)
        self.fixed_pos = pos
        self.pos = pos
        self.size = 50
    
    def update(self, surface, altitude, closest, speed):
        change_altitude = 0

        real_pos = self.pos + altitude
        target = surface.get_height() // 2
        distance = target - real_pos
        
        wanted = surface.get_width() - 150
        if distance != 0 and abs(distance) < 300:
            if closest == self:
                change_altitude += (distance * min(max(0.08, 18 / abs(distance)), 1.1))
                distance -= change_altitude
            if distance != 0:
                wanted = max(min((920 / (abs(distance) ** 2)), surface.get_width() - 150), 190)
        elif abs(distance) > 300:
            wanted = 190
            
        self.size += (wanted - self.size) * 0.1

        coolsize = self.size * 1.1
        coolheight = self.size * 0.26

        color = transition_colors((30, 51, 190), (9, 20, 50), 
                (abs(self.size - 500)) / 500)

        pygame.draw.rect(surface, color, Rect(coolsize, real_pos - coolheight, 
            surface.get_width() - coolsize * 2, coolheight * 2), 0, int(5 - 0.003 * self.size))

        return change_altitude

    def draw_content(self, pos):
        x = 0


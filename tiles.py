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
    
    def update(self, surface, altitude,  closest):
        real_pos = self.pos + altitude * 5
        target = surface.get_height() // 2
        distance = target - real_pos
        
        if distance != 0:
            if closest == self:
                self.pos += distance * min(max(0.09, 7 / abs(distance)), 1.1)

            wanted = max(min((1000 / (abs(distance) ** 2)), surface.get_width() - 150), 150)
        else:
            wanted = surface.get_width() - 150
         
        self.size += (wanted - self.size) * 0.1

        coolsize = self.size * 1.1
        coolheight = self.size * 0.26

        color = transition_colors((9, 20, 60), (63, 78, 232), 
                self.size / (surface.get_height() // 2))

        pygame.draw.rect(surface, (9, 20, 60), Rect(coolsize, real_pos - coolheight, 
            surface.get_width() - coolsize * 2, coolheight * 2), 0, int(47 - 0.0375 * self.size))

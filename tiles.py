import math
import random
import sys
import pygame
from pygame.locals import *
import time
import json

from helpers import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, time_point):
        super().__init__()     

        self.time = time_point
        self.size = 1000
        self.pos = 0

        self.title_font = pygame.font.SysFont('texgyreadventor', 20)

    def update(self, surface, focus_time, closest):
        real_pos = focus_time - self.time
        
        change_altitude = 0

        #real_pos = self.pos + altitude
        target = surface.get_height() // 2
        distance = target - real_pos
        
        wanted = 1215
        if distance != 0 and abs(distance) < 350:
            #if closest == self:
            change_altitude = (distance * min(max(0.09, 20 / abs(distance)), 1))
            if abs(distance) < 30:
                change_altitude = distance * 1.1

            wanted = max(1000, 1215 / max(abs(distance - change_altitude), 1))
        elif abs(distance) > 300:
            wanted = 1000
            
        self.size += (wanted - self.size) * 0.28

        coolsize = self.size * 1.1
        coolheight = self.size * 0.33 - 80

        color = transition_colors(get_colors()[1], get_colors()[2], 
                (abs(self.size - 1180)) / 380)

        pygame.draw.rect(surface, color, Rect(coolsize, real_pos - coolheight, 
            surface.get_width() - coolsize * 2, coolheight * 2), 0, int(1 - 0.00 * (self.size - 1000)))
        
        self.draw_content(surface, real_pos - coolheight - 5, surface.get_width() - coolsize,
                             min(1, 30 / (1215 - self.size)), color)

        return change_altitude

    def draw_content(self, surface, top, side, vis, tile_color):
        if vis > 0.06:
            c1 = transition_colors(tile_color, get_colors()[3], vis)
            c2 = transition_colors(tile_color, get_colors()[4], vis)
            blit_text(surface, c1, 'new tab', [surface.get_width() / 2, top], 
                        self.title_font, 3)
            blit_text(surface, c2, 'chromium', [side + 20, top], 
                        self.title_font, 0)

class Tile_space(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.tiles = []
    
    def add_tile(self, focus_time):
        x = Tile(focus_time + 3)
        self.tiles.append(x)
    
    def update(self, surface, focus_time):
        alt_change = 0
        for n in self.tiles:
            alt_change += n.update(surface, focus_time + 360, 0)

        return alt_change * 0.88

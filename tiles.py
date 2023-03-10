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
        self.wanted = 1200

        self.title_font = pygame.font.SysFont('texgyreadventor', 20)

    def size_adjust(self, surface, distance, smooth_scroll):
        self.wanted = 1215
        if abs(distance) > surface.get_height() / 2 or smooth_scroll > 30:
            self.wanted = 950

    def update(self, surface, focus_time, smooth_scroll):
        real_pos = focus_time - self.time
        target = surface.get_height() // 2
        distance = target - real_pos + 3

        self.size_adjust(surface, distance, smooth_scroll)

        if distance < surface.get_height() * 1.7:
            self.size += (self.wanted - self.size) * 0.22
            self.texture(surface, real_pos)
    
    def texture(self, surface, real_pos):
        coolsize = self.size * 1.1
        coolheight = self.size * 0.33 - 80

        color = transition_colors(get_colors()[1], get_colors()[2], 
                (abs(self.size - 1180)) / 300)

        pygame.draw.rect(surface, color, Rect(coolsize, real_pos - coolheight, 
            surface.get_width() - coolsize * 2, coolheight * 2), 0, int(1 - 0.00 * (self.size - 1000)))
        
        self.draw_content(surface, real_pos - coolheight - 5, surface.get_width() - coolsize,
                             min(1, 30 / (1215 - self.size)), color)

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
        x = Tile(focus_time)
        self.tiles.append(x)
    
    def any_close(self, est_time, focus_time):
        requested_altitude = None
        for n in self.tiles:
            real_pos = focus_time - n.time
            if abs(real_pos - est_time) < 200:
                requested_altitude = real_pos
        return requested_altitude

    def update(self, surface, focus_time, smooth_scroll):
        for n in self.tiles:
            n.update(surface, focus_time + 360, smooth_scroll)
            

def marker(pos, surface):
    real_pos = pos + surface.get_height() // 2
    pygame.draw.circle(surface, (250, 0, 250), [20, surface.get_height() // 2], 5)
    pygame.draw.circle(surface, (250, 250, 250), [20, real_pos], 5)

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

    def size_adjust(self, surface, focus_time):
        real_pos = focus_time - self.time
        target = surface.get_height() // 2
        distance = target - real_pos + 3
        
        self.wanted = 1215
        if abs(distance) > 300:
            self.wanted = 950

    def update(self, surface, focus_time):
        self.size += (self.wanted - self.size) * 0.22
        real_pos = focus_time - self.time
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
    
    def any_close(self, est_time, surface, speed):
        change_speed = 0
        for n in self.tiles:
            x = est_time + (surface.get_height() / 2) - n.time
            if abs(x) < 200:
                change_speed += x * 0.0002
        return change_speed

    def refine(self, focus_time):
        change_altitude = 0
        for n in self.tiles:
            real_pos = focus_time - n.time
            if abs(real_pos) < 0:
                change_altitude -= real_pos * 0.2
        return change_altitude
    
    def update(self, surface, focus_time, smooth_scroll):
        if abs(smooth_scroll) > 18:
            for n in self.tiles:
                n.wanted = 950
                n.update(surface, focus_time + 360)
        else:
            for n in self.tiles:
                n.size_adjust(surface, focus_time + 360)
                n.update(surface, focus_time + 360)

def marker(pos, surface):
    real_pos = pos + surface.get_height() // 2
    pygame.draw.circle(surface, (250, 0, 250), [20, surface.get_height() // 2], 5)
    pygame.draw.circle(surface, (250, 250, 250), [20, real_pos], 5)

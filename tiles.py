import math
import random
import sys
import pygame
from pygame.locals import *
import time
import json

from helpers import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, time_point, app = 0):
        super().__init__()     

        self.app = app

        self.time = time_point
        self.size = 950
        self.pos = 0
        self.wanted = 1200
        #self.image = pygame.image.load("images/air_balloon1.png")  

        self.title_font = pygame.font.SysFont('texgyreadventor', 20)

    def size_adjust(self, surface, distance, smooth_scroll):
        self.wanted = 1215  #1215
        if abs(distance) > surface.get_height() / 2 or abs(smooth_scroll) > 24:
            self.wanted = 1050 - abs(distance) * 0.2

    def update(self, surface, focus_time, smooth_scroll):
        real_pos = focus_time - self.time
        target = surface.get_height() // 2
        distance = target - real_pos + 3

        self.size_adjust(surface, distance, smooth_scroll)

        if abs(distance) < surface.get_height() * 1.3:
            #self.texture(surface, real_pos + smooth_scroll, smooth_scroll * 0.3)
            self.size += (self.wanted - self.size) * 0.17
            self.texture(surface, real_pos)
    
    def texture(self, surface, real_pos):
        coolsize = self.size * 1.1
        coolheight = self.size * 0.33 - 80
        
        color = transition_colors(get_colors()[1], get_colors()[2], 
                    (abs(self.size - 1180)) / 200)

        pygame.draw.rect(surface, color, Rect(coolsize, real_pos - coolheight, 
            surface.get_width() - coolsize * 2, coolheight * 2), 0, 1)
        
    
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
    
    def add_tile(self, focus_time, app):
        x = Tile(focus_time, app)
        self.tiles.append(x)
    
    def any_close(self, est_time, focus_time):
        requested_altitude = None
        for n in self.tiles:
            real_pos = focus_time - n.time
            if abs(real_pos - est_time) < 300:
                requested_altitude = real_pos
        return requested_altitude

    def update(self, surface, focus_time, smooth_scroll):
        for n in self.tiles:
            n.update(surface, focus_time + 360, smooth_scroll)
            

def marker(pos, surface):
    real_pos = pos + surface.get_height() // 2
    pygame.draw.circle(surface, (250, 0, 250), [20, surface.get_height() // 2], 5)
    pygame.draw.circle(surface, (250, 250, 250), [20, real_pos], 5)

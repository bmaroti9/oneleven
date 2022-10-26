import math
import random
import sys
import pygame
from pygame.locals import *
import time
import json

from designs import *
from gradient import *
from helpers import *
from experimental import *

SCREEN_WIDTH = 350
SCREEN_HEIGHT = 600


CLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("©2022 Dragon tail")

class Cloud(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()            
        
        self.distance = random.randint(30, 1000)
        self.width = max(random.randint(270, 900), self.distance)
        
        self.image = pygame.Surface((self.width, self.distance))  
        self.image.set_colorkey((0, 0, 0))

        #gray = gray_color(min(max(self.distance // 1.3 - 100, 100), 250))
        gray = transition_colors((250, 250, 250), (100, 100, 100), 150 / self.distance)

        magic_number = 18
        
        for _ in range(magic_number):
            x = random.randint(round(self.width * 0.18), round(self.width * 0.82))  
            y = random.randint(round(self.distance * 0.4), round(self.distance * 0.5)) 
            height = random.randint(round(self.distance * 0.05), round(self.distance * 0.10))

            pygame.draw.ellipse(self.image, gray, Rect(x, y, self.width // magic_number * 3.5, height))
        
        x = random.randint(-self.width // 2, surface.get_width() -self.width // 2)
        y = random.randint(-self.distance * 15, surface.get_height() + self.distance * 15)

        self.original_x = x
        self.original_y = y

    def get_distance(self):
        return self.distance

    def update(self, surface, altitude):
        surface.blit(self.image, 
                [self.original_x, self.original_y + altitude * (self.distance // 13 ** 2)])
        

class Cloudmap(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.clouds = pygame.sprite.Group()

        for _ in range(100):
            self.clouds.add(Cloud(surface))
        
        self.clouds.add(Rocket(surface))

        self.clouds = sorted(self.clouds, key=Cloud.get_distance) 

    def update(self, surface, altitude):
        for n in self.clouds:
            n.update(surface, altitude)

class Rocket(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()       

        self.image = pygame.image.load("images/rocket_1.png").convert_alpha(surface)
        self.image = pygame.transform.rotozoom(self.image, 0, 0.38)
        self.distance = 700

    def update(self, surface, altitude):
        surface.blit(self.image, [0, 0])   

ALTITUDE = 0
SMOOTH_SCROLL = 0
SCROLL = 0
CLOUDMAP = Cloudmap(SURFACE)
MAX = [0, 0, 0, 0, 0]
RUNNING = True

while RUNNING:
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
        if event.type == KEYDOWN:
            if event.key == K_q:
                RUNNING = False
        if event.type == pygame.MOUSEWHEEL:
            SCROLL += event.y * 2.4 #0.95
    
    SCROLL = SCROLL * 0.97
    SMOOTH_SCROLL += (SCROLL - SMOOTH_SCROLL) * 0.5
    ALTITUDE += SMOOTH_SCROLL
    MAX.append(abs(SMOOTH_SCROLL))

    del MAX[0]


    SURFACE.fill((210, 225, 235))

    CLOUDMAP.update(SURFACE, ALTITUDE)

    pygame.display.update()
    CLOCK.tick(40)

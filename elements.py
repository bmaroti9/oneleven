import pygame
import math
from pygame.locals import*
import time
import random
import sys
import json
from gradient import sin_pos

from helpers import *

pygame.init()


class Cloud(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        
        self.distance = random.randint(20, 500)

        self.image = pygame.Surface((self.distance, self.distance))   
        self.image.set_colorkey((0, 0, 0))

        gray = gray_color(max(self.distance // 2 - 50, 20))
        for _ in range(18):
            x = random.randint(round(self.distance * 0.16), round(self.distance * 0.84))  
            y = random.randint(round(self.distance * 0.4), round(self.distance * 0.5)) 
            radius = random.randint(round(self.distance * 0.05), round(self.distance * 0.10))

            pygame.draw.circle(self.image, gray, [x, y], radius)
        
        x = random.randint(-self.distance // 2, surface.get_width() -self.distance // 1000)
        y = random.randint(-10000, 10000)

        self.original_x = x
        self.original_y = y

    def get_distance(self):
        return self.distance

    def update(self, surface, altitude):
        surface.blit(self.image, [self.original_x, self.original_y + altitude * (self.distance // 40)])
        

class Cloudmap(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.clouds = pygame.sprite.Group()

        for _ in range(200):
            self.clouds.add(Cloud(surface))
        
        self.clouds.add(Balloon(surface))

        self.clouds = sorted(self.clouds, key=Cloud.get_distance) 

    def update(self, surface, altitude):
        for n in self.clouds:
            n.update(surface, altitude)


class Balloon(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.distance = 450
        self.image = pygame.image.load("images/balloon.png").convert_alpha(surface)
        self.image = pygame.transform.rotozoom(self.image, 0, 0.3)
        self.rect = self.image.get_rect()
    
    def update(self, surface, altitude):
        y = math.sin(altitude / 30) * 20     # scale sine wave
        y = int(y)

        self.rect.center = [surface.get_width() // 2 + y, 
                    surface.get_height() // 2 - altitude // 4]
        
        surface.blit(self.image, self.rect)

        
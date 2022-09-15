import pygame
import math
from pygame.locals import*
import time
import random
import sys
import json
from gradient import blurSurf, sin_pos

from helpers import *

pygame.init()


class Cloud(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()            
        
        self.distance = random.randint(30, 1000)
        self.width = max(random.randint(270, 900), self.distance)
        
        self.image = pygame.Surface((self.width, self.distance))  
        self.image.set_colorkey((0, 0, 0))

        #gray = gray_color(min(max(self.distance // 1.3 - 100, 100), 250))
        gray = transition_colors((250, 250, 250), (226, 116, 139), 150 / self.distance)

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
        
        self.clouds.add(Balloon(surface))

        self.clouds = sorted(self.clouds, key=Cloud.get_distance) 

    def update(self, surface, altitude):
        for n in self.clouds:
            n.update(surface, altitude)


class Balloon(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.distance = 700
        self.image = pygame.image.load("images/balloon.png").convert_alpha(surface)
        self.image = pygame.transform.rotozoom(self.image, 0, 0.25)
        self.rect = self.image.get_rect()
    
    def update(self, surface, altitude):
        y = math.sin(altitude / 30) * 20     # scale sine wave
        y = int(y)

        self.rect.center = [surface.get_width() // 2 + y, 
                    surface.get_height() // 2 - altitude // 4]
        
        surface.blit(self.image, self.rect)

        
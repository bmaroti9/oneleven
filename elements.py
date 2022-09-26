from os import posix_fadvise
from re import I
import pygame
import math
from pygame.locals import*
import time
import random
import sys
import json
from gradient import blurSurf, sin_pos
from datetime import datetime


from helpers import *

pygame.init()

with open("times.txt", "r") as f:
    TIMES = json.load(f)


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
        self.image = pygame.image.load("images/balloon2.png").convert_alpha(surface)
        self.image = pygame.transform.rotozoom(self.image, 0, 0.25)
        self.rect = self.image.get_rect()
    
    def update(self, surface, altitude):
        y = math.sin(altitude / 100) * 40     # scale sine wave
        y = int(y)

        self.rect.center = [surface.get_width() // 2 + y, 
                    surface.get_height() // 2 - altitude // 15]
        
        surface.blit(self.image, self.rect)
    
class Time(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.time_font = pygame.font.SysFont('texgyreadventor', 50)
        self.day_font = pygame.font.SysFont('texgyreadventor', 30)
        self.test_font = pygame.font.SysFont('texgyreadventor', 30)
    

    def update(self, surface, altitude):
        now = datetime.now()

        current_hour = int(now.strftime("%H"))
        current_hour = now.weekday() * 24 + current_hour
        current_time_minutes = current_hour * 60 + int(now.strftime("%M"))  
        current_time_minutes += round(altitude)
        
        minutes = current_time_minutes % 60
        hours = ((current_time_minutes - minutes) // 60) % 24
        day = TIMES["days"][(current_time_minutes - hours - minutes) // 1440 % 7]

        blit_text(surface, (73, 158, 130), "{0:0=2d}".format(hours) + ":" + "{0:0=2d}".format(minutes), 
                [35, surface.get_height() - 130], self.time_font)
        
        blit_text(surface, (73, 158, 130), day, 
                [35, surface.get_height() - 70], self.day_font)
        
        blit_text(surface, (73, 158, 130), day, 
                [35, surface.get_height() - 70], self.day_font)

        a = max(110 - abs(altitude * 3), 40 - math.sqrt(abs(altitude)) * 0.3)
        
        pygame.draw.line(surface, (158, 62, 84), 
            [27, surface.get_height() - a], [27, surface.get_height() - 25], 3)
    

class Floating_event(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        super().__init__()     

        self.text = text
        self.font = pygame.font.SysFont('comicsansms', 70)
        self.pos = pos
    
    def update(self, surface, altitude, scroll):
        pos = self.pos + altitude * 2
        size = max((300 / max((abs(scroll) ** 2.5) * 0.2, 1)), 45)
        
        pygame.draw.rect(surface, (83, 178, 140), 
                Rect(20, pos - size, surface.get_width() - 40, size * 2), 0, int(47 - 0.075 * size))


class Eventmap(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  

        self.events = pygame.sprite.Group()
    
    def add_event(self, text, pos):
        self.events.add(Floating_event(text, pos))

    def update(self, surface, altitude, scroll):
        for n in self.events:
            n.update(surface, altitude, scroll)
        
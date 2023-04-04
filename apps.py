import pygame
import math
from pygame.locals import*
import time
import random
import sys
import json

from helpers import *
from datetime import datetime

class Folder(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        self.name = 'Workspace'
        self.contents = ['Hihi', 'Hehe', 'Huhu', 'Höhö', 'Haha']
        self.colors = []
        self.points = []
        self.font = pygame.font.SysFont('texgyreadventor', 60)
        self.font_200 = pygame.font.SysFont('texgyreadventor', 200)

        for n in self.contents:
            self.colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self.points.append(random.randint(0, surface.get_width()))
        self.points = sorted(self.points)
        self.points[0] = 0
        self.surf = pygame.Surface((surface.get_width(), surface.get_height()))
        self.surf.fill((0, 0, 0))
        for n in range(len(self.contents)):
            pygame.draw.rect(self.surf, self.colors[n], 
                Rect(self.points[n], 0, self.surf.get_width() - self.points[n], self.surf.get_height()))
            #c = self.colors[(n + 1) % len(self.colors)]
            c = [255 - self.colors[n][0], 255 - self.colors[n][1], 255 - self.colors[n][2]]
            wrighting = self.font.render(self.contents[n], True, c)
            wrighting = pygame.transform.rotozoom(wrighting, -90, 0.8)
            self.surf.blit(wrighting, [self.points[n], 0])
        blit_text(self.surf, c, self.name, [0, 300], self.font_200, 0)
            
        self.surf = self.surf.convert_alpha()

    
    def update(self, surface):
        surface.fill((0, 0, 0))
        surface.blit(self.surf, [0, 0])
        

class Image_viewer(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.image = pygame.image.load("images/black_and_white" + str(random.randint(1, 12)) + ".png")
        scalex = surface.get_width() / self.image.get_width()
        scaley = surface.get_height() / self.image.get_height()
        zoom = min(scalex, scaley)
        self.image = pygame.transform.rotozoom(self.image, 0, zoom)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [surface.get_width() / 2, surface.get_height() / 2]
    
    def update(self, surface):
        surface.fill((200, 200, 200))
        surface.blit(self.image, self.rect)

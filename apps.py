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
        self.contents = ['Hihi', 'Hehe', 'Huhu', 'Höhö', 'Haha']
        self.colors = []
        self.points = []
        for n in self.contents:
            self.colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            self.points.append(random.randint(0, surface.get_width()))
        self.points = sorted(self.points)
        self.points[0] = 0
    
    def update(self, surface):
        surface.fill((0, 0, 0))
        for n in range(len(self.contents)):
            pygame.draw.rect(surface, self.colors[n], 
                    Rect(self.points[n], 0, surface.get_width() - self.points[n], surface.get_height()))

class Image_viewer(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.image = pygame.image.load("images/black_and_white" + str(random.randint(1, 12)) + ".png")
        scalex = surface.get_width() / self.image.get_width()
        scaley = surface.get_height() / self.image.get_height()
        zoom = min(scalex, scaley)
        self.image = pygame.transform.rotozoom(self.image, 0, zoom).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [surface.get_width() / 2, surface.get_height() / 2]
    
    def update(self, surface):
        surface.fill((200, 200, 200))
        surface.blit(self.image, self.rect)

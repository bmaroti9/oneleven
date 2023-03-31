import pygame
import math
from pygame.locals import*
import time
import random
import sys
import json

from helpers import *

class Image_viewer(pygame.sprite.Sprite):
    def __init__(self, surface, image):
        super().__init__()

        self.image = pygame.image.load(image)
        scalex = surface.get_width() / self.image.get_width()
        scaley = surface.get_height() / self.image.get_height()
        zoom = min(scalex, scaley)
        self.image = pygame.transform.rotozoom(self.image, 0, zoom).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [surface.get_width() / 2, surface.get_height() / 2]
    
    def update(self, surface):
        surface.fill((200, 200, 200))
        surface.blit(self.image, self.rect)
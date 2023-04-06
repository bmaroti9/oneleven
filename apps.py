import pygame
from pygame.locals import*
import random
from os import listdir
from os.path import isfile, join, basename

from helpers import *
from gradient import uniform_colors


class Folder(pygame.sprite.Sprite):
    def __init__(self, surface, path):
        super().__init__()
        self.name = basename(path)
        self.contents = listdir(path)
        if len(self.contents) > 9:
            self.contents = self.contents[:9]
        self.contents = self.shorten(self.contents)

        self.colors = uniform_colors(len(self.contents))
        self.points = []
        self.font = pygame.font.SysFont('texgyreadventor', 120)
        self.font_200 = pygame.font.SysFont('texgyreadventor', 200)

        for n in self.contents:
            self.points.append(random.randint(0, surface.get_width()))
        self.points.append(surface.get_width())

        self.points = sorted(self.points)
        self.points[0] = 0
        self.surf = pygame.Surface((surface.get_width(), surface.get_height()))
        self.surf.fill((0, 0, 0))
        c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for n in range(len(self.contents)):
            pygame.draw.rect(self.surf, self.colors[n], 
                Rect(self.points[n], 0, self.surf.get_width() - self.points[n], self.surf.get_height()))
            c = [255 - self.colors[n][0], 255 - self.colors[n][1], 255 - self.colors[n][2]]
            wrighting = self.font.render(self.contents[n], True, c)
            
            width = self.points[n + 1] - self.points[n]
            zoomx = min(width / wrighting.get_height(), 70 / wrighting.get_height())
            wrighting = pygame.transform.rotozoom(wrighting, -90, zoomx)
            self.surf.blit(wrighting, [self.points[n], 0])
        blit_text(self.surf, c, self.name, [0, 300], self.font_200, 0)
            
        self.surf = self.surf.convert_alpha()
    
    def shorten(self, texts):
        for n in range(len(texts)):
            if len(texts[n]) > 12:
                texts[n] = texts[n][:12]
                texts[n] += '...'
        return texts
    
    def update(self, surface):
        surface.fill((0, 0, 0))
        surface.blit(self.surf, [0, 0])
        
class Unloadable(pygame.sprite.Sprite):
    def __init__(self, surface, path):
        super().__init__()

        self.font_200 = pygame.font.SysFont('texgyreadventor', 200)
        self.name = basename(path)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.surf = pygame.Surface((surface.get_width(), surface.get_height()))
        self.surf.fill(self.color)
        c = [255 - self.color[0], 255 - self.color[1], 255 - self.color[2]]
        blit_text(self.surf, c, self.name, [0, 300], self.font_200, 0)
        self.surf = self.surf.convert_alpha()
    
    def update(self, surface):
        surface.fill((0, 0, 0))
        surface.blit(self.surf, [0, 0])

class Image_viewer(pygame.sprite.Sprite):
    def __init__(self, surface, path):
        super().__init__()

        print(path)
        self.image = pygame.image.load(path)
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

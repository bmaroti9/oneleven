import pygame
import math
from pygame.locals import*
import time
import random
import sys
import json

from helpers import *

pygame.init()

def generate_cloud(size):
    surface = pygame.Surface((size, size))   
    gray = gray_color(random.randint(70, 250))
    for _ in range(15):
        x = random.randint(round(size * 0.16), round(size * 0.84))  
        y = random.randint(round(size * 0.4), round(size * 0.5)) 
        radius = random.randint(round(size * 0.05), round(size * 0.15))

        pygame.draw.circle(surface, gray, [x, y], radius)
    
    return surface

CLOUDS = pygame.sprite.Group()

def generate_cloudmap():
    global CLOUDS

    CLOUDS = []
    CLOUDS = pygame.sprite.Group()

    for _ in range(50):
        a = []
        distance = random.randint(100, 400)

        a.add(generate_cloud())
        
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

image = pygame.image.load("images/black_and_white3.png")  
original_array = pygame.surfarray.array3d(image)
color_array = pygame.surfarray.array3d(image)
black = pygame.Surface((image.get_width(), image.get_height()))      
array = pygame.surfarray.array3d(black)
width, height, _ = array.shape
'''
for y in range(height):
    for x in range(width):
        border = original_array[x, y, 0]

        randi = random.randint(0, 250)

        if randi > border:
            z = 250
        else:
            z = 0
        
        array[x, y, 0] = z
        array[x, y, 1] = z
        array[x, y, 2] = z
'''

SCREEN_WIDTH = width
SCREEN_HEIGHT = height

POINTS = []

FONT1 = pygame.font.SysFont('texgyrechorus', 47)

CLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

SURFACE.blit(pygame.surfarray.make_surface(array), (0, 0))

pygame.display.set_caption("©2022 Dragon tail")

def list_all_offset(offset):
    options = []

    for x in range(-offset, offset):
        options.append([x, offset])
        options.append([x, -offset])
    
    for y in range(-offset, offset):
        options.append([offset, y])
        options.append([-offset, y])
    
    if offset == 0:
        options.append([0, 0])

    return options


def list_values(offset, array, pos):
    z = []
    
    x = list_all_offset(offset)

    for n in x:
        hihi = [pos[0] + n[0], pos[1] + n[1]]

        eggyik = hihi[0] > -1 and hihi[0] < SCREEN_WIDTH
        másik =  hihi[1] > -1 and hihi[1] < SCREEN_HEIGHT

        if eggyik and másik:
            z.append(array[hihi[0], hihi[1], 0])

    return z


def find_closest(array, search, pos):
    offset = 7

    while True:
        z = list_values(offset, array, pos)

        if z.__contains__(search):
            return offset

        if offset == 0:
            return 0
        
        offset -= 1

def set_gray(original_array, d_array, pos):
    eggyik = pos[0] > -1 and pos[0] < SCREEN_WIDTH
    másik =  pos[1] > -1 and pos[1] < SCREEN_HEIGHT
    
    if eggyik and másik:
        want = original_array[pos[0], pos[1], 0]
        
        black = find_closest(d_array, 0, pos)
        white = find_closest(d_array, 250, pos)

        first = (10 * 0 + white * 250) / (10 + white)

        second = (black * 0 +  10 * 250) / (black + 10)

        first_dif = abs(want - first)

        second_dif = abs(want - second)

        if second_dif > first_dif:
            hehe = 0
        else:
            hehe = 250
        
        d_array[pos[0], pos[1], 0] = hehe
        d_array[pos[0], pos[1], 1] = hehe
        d_array[pos[0], pos[1], 2] = hehe


print(list_all_offset(0))

RUNNING = True
X = 1
Y = 1

while RUNNING:
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
        if event.type == KEYDOWN:
            if event.key == K_q:
                RUNNING = False

    SURFACE.fill((210, 225, 235))

    for n in range((SCREEN_WIDTH - 2) // 10):
        set_gray(original_array, array, [X, Y])
        X += 1

    if X >= SCREEN_WIDTH - 2:
        X = 1
        Y += 1

    if Y == SCREEN_HEIGHT - 2:
        Y = 1

    hihi = pygame.mouse.get_pressed(3)[0]

    if hihi == True:
        SURFACE.blit(image, (0, 0))
        #SURFACE.blit(pygame.surfarray.make_surface(color_array), (0, 0))
    else:
        SURFACE.blit(pygame.surfarray.make_surface(array), (0, 0))

    pygame.display.update()
    CLOCK.tick(50)
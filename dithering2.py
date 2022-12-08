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

#image = pygame.image.load("images/black_and_white3.png")  
image = pygame.Surface((120, 600))   
gradientRect_h(image, (250, 250, 250), (0, 0, 0), Rect(0, 0, image.get_width(), image.get_height()))

original_array = pygame.surfarray.array3d(image)
color_array = pygame.surfarray.array3d(image)
black = pygame.Surface((image.get_width(), image.get_height()))     
#black.fill((100, 100, 100))
array = pygame.surfarray.array3d(black)
width, height, _ = array.shape 

'''
for y in range(height):
    for x in range(width):
        border = original_array[x, y, 0]

        randi = random.randint(0, 250)

        if randi < border:
            z = 250
        else:
            z = 0
        
        array[x, y, 0] = z
        array[x, y, 1] = z
        array[x, y, 2] = z


for n in range(width // 9):
    print(250 * (n % 2))
    pygame.draw.rect(black, (250 * (n % 2), 250 * (n % 2), 250 * (n % 2)), 
        Rect(n * 9, 0, 9, height))


array = pygame.surfarray.array3d(black)
width, height, _ = array.shape
'''

SCREEN_WIDTH = width
SCREEN_HEIGHT = height

POINTS = []

OFFSET = 6

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
    offset = OFFSET

    while True:
        z = list_values(OFFSET - offset, array, pos)

        if z.__contains__(search):
            #print(z, z.__contains__(search))
            return offset
        
        if offset == 0:
            return 0
        
        offset -= 1

def find_closer(array, search, pos, dis1, dis2):
    one = list_values(dis1, array, pos).__contains__(search)
    two = list_values(dis2, array, pos).__contains__(search)

    if dis1 < dis2:
        if one:
            return dis1
        elif two:
            return dis2
        else:
            return dis1 - 1
    else:
        if two:
            return dis2
        elif one:
            return dis1
        else:
            return dis1 - 1

    

def set_gray(original_array, d_array, pos, check):
    eggyik = pos[0] > -1 and pos[0] < SCREEN_WIDTH
    másik =  pos[1] > -1 and pos[1] < SCREEN_HEIGHT
    
    if eggyik and másik:
        want = original_array[pos[0], pos[1], 0]
        
        if check[0] == None:
            black = find_closest(d_array, 0, pos)
        else:
            black = find_closer(d_array, 0, pos, check[0] + 1, check[0] - 1)

        if check[1] ==  None:    
            white = find_closest(d_array, 250, pos)
        else:
            white = find_closer(d_array, 250, pos, check[1] + 1, check[1] - 1)
        
        '''
        black = find_closest(d_array, 0, pos)
        white = find_closest(d_array, 250, pos)
        '''
        #now = (black * 0 + white * 250) / (black + white)

        first = (OFFSET * 0 + white * 250) / (OFFSET + white)

        second = (black * 0 +  OFFSET * 250) / (black + OFFSET)

        #print('hihi', black, first, white, second, want)

        first_dif = abs(want - first)
        second_dif = abs(want - second)

        if second_dif > first_dif:
            hehe = 250
        else:
            hehe = 0
        
        d_array[pos[0], pos[1], 0] = hehe
        d_array[pos[0], pos[1], 1] = hehe
        d_array[pos[0], pos[1], 2] = hehe

        return [black, white]
    
    return [None, None]


print(list_all_offset(6))

RUNNING = True
X = 0
Y = 0
DIR = 0

while RUNNING:
    for event in pygame.event.get():
        if event.type == QUIT:
            RUNNING = False
        if event.type == KEYDOWN:
            if event.key == K_q:
                RUNNING = False

    SURFACE.fill((210, 225, 235))

    last = [None, None]
    
    if DIR == 0:
        for n in range((SCREEN_WIDTH - 2)):
            last = list(set_gray(original_array, array, [X, Y], last))
            X += 1
            

        if X >= SCREEN_WIDTH - 2:
            X = 0
            Y += 1
            print(Y)
    
        if Y == SCREEN_HEIGHT - 2:
            Y = 0
            DIR = 0
            print('hihi')
    else:
        for n in range((SCREEN_HEIGHT - 2) // 12):
            last = list(set_gray(original_array, array, [X, Y], last))
            Y += 1

        if Y >= SCREEN_HEIGHT - 2:
            Y = 0
            X += 1
    
        if X == SCREEN_WIDTH - 2:
            X = 0
            DIR = 0
            print('hihi')

    
    x = random.randint(0, SCREEN_WIDTH - 1)
    y = random.randint(0, SCREEN_HEIGHT - 1)
    z = 250 * random.randint(0, 1)
    array[x, y, 0] = z
    array[x, y, 1] = z
    array[x, y, 2] = z

    hihi = pygame.mouse.get_pressed(3)[0]

    if hihi == True:
        SURFACE.blit(image, (0, 0))
        #SURFACE.blit(pygame.surfarray.make_surface(color_array), (0, 0))
    else:
        SURFACE.blit(pygame.surfarray.make_surface(array), (0, 0))

    pygame.draw.line(SURFACE, (200, 0, 0), [0, Y], [SCREEN_WIDTH, Y], 2)

    pygame.display.update()
    CLOCK.tick(100)
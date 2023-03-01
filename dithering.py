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

image = pygame.image.load("images/black_and_white9.png")  
original_array = pygame.surfarray.array3d(image)
color_array = pygame.surfarray.array3d(image)
black = pygame.Surface((image.get_width(), image.get_height()))      
array = pygame.surfarray.array3d(black)
width, height, _ = array.shape

SCREEN_WIDTH = width
SCREEN_HEIGHT = height

POINTS = []

FONT1 = pygame.font.SysFont('texgyrechorus', 47)

CLOCK = pygame.time.Clock()
SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("©2022 Dragon tail")

TEN_BRIGHT = []

def calculate_9bright(array, pos):
    b = 0

    for y in [pos[1] - 1, pos[1], pos[1] + 1]:
        for x in [pos[0] - 1, pos[0], pos[0] + 1]:
            if array[x, y, 0] > 128:
                b += 1
    
    return b

def random9pos(pos):
    return [pos[0] + random.randint(-1, 1), pos[1] + random.randint(-1, 1)]

def check_9bright(original_array, new_array, color_array, pos):
    #want = math.floor((original_array[pos[0], pos[1], 0]) / 25.6)
    original_b = (original_array[pos[0], pos[1], 0])
    want = -1
    l = math.inf
    index = 0

    for i in TEN_BRIGHT:
        if abs(i - original_b) < l:
            l = abs(i - original_b)
            want = index
        index += 1

    now = calculate_9bright(new_array, pos)

    if want > now:
        hihi = 255
    elif want < now:
        hihi = 0
    else:
        hihi = -1

    #print(want, now, hihi)
    if hihi != -1:
        randpos = random9pos(pos)
        
        new_array[randpos[0], randpos[1], 0] = hihi
        new_array[randpos[0], randpos[1], 1] = hihi
        new_array[randpos[0], randpos[1], 2] = hihi
    
    color_array[pos[0], pos[1], 0] = 0
    color_array[pos[0], pos[1], 2] = 0
    color_array[pos[0], pos[1], 1] = 0
    

    if now == 1:
        color_array[pos[0], pos[1], 0] = 250
    
    if now == 0:
        color_array[pos[0], pos[1], 2] = 250
    
    if now == 2:
        color_array[pos[0], pos[1], 1] = 250


def working_pos():
    x = random.randint(1, SCREEN_WIDTH - 2)
    y = random.randint(1, SCREEN_HEIGHT - 2)
    return [x, y]


def pick_random_points(array):
    items = []
    for n in range(400):
        x = random.randint(0, SCREEN_WIDTH - 1)
        y = random.randint(0, SCREEN_HEIGHT - 1)
        items.append(array[x, y, 0])
    
    return items

def random10brightness():
    x = []
    for n in range(10):
        x.append(random.randint(0, 255))
    
    x = sorted(x)
    return x

def calculate_unprecise(array, random10, points):
    r10b = random10

    unprecise = 0

    for n in points:
        l = math.inf

        for i in r10b:
            l = min(l, abs(n - i))
        unprecise += l

    return [unprecise, r10b]

def find_best_10(array, number):
    best = []
    least_unprecise = math.inf

    for n in range(number // 100):
        for _ in range(100):
            z = random10brightness()
            x = calculate_unprecise(array, z, POINTS)
            if x[0] < least_unprecise:
                least_unprecise = x[0]
                best = x[1]
        SURFACE.fill((210, 225, 235))
        blit_text(SURFACE, (100, 100, 100), str(round(n / (number / 100) * 100)) + '%', 
                [SURFACE.get_width() // 2, SURFACE.get_height() // 2], FONT1, 1)
        
        blit_text(SURFACE, (100, 100, 100), str(best), 
                [SURFACE.get_width() // 2, SURFACE.get_height() - 100], FONT1, 1)
        

        blit_text(SURFACE, (100, 100, 100), str(least_unprecise), 
                [SURFACE.get_width() // 2, SURFACE.get_height() - 50], FONT1, 1)
        
        
        pygame.display.update()
    
    return best

def tweak_10bright(array, number):
    global TEN_BRIGHT
    for n in range(number):
        hihi = random.randint(0, 9)
        x = list(TEN_BRIGHT)
        x[hihi] += random.randint(-16, 16)
        u = calculate_unprecise(array, x, POINTS)
        now = calculate_unprecise(array, TEN_BRIGHT, POINTS)

        if u[0] < now[0]:
            print('no', u[0], now[0])
            TEN_BRIGHT = list(u[1])
        
        SURFACE.fill((210, 225, 235))
        blit_text(SURFACE, (100, 100, 100), str(round(n / number * 100)) + '%', 
                [SURFACE.get_width() // 2, SURFACE.get_height() // 2], FONT1, 1)
        
        blit_text(SURFACE, (100, 100, 100), str(TEN_BRIGHT), 
                [SURFACE.get_width() // 2, SURFACE.get_height() - 100], FONT1, 1)
        
        blit_text(SURFACE, (100, 100, 100), str(now[0]), 
                [SURFACE.get_width() // 2, SURFACE.get_height() - 50], FONT1, 1)
        
        pygame.display.update()

        
POINTS = pick_random_points(original_array)

TEN_BRIGHT = find_best_10(original_array, 3000)

tweak_10bright(original_array, 2000)

TEN_BRIGHT[0] = TEN_BRIGHT[0] * 0.5

print(TEN_BRIGHT)

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

    for n in range(SCREEN_WIDTH - 2):
        check_9bright(original_array, array, color_array, [X, Y])
        X += 1
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
    CLOCK.tick(40)
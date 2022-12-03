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

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675

FONT1 = pygame.font.SysFont('texgyrechorus', 50)


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
    x = random.randint(1, 1198)
    y = random.randint(1, 673)
    return [x, y]


def pick_random_points(array):
    items = []
    for n in range(200):
        x = random.randint(0, 1199)
        y = random.randint(0, 674)
        items.append(array[x, y, 0])
    
    return items

def random10brightness():
    x = []
    for n in range(10):
        x.append(random.randint(0, 255))
    
    x = sorted(x)
    return x

def calculate_unprecise(array):
    points = pick_random_points(array)
    r10b = random10brightness()

    unprecise = 0

    for n in points:
        l = math.inf

        for i in r10b:
            l = min(l, abs(n - i))
        unprecise += l

    return unprecise, r10b

def find_best_10(array, number):
    best = []
    least_unprecise = math.inf

    for n in range(number):
        x = calculate_unprecise(array)
        if x[0] < least_unprecise:
            least_unprecise = x[0]
            best = x[1]
    
    return best



image = pygame.image.load("images/balck_and_white2.png")  
original_array = pygame.surfarray.array3d(image)
color_array = pygame.surfarray.array3d(image)
black = pygame.Surface((image.get_width(), image.get_height()))      
array = pygame.surfarray.array3d(black)
width, height, _ = array.shape

for n in range(100):
    TEN_BRIGHT = find_best_10(array, 100)
    SURFACE.fill((210, 225, 235))
    blit_text(SURFACE, (100, 100, 100), str(n) + '%', 
            [SURFACE.get_width() // 2, SURFACE.get_height() // 2], FONT1, 1)
    pygame.display.update()


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

    for n in range(1198):
        check_9bright(original_array, array, color_array, [X, Y])
        X += 1
    X = 1
    Y += 1

    if Y == 673:
        Y = 1

    hihi = pygame.mouse.get_pressed(3)[0]

    if hihi == True:
        SURFACE.blit(image, (0, 0))
        #SURFACE.blit(pygame.surfarray.make_surface(color_array), (0, 0))
    else:
        SURFACE.blit(pygame.surfarray.make_surface(array), (0, 0))

    pygame.display.update()
    CLOCK.tick(40)
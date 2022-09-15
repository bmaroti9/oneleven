import math
import random
import sys
import pygame
from pygame.locals import *
import time
import json

from helpers import *

pygame.init()

SKY_PICTURES = []
PARCTICLES = pygame.sprite.Group()

def gradientRect_w(surface, left_colour, right_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface(
        (2, 2))                                   # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, left_colour,  (0, 0),
                     (0, 1))            # left colour line
    pygame.draw.line(colour_rect, right_colour, (1, 0),
                     (1, 1))            # right colour line
    colour_rect = pygame.transform.smoothscale(
        colour_rect, (target_rect.width, target_rect.height))  # stretch!
    # paint it
    surface.blit(colour_rect, target_rect)


def gradientRect_h(surface, top_colour, bottom_colour, target_rect):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface(
        (2, 2))                                   # tiny! 2x2 bitmap
    pygame.draw.line(colour_rect, top_colour,  (0, 0),
                     (1, 0))            # left colour line
    pygame.draw.line(colour_rect, bottom_colour, (0, 1),
                     (1, 1))            # right colour line
    colour_rect = pygame.transform.smoothscale(
        colour_rect, (target_rect.width, target_rect.height))  # stretch!
    # paint it
    surface.blit(colour_rect, target_rect)


def draw_arc(surface, percent, radius, color, center_pos, width):
    angle = 0
    old_pos = rotating_position(0, radius, angle, center_pos)

    for n in range(round(180 * percent)):
        angle -= 2
        new_pos = rotating_position(0, radius, angle, center_pos)
        pygame.draw.line(surface, color, old_pos, new_pos, width)
        old_pos = new_pos
    
def arc_circle(surface, percent, radius, color, center_pos, width, number, font, font_color, add, back):
    angle = 0

    pygame.draw.circle(surface, back, [center_pos[0] - 1, center_pos[1] - 1], radius + 6, (width * 2) + 2)

    for n in range(round(120 * percent)):
        angle -= 3
        pygame.draw.circle(surface, color, rotating_position(0, radius, angle, center_pos), width)

    blit_text(surface, font_color, str(number), center_pos, font, 1)
    
def arc_circle2(surface, center, font, number, radius, width, percent, color, t_color, add):
    #filled_arc(surface, center, color, radius, width, 90, 90 + (-360 * percent))
    blit_text(surface, t_color, str(number), center, font, 1)

def integer_to_english(number):
    if number>=1 and number<=1000:
        a = ['','one','two','three','four','five','six',
                'seven','eight','nine','ten','eleven','twelve','thirteen','fourteen',
                        'fifteen','sixteen','seventeen','eighteen','nineteen','twenty ','thirty ',
                        'fourty ','fifty ','sixty ','seventy ','eighty ','ninty ']
        if number<=20:
            if number%10==0: return a[number]
            else: return a[number]
        elif number<100:
            b=number-20
            r=b%10
            b//=10
            return a[20+b]+a[r]
        elif number<1000:
            if number%100==0:
                b=number//100
                return a[b]+' hundred'
            else:
                r=number%100
                b=number//100
                if r<=20:
                    return a[b]+' hundred'+' and '+a[r]
                else:
                    r=r-20
                    d=r//10
                    r%=10
                    return a[b]+' hundred'+' and '+a[20+d]+a[r]
        elif number==1000:
            return 'one thousand'
        else:
            return -1


def sin_pos(rattle, loop_length, speed, time, offset = 0):
    t = ((time + offset) / 2 % loop_length) * speed # scale and loop time
    x = t
    y = math.sin(t/50.0) * rattle     # scale sine wave
    y = int(y)   
    return [x, y]

def generate_new_skymap(surface):
    global SKY_PICTURES
    SKY_PICTURES = []

    star_positions = []
    for n in range(500):
        star_positions.append(random_pos_on_surf(surface))
    
    for n in range(20):
        a = pygame.Surface([surface.get_width(), surface.get_height()], pygame.SRCALPHA, 32)
        for n in star_positions:
            if random.randint(0, 10) != 0:
                pygame.draw.circle(a, (255, 255, 255), n, 1)
        SKY_PICTURES.append(a)

def blit_skymap(surface, pos):
    current_sky = (pygame.time.get_ticks() // 89) % 20
    surface.blit(SKY_PICTURES[current_sky], pos)


def blurSurf(surface, amt):
    """
    Blur the given surface by the given 'amount'.  Only values 1 and greater
    are valid.  Value 1 = no blur.
    """
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
    
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pygame.transform.smoothscale(surface, scale_size)
    surf = pygame.transform.smoothscale(surf, surf_size)
    return surf


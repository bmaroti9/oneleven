import math
import random
import sys
import pygame
from pygame.locals import *
import time
import json
from os.path import isfile, join, basename, getmtime

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

def uniform_colors(number, c):
    first_c = []
    first_c.append(c)
    first_c.append((255 - first_c[0][0], 255 - first_c[0][1], 255 - first_c[0][2]))
    colors = []
    for n in range(number):
        h = random.randint(0, 1) * 255
        colors.append(transition_colors(random.choice(first_c), (h, h, h), random.randint(0, 100) / 100))
    return colors

PALETTE = [(0, 0, 0), (0, 0, 0)]

def pastel_color(base, pastel_factor = 0.5):
    color = [(x+pastel_factor)/(1.0+pastel_factor) for x in base]
    return (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

def random_paste_color():
    c = []
    for n in range(3):
        c.append(random.randint(0, 100) / 100)
    return pastel_color(c, 0.8)

def generate_palette():
    global PALETTE
    PALETTE = []
    PALETTE.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    PALETTE.append((255 - PALETTE[0][0], 255 - PALETTE[0][1], 255 - PALETTE[0][2]))

def get_color():
    h = random.randint(0, 1) * 255
    color = transition_colors(random.choice(PALETTE), (h, h, h), random.randint(0, 100) / 100)
    return color

def file_color(path, back = 1):
    pathy = path.split('/')
    x = pathy.index(basename(path))
    name = pathy[x - back]
    c = []
    for n in range(3):
        c.append(generate_number_from_string(name, 100, n) / 100)
    c = pastel_color(c, 0.8)
    
    first_c = []
    first_c.append(c)
    first_c.append((255 - first_c[0][0], 255 - first_c[0][1], 255 - first_c[0][2]))
    h = generate_number_from_string(path, 1, 0) * 255
    hihi = transition_colors(first_c[generate_number_from_string(path, 1, 2)], (h, h, h), 
                                generate_number_from_string(path, 70, 1) / 100)
    return hihi
import pygame
import math
from pygame.locals import*
import random

from gradient import *
from helpers import *

KEY = None

def log_key(event):
    global KEY
    if event.key == pygame.K_BACKSPACE:
        #TALK_WORD = TALK_WORD[:-1]
        KEY = -1
    else:
        KEY = event.unicode

def get_key():
    global KEY
    return KEY

#color: background   big tile     small tile     theme          date color
COLORS = [
    [(5, 10, 30), (9, 20, 50), (30, 51, 190), (188, 82, 120), (255, 255, 255)],
    [(176, 189, 164), (105, 209, 15), (85, 143, 34), (133, 168, 103), (23, 26, 22)],
    [(240, 240, 240), (164, 183, 237), (154, 173, 227), (178, 72, 100), (100, 100, 100)],
    [(20, 20, 20), (80, 70, 40), (189, 165, 49), (250, 250, 250), (189, 165, 49)]
]

THEME = COLORS[0]

def random_theme():
    global THEME
    x = []
    for n in range(5):
        x.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    print(x)
    THEME = x

def set_theme(x):
    global THEME
    THEME = COLORS[x]

def get_colors():
    return THEME

FULL_SET = False
SIZES = [[100, 100], [100, 100]]

def full_set_initialize(surface):
    global SIZES
    SIZES[0] = [(surface.get_width() - 20) * 0.6, (surface.get_height() - 50) * 0.6]
    SIZES[1] = [surface.get_width() - 20, surface.get_height() - 50]

def full_set_change():
    global FULL_SET
    FULL_SET = not FULL_SET

def full_set_get():
    return SIZES[FULL_SET]

def get_the_screen_max():
    return SIZES[1]

MIL = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
WANTED_SPEED = 10

def frame_set(miliseconds):
    global MIL
    MIL.append(miliseconds / WANTED_SPEED)
    del MIL[0]

def frame_get():
    return sum(MIL) / len(MIL)

EVENT = 0

def upload_event(event):
    global EVENT
    EVENT = event

def get_event():
    return EVENT

def create_gradient_surface(c1, c2, x, y):
      x = pygame.Surface((x, y))
      gradientRect_w(x, c1, c2, x.get_rect())
      return x

GRADIENT = [0, 0]
SURFACE = 0

def gradient_init_surface(surface):
      global SURFACE
      SURFACE = surface

def upload_random_gradient(start):
      global GRADIENT
      c1 = small_change_to_color((start, start, start), 50)
      c2 = small_change_to_color(c1, 100)
      print(c1, c2)
      GRADIENT[0] = create_gradient_surface(c1, c2, SURFACE.get_width(), SURFACE.get_height())
      c1 = transition_colors(c1, (255, 255, 255), 0.15)
      c2 = transition_colors(c2, (255, 255, 255), 0.15)
      GRADIENT[1] = create_gradient_surface(c1, c2, SURFACE.get_width(), SURFACE.get_height())

def upload_specific_gradient(c1, c2):
      global GRADIENT
      GRADIENT[0] = create_gradient_surface(c1, c2, SURFACE.get_width(), SURFACE.get_height())
      c1 = transition_colors(c1, (255, 255, 255), 0.15)
      c2 = transition_colors(c2, (255, 255, 255), 0.15)
      GRADIENT[1] = create_gradient_surface(c1, c2, SURFACE.get_width(), SURFACE.get_height())

def get_uploaded_gradient():
      return GRADIENT


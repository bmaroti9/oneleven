import pygame
from pygame.locals import *

from helpers import *

EVENT = 0

def upload_event(event):
    global EVENT
    EVENT = event

def get_event():
    return EVENT
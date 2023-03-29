import pygame
import math
from pygame.locals import*
import time
import random
import sys
import json

from helpers import *

class image_viewer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.font = 0
    
    def display_image(surface, image):
        x = 0
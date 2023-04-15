import pygame
from pygame.locals import *
from os import listdir, stat
from os.path import isfile, join, basename, getmtime
import time
from datetime import timedelta, datetime, date

from helpers import *
from tiles import *
from gradient import *

class Tile_space(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.tiles = []

    def set_tiles(self, paths, origin):
        self.tiles = []

        for n in paths:
            t = getmtime(n)
            self.add_tile(t, n)
        
        for n in range(-360, 360):
            end_date = date.today() + timedelta(days=n)
            self.add_marker(end_date)

        self.tiles = sorted(self.tiles, key=Tile.get_my_time)

        last = False
        index = 0
        for _ in range(len(self.tiles)):
            if self.tiles[index].close_setting < 110:
                if last:
                    del self.tiles[index - 1]
                else:
                    last = True
                    index += 1
            else:
                last = False
                index += 1
        del self.tiles[-1]

        for n in self.tiles:
            if n.close_setting < 110:
                n.temp_time += timedelta(days=-1)
                n.sync()
                    
        i = -self.tiles[0].close_setting
        for n in self.tiles:
            i += n.push
            n.pos = origin - i
            i += n.push

    def add_tile(self, time, path):
        x = Tile(time, path)
        self.tiles.append(x)
    
    def add_marker(self, time):
        x = Date_Marker(time)
        self.tiles.append(x)

    def any_close(self, est_time, focus_time):
        requested_altitude = None
        for n in self.tiles:
            real_pos = focus_time - n.pos
            if abs(real_pos - est_time) < n.close_setting:
                requested_altitude = real_pos
        return requested_altitude

    def update(self, surface, focus_time, smooth_scroll):
        for n in self.tiles:
            n.update(surface, focus_time + 360, smooth_scroll)

class Directory_manager(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.path = "."
        self.altitudes = []
        self.font1 = pygame.font.SysFont('texgyreadventor', 20)

    def load_directory(self, tile_space):
        generate_palette()
        dirct = listdir(self.path)
        paths = []
        for n in dirct:
            x = self.path + '/' + n
            x = x[2:]
            paths.append(x)
        tile_space.set_tiles(paths, 0)
    
    def forward(self, tile_space, altitude):
        x = self.path + '/' + get_closest().name
        if not isfile(x):
            self.path = x
            self.load_directory(tile_space)
            self.altitudes.append(altitude)
            set_wanted(0)
    
    def backward(self, tile_space, altitude):
        before = str(self.path)
        z = self.path.split('/')
        back = len(z[-1]) + 1
        self.path = self.path[:len(self.path) - back]
        if self.path == '':
            self.path = '.'
        if before != self.path:
            self.load_directory(tile_space)
            set_wanted(self.altitudes[-1])
            del self.altitudes[-1]
        
    def update(self, surface, tile_space, altitude):
        p = get_closest()
        if p != None:
            x = self.path + '/' + p.name
            pos = 5
            s = x.split('/')
            for n in range(len(s)):
                if n == len(s) - 2:
                    c = get_colors()[3]
                else:
                    c = (255, 255, 255)
                text = '/' + s[n]
                if text == '/.':
                    text = '~~~'

                hihi = button(surface, self.font1, c, text, [pos, 12, 2], 
                    None, get_colors()[3], 1, [0, 0], 15)
                if hihi:
                    v = s[:(n + 1)]
                    before = self.path
                    self.path = '/'.join(v)
                    if before != self.path and not isfile(self.path) and self.path != '' and text != '/':
                        self.load_directory(tile_space)
                    else:
                        self.path = before
                pos += test_text_rect(text, self.font1).right + 8
            
            blit_text(surface, (255, 255, 255), p.abs_time, [surface.get_width() - 10, -4], self.font1, 2)
            b = button(surface, self.font1, (255, 255, 255), '<', [pos + 8, -4, 0], 
                    None, get_colors()[3], 1, [0, 0], 15)
            if b:
                self.backward(tile_space, altitude)
            elif detect_click_rect(0, Rect(50, 50, surface.get_width() - 100, surface.get_height() - 100)):
                self.forward(tile_space, altitude)

WANTED = None

def set_wanted(altitude):
    global WANTED
    WANTED = altitude

def reload():
    global WANTED
    x = WANTED
    WANTED = None
    if x == None:
        return None
    else:
        return x

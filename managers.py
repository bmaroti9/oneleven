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
        self.space_progress = -10
        self.i = 0
        self.origin = 0

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
            n.pos = -999999
        
        self.space(origin)
        self.space(-999999999)
        set_closest(None)
        self.space_work()
    
    def space(self, origin):
        self.space_progress = -1
        self.origin = origin

    def space_work(self):
        if self.space_progress == -1:
            self.original_closest = get_closest()
            if self.original_closest != None:
                self.before = self.original_closest.pos
            self.i = -999999999
        elif self.space_progress < len(self.tiles):
            n = self.tiles[self.space_progress]
            if n.close_setting > 120:    
                n.set_my_surf()
            self.i += n.push
            n.pos = self.origin - self.i
            self.i += n.push
        else: 
            if self.original_closest != None:
                after = self.original_closest.pos
                change = self.before - after
                for n in self.tiles:
                    n.pos += change
                #self.original_closest.size = 100
            self.space_progress = -10
        self.space_progress += 1

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
        for n in range(2):
            if self.space_progress > -2:
                self.space_work()
        else:
            for n in self.tiles:
                n.update(surface, focus_time + surface.get_height() / 2, smooth_scroll)

class Directory_manager(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.path = "."
        self.altitudes = []
        #self.font1 = pygame.font.SysFont('texgyreadventor', 20)
        self.font1 = pygame.font.Font('fonts/static/Raleway-ExtraLight.ttf', 23)

    def load_directory(self, tile_space):
        generate_palette()
        dirct = listdir(self.path)
        paths = []
        for n in dirct:
            x = self.path + '/' + n
            #x = x[2:]
            paths.append(x)
        tile_space.set_tiles(paths, 0)
        set_closest(None)

    def forward(self, tile_space, altitude):
        x = self.path + '/' + get_closest().name
        if not isfile(x) and get_closest().close_setting > 200:
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
        #blit_image(surface, 'images/eternal_white.png', [18, 24], 0.135)
        if p != None:
            x = self.path + '/' + p.name
            pos = 9
            s = x.split('/')
            for n in range(len(s)):
                if n == len(s) - 2:
                    c = get_colors()[3]
                else:
                    c = (255, 255, 255)
                text = '/' + s[n]
                if text == '/.':
                    text = 'Q'

                hihi = button(surface, self.font1, c, text, [pos, 14, 2],
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

            blit_text(surface, (255, 255, 255), p.abs_time, [surface.get_width() - 10, 2], self.font1, 2)
            b = button(surface, self.font1, (255, 255, 255), '<', [pos + 8, 14, 2],
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

def find_end_altitude(v):
    # t = v because: t = v / 1
    s = ((0.5 * (v ** 2)) - abs(v / 2)) * sign_function(v * -10000)

    return s

def required_speed(s):
    # t = v because: t = v / 1
    v = math.sqrt(abs(s) / 0.5) * sign_function(s * -1000)
    return v

def change_speed(v_current, s):
    v_wanted = required_speed(s)
    delta_v = v_wanted - v_current
    a = delta_v * 0.7 * frame_get()
    return a
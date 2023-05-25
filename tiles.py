import pygame
import json
from pygame.locals import *
from os import listdir, stat
from os.path import isfile, join, basename, getmtime
import time
from datetime import timedelta, datetime, date

from helpers import *
from apps import *
from settings import *

with open("times.txt", "r") as f:
    TIMES = json.load(f)

class Tile(pygame.sprite.Sprite):
    def __init__(self, time_point, path):
        super().__init__()

        self.type = 1
        self.path = path
        self.name = basename(path)

        self.time = time_point
        self.real_time = time.ctime(time_point)
        self.abs_time = self.real_time[0:3] + self.real_time[10:16]

        self.pos = 0
        self.push = 1
        self.size = 0
        self.set_my_surf()
        self.size = full_set_get()[1] / 2 * (1 - (full_set_get()[1] * 0.0002))
        self.new = 0

    def size_adjust(self, surface, distance, smooth_scroll):
        wanted = full_set_get()[1] / 2
        if abs(distance) > surface.get_height() / 2 * 0.6 or abs(smooth_scroll) > 24:
            wanted = full_set_get()[1] / 2 * (1 - (abs(distance) * 0.0002))
        self.size += (wanted - self.size) * 0.11  * frame_get()

    def update(self, surface, altitude, smooth_scroll, tiles):
        i = tiles.index(self)
        x = tiles.index(get_closest())
        d = sign_function((x - i) * 10)
        if 0 < i + d < len(tiles) - 1:
            pos = tiles[i + d].pos + full_set_get()[1] * d * ((self.push + tiles[i + d].push) / 2)
            self.pos += (pos - self.pos) * min(0.15 * frame_get(), 1)
        real_pos = altitude - self.pos
        target = surface.get_height() // 2
        distance = target - real_pos

        if abs(distance) < surface.get_height() + 60:
            if self.new != full_set_get()[0] and abs(smooth_scroll) < 0.02:
                self.set_my_surf()
                self.new = full_set_get()[0]
            if abs(distance) < self.close_setting:
                self.app.update(self.surf)
                set_closest(self)
            #self.size_adjust(surface, distance, smooth_scroll)
            x = full_set_get()[1] * 0.49
            self.size = max(x - (abs(smooth_scroll * 0.125) ** 2) - abs(distance) * 0.01, 40)
            real_pos = target - (distance) * (self.size / x )
            self.texture(surface, real_pos)
        else:
            self.new = 0

    def texture(self, surface, real_pos):
        coolsize = self.size * self.xy_ratio
        coolheight = self.size

        mid = surface.get_width() // 2
        top = real_pos - coolheight    #REVERSE FOR SIDEWAYS SCROLLING
        side = mid - coolsize

        surface.blit(pygame.transform.scale(self.surf.convert_alpha(),
                              [int(coolsize * 2), int(coolheight * 2)]), [side, top + 10])

    def set_my_surf(self):
        full = full_set_get()
        self.xy_ratio = full[0] / full[1]
        self.close_setting = full[1] * 0.5
        self.surf = pygame.Surface((full[0], full[1]))
        app = decide_tile_app(self.path)

        self.app = app(self.surf, self.path)
        self.app.update(self.surf)

    def get_my_time(self):
        return -self.time #we want the most reccent on the top so its necessary to flip

class Date_Marker(pygame.sprite.Sprite):
    def __init__(self, time_point):
        super().__init__()

        self.type = 0
        self.name = ''
        self.close_setting = 70 #when scrolling will jump on it
        self.push = 0.3
        self.temp_time = time_point
        self.time = time.mktime(self.temp_time.timetuple())
        self.real_time = time.ctime(self.time)
        self.pos = 0
        self.blit_time = 'hihi'

        self.font = pygame.font.Font('fonts/static/Raleway-ExtraLightItalic.ttf', 40)

    def sync(self):
        self.time = time.mktime(self.temp_time.timetuple())
        self.real_time = time.ctime(self.time)
        day = TIMES["interpret_d"].index(self.real_time[0:3])
        eth = TIMES["interpret_m"].index(self.real_time[4:7])
        self.blit_time = self.real_time[20:26] + ' ' + TIMES['months'][eth] + self.real_time[7:10]
        self.blit_time = self.blit_time + '     ' + TIMES['days'][day]
        self.abs_time = ''

    def update(self, surface, altitude, smooth_scroll, tiles):
        i = tiles.index(self)
        x = tiles.index(get_closest())
        d = sign_function((x - i) * 10)
        if 0 < i + d < len(tiles) - 1:
            pos = tiles[i + d].pos + full_set_get()[1] * d * ((self.push + tiles[i + d].push) / 2)
            self.pos += (pos - self.pos) * min(0.15 * frame_get(), 1)

        real_pos = altitude - self.pos
        target = surface.get_height() // 2
        distance = target - real_pos + 3

        if abs(distance) < surface.get_height():
            pygame.draw.line(surface, get_colors()[3],
                                [20, real_pos + 10], [surface.get_width() - 60, real_pos + 10])
            blit_text(surface, get_colors()[3], str(self.blit_time), [20, real_pos - 4], self.font, 4)
            if abs(distance) < self.close_setting:
                set_closest(self)

    def get_my_time(self):
        return -self.time #we want the most reccent on the top so its necessary to flip


FROM = ['.png', '.eml']
TO = [Image_viewer, Email]

def decide_tile_app(name):
    if isfile(name):
        for n in range(len(FROM)):
            if FROM[n] in name:
                return TO[n]
        return Unloadable
    else:
        return Folder

CLOSEST = None

def set_closest(me):
    global CLOSEST
    CLOSEST = me

def get_closest():
    return CLOSEST

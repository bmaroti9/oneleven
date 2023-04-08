import pygame
from pygame.locals import *
from os import listdir, stat
from os.path import isfile, join, basename, getmtime
import time
from datetime import timedelta, datetime, date

from helpers import *
from apps import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, time_point, path):
        super().__init__()

        self.close_setting = 300 #when scrolling will jump on it
        self.push = 325 #push the ones next to it farther away
        self.name = basename(path)
        self.surf = pygame.Surface((1320, 660))
        app = decide_tile_app(path)
        
        self.app = app(self.surf, path)

        self.time = time_point
        self.real_time = time.ctime(time_point)

        self.pos = 0
        self.size = 280

        self.title_font = pygame.font.SysFont('texgyreadventor', 20)

    def size_adjust(self, surface, distance, smooth_scroll):
        wanted = 330
        if abs(distance) > surface.get_height() / 2 - 200 or abs(smooth_scroll) > 24:
            wanted = 300 - abs(distance) * 0.08
        self.size += (wanted - self.size) * 0.3

    def update(self, surface, altitude, smooth_scroll):
        real_pos = altitude - self.pos
        target = surface.get_height() // 2
        distance = target - real_pos + 3

        if abs(distance) < surface.get_height():
            self.size_adjust(surface, distance, smooth_scroll)
            self.texture(surface, real_pos)

            if abs(distance) < 200:
                set_closest(self.name, self.real_time[10:16])
            
    def texture(self, surface, real_pos):
        coolsize = self.size * 2
        coolheight = self.size

        mid = surface.get_width() // 2
        top = real_pos - coolheight - 5    #REVERSE FOR SIDEWAYS SCROLLING
        side = mid - coolsize

        self.app.update(self.surf)
        surface.blit(pygame.transform.scale(self.surf.convert_alpha(),
                              [int(coolsize * 2), int(coolheight * 2)]), [side, top + 5])
        '''
        blit_text(surface, get_colors()[3], 'new tab', [surface.get_width() / 2, top],
                   self.title_font, 3)
        blit_text(surface, get_colors()[4], 'chromium', [side + 20, top],
                   self.title_font, 0)
        '''
    
    def get_my_time(self):
        return -self.time #we want the most reccent on the top so its necessary to flip

class Date_Marker(pygame.sprite.Sprite):
    def __init__(self, time_point):
        super().__init__()

        self.close_setting = 100 #when scrolling will jump on it
        self.push = 47 #push the ones next to it farther away
        self.time = time_point
        self.real_time = time.ctime(time_point)
        self.blit_time = self.real_time[0:10]

        self.font = pygame.font.SysFont('texgyreadventor', 30)
    
    def update(self, surface, altitude, smooth_scroll):
        real_pos = altitude - self.pos
        target = surface.get_height() // 2
        distance = target - real_pos + 3

        if abs(distance) < surface.get_height():
            blit_text(surface, get_colors()[3], str(self.blit_time), [20, real_pos], self.font, 4)
            pygame.draw.line(surface, get_colors()[3], 
                                [20, real_pos + 10], [surface.get_width() - 60, real_pos + 10])
            
            if abs(distance) < 200:
                set_closest('', self.real_time[10:16])
        
    def get_my_time(self):
        return -self.time #we want the most reccent on the top so its necessary to flip
    
class Tile_space(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.tiles = []

    def set_tiles(self, paths, origin):
        self.tiles = []

        for n in paths:
            t = getmtime(n)
            self.add_tile(t, n)
        
        for n in range(-1000, 1000):
            end_date = date.today() + timedelta(days=n)
            unixtime = time.mktime(end_date.timetuple())
            self.add_marker(unixtime)

        self.tiles = sorted(self.tiles, key=Tile.get_my_time)

        last = False
        index = 0
        for _ in range(len(self.tiles)):
            if self.tiles[index].close_setting < 110:
                if last:
                    del self.tiles[index]
                else:
                    last = True
                    index += 1
            else:
                last = False
                index += 1
                    
        #self.tiles = self.tiles.reverse()
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
        self.font = pygame.font.SysFont('texgyreadventor', 20)

    def load_directory(self, tile_space):
        dirct = listdir(self.path)
        paths = []
        for n in dirct:
            x = self.path + '/' + n
            x = x[2:]
            paths.append(x)
        tile_space.set_tiles(paths, 0)
    
    def forward(self, tile_space):
        x = self.path + '/' + get_closest()[0]
        if not isfile(x):
            self.path = x
        self.load_directory(tile_space)
    
    def backward(self, tile_space):
        z = self.path.split('/')
        back = len(z[-1]) + 1
        self.path = self.path[:len(self.path) - back]
        print(self.path)
        self.load_directory(tile_space)
    
    def update(self, surface, tile_space):
        p = get_closest()
        x = self.path + '/' + p[0]
        j = blit_text(surface, (255, 255, 255), x, [0, -4], self.font)
        blit_text(surface, (255, 255, 255), p[1], [surface.get_width() - 10, -4], self.font, 2)
        b = button(surface, self.font, (255, 255, 255), '<', [j.right + 10, -4, 0], 
                None, get_colors()[3], 1, [0, 0], 8)
        if b:
            self.backward(tile_space)

FROM = ['.png']
TO = [Image_viewer]

def decide_tile_app(name):
    if isfile(name):
        for n in range(len(FROM)):
            if FROM[n] in name:
                return TO[n]
        return Unloadable
    else:
        return Folder
    
CLOSEST = ['', None]

def set_closest(me, time):
    global CLOSEST
    CLOSEST = [str(me), time]

def get_closest():
    return CLOSEST

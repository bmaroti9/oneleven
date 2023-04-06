import pygame
from pygame.locals import *
from os import listdir
from os.path import isfile, join, basename

from helpers import *
from apps import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, time_point, path):
        super().__init__()

        self.name = basename(path)
        self.surf = pygame.Surface((1320, 660))
        app = decide_tile_app(path)
        #print(path, self.name, app)
        self.app = app(self.surf, path)

        self.time = time_point
        self.size = 280

        self.title_font = pygame.font.SysFont('texgyreadventor', 20)

    def size_adjust(self, surface, distance, smooth_scroll):
        wanted = 330
        if abs(distance) > surface.get_height() / 2 - 200 or abs(smooth_scroll) > 24:
            wanted = 300 - abs(distance) * 0.08
        self.size += (wanted - self.size) * 0.3

    def update(self, surface, focus_time, smooth_scroll):
        real_pos = focus_time - self.time
        target = surface.get_height() // 2
        distance = target - real_pos + 3

        if abs(distance) < surface.get_height():
            self.size_adjust(surface, distance, smooth_scroll)
            self.texture(surface, real_pos)

        if distance < 200:
            set_closest(self.name)
            
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

class Tile_space(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.tiles = []

    def set_tiles(self, paths, focus_time):
        self.tiles = []

        time = focus_time
        for n in paths:
            self.add_tile(time, n)
            time += 660

    def add_tile(self, focus_time, path):
        x = Tile(focus_time, path)
        self.tiles.append(x)

    def any_close(self, est_time, focus_time):
        requested_altitude = None
        for n in self.tiles:
            real_pos = focus_time - n.time
            if abs(real_pos - est_time) < 300:
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

    def load_directory(self, tile_space, focus_time):
        dirct = listdir(self.path)
        paths = []
        for n in dirct:
            x = self.path + '/' + n
            x = x[2:]
            paths.append(x)
        tile_space.set_tiles(paths, focus_time)
    
    def forward(self):
        x = self.path + '/' + get_closest()
        if not isfile(x):
            self.path = x
        print(self.path)
    
    def update(self, surface):
        x = self.path + '/' + get_closest()
        blit_text(surface, (255, 255, 255), x, [0, -4], self.font)

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
    
CLOSEST = ''

def set_closest(me):
    global CLOSEST
    CLOSEST = str(me)

def get_closest():
    return CLOSEST

def marker(pos, surface):
    real_pos = pos + surface.get_height() // 2
    pygame.draw.circle(surface, (250, 0, 250), [20, surface.get_height() // 2], 5)
    pygame.draw.circle(surface, (250, 250, 250), [20, real_pos], 5)

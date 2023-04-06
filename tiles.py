import pygame
from pygame.locals import *
from os import listdir

from helpers import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, time_point, surface, app = 0):
        super().__init__()

        self.surf = pygame.Surface((1320, 660))
        self.app = app(self.surf)

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
            
    def texture(self, surface, real_pos):
        coolsize = self.size * 2
        coolheight = self.size

        mid = surface.get_width() // 2
        top = real_pos - coolheight - 5    #REVERSE FOR SIDEWAYS SCROLLING
        side = mid - coolsize

        self.app.update(self.surf)
        #self.surf.fill((0, 0, 200))
        surface.blit(pygame.transform.scale(self.surf.convert_alpha(),
                              [int(coolsize * 2), int(coolheight * 2)]), [side, top + 5])
        #surface.blit(self.surf.convert_alpha(), [side, top + 5])
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

    def add_tile(self, focus_time, surface, app):
        x = Tile(focus_time, surface, app)
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

    def load_directory(self):
        dirct = listdir(self.path)

def marker(pos, surface):
    real_pos = pos + surface.get_height() // 2
    pygame.draw.circle(surface, (250, 0, 250), [20, surface.get_height() // 2], 5)
    pygame.draw.circle(surface, (250, 250, 250), [20, real_pos], 5)

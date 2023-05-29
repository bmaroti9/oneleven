import pygame
import json
from pygame.locals import *
import time
from datetime import timedelta, datetime, date

from helpers import *
from apps import *
from settings import *

class Supertile(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()

        self.timeline = []

        self.screen_center = [surface.get_width() // 2, surface.get_height() // 2]

        self.full_set = [surface.get_width() - 20, surface.get_height() - 20]
        self.xy_ratio = self.full_set[0] / self.full_set[1]
        
        self.scroll = 0
        self.smooth_scroll = 0
        self.altitude = 0
        self.zoom = 0.9
        
        self.pull()

        self.center = 0

        #self.add_tile(Box)
        #self.push()
           
    def text_to_app(self, text):
        t = ['Box']
        a = [Box]
        return a[t.index(text)]

    def app_to_text(self, app):
        t = ['Box']
        a = [Box]
        return t[a.index(app)]

    def push(self):
        print(self.timeline)
        self.timeline = sorted(self.timeline, key=lambda d: d['mili_timepoint'])
        with open("timeline.txt", "w") as f:
            json.dump(self.timeline, f, indent=2)
    
    def pull(self):
        with open("timeline.txt", "r") as f:
            self.timeline = json.load(f)
        
    def add_tile(self, app):
        x = app()
        storage = x.setup()
        x = datetime.now()
        storage['app'] = self.app_to_text(app)
        storage['mili_timepoint'] = x.timestamp() * 1000
        self.timeline.append(storage)
        self.push()
    
    def blit_to_center(self, surface, pos, zoom, storage):
        size = (zoom - (abs(pos) * 0.0001)) * self.full_set[1]
        top = self.screen_center[1] - (size / 2) + pos
        side = self.screen_center[0] - (size / 2) * self.xy_ratio
        surf = pygame.Surface((size * self.xy_ratio, size))
        z = self.text_to_app(storage['app'])
        z.update(surf, storage)
        surface.blit(surf, [side, top])
        return size

    def update(self, surface):
        events = get_event()
        for event in events:
                if event.type == KEYDOWN:
                    if event.key == pygame.K_a:
                        self.add_tile(Box)
                    elif event.key == pygame.K_UP:
                        self.center -= 1
                    elif event.key == pygame.K_DOWN:
                        self.center += 1
                if event.type == pygame.MOUSEWHEEL:
                    self.scroll += event.y * 4
                    self.scroll = self.scroll * 0.9
        
        self.scroll -= sign_function(self.scroll) * 0.3
        self.smooth_scroll += (self.scroll - self.smooth_scroll) * 0.4
        self.altitude += self.smooth_scroll
        self.zoom = max(1 - abs((self.smooth_scroll * 0.8) ** 2 * 0.0007), 0.2)

        origin = self.blit_to_center(surface, self.altitude, self.zoom, self.timeline[self.center])
        before = self.timeline[:self.center]
        before.reverse()
        before = before[:2]
        b = self.altitude - origin
        for n in before:
            x = self.blit_to_center(surface, b, self.zoom, n)
            b -= x
        after = self.timeline[(self.center + 1):]
        after = after[:2]
        a = self.altitude + origin
        for n in after:
            x = self.blit_to_center(surface, a, self.zoom, n)
            a += x
        if abs(self.altitude - origin) < abs(self.altitude):
            if self.center == 0:
               self.altitude -= self.smooth_scroll * 0.9
            else:
                self.center -= 1
                self.altitude = self.altitude - origin
        elif abs(self.altitude + origin) < abs(self.altitude):
            if self.center == len(self.timeline) - 1:
                self.altitude -= self.smooth_scroll * 0.9
            else:
                self.center += 1
                self.altitude = self.altitude + origin


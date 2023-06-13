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
            

            #requirements for horizontal scrolling
            self.scroll = [0, 0]
            self.smooth_scroll = [0, 0]
            self.altitude = [0, 0]
            self.center = [0, 0]
            self.prediction = [0, 0]

            self.absolute_pos = [0, 0]

            self.max_zoom = 1
            self.zoom = 0.9
            
            self.pull()

            self.a = [Box(surface), Music(surface)]
            self.t = ['Box', 'Music']
            
      def text_to_app(self, text):
            return self.a[self.t.index(text)]

      def app_to_text(self, app):
            return self.t[self.a.index(app)]

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
      
      def blit_to_center(self, surface, pos, storage):
            size = (self.zoom - (max(abs(pos[0]), abs(pos[1])) * 0.0001)) * self.full_set[1]
            size = [size * self.xy_ratio, size]

            if abs(self.max_speed) < 20 * self.zoom:
                  for d in (0, 1):
                        if abs(self.prediction[d] - pos[d]) < size[d] / 2:
                              z = change_speed(self.smooth_scroll[d], pos[d]) * 1.4
                              if abs(z) > 0.15:
                                    self.altitude[d] += z

            if abs(pos[0]) < surface.get_width() and abs(pos[1]) < surface.get_height():
                  top = self.screen_center[1] - (size[1] / 2) + pos[1]
                  side = self.screen_center[0] - (size[0] / 2) + pos[0]
                  surf = pygame.Surface(size)
                  z = self.text_to_app(storage['app'])
                  z.update(surf, storage)
                  surface.blit(surf, [side, top])
            return size

      def update(self, surface):
            events = get_event()
            for event in events:
                  if event.type == KEYDOWN:
                        if event.key == pygame.K_a:
                              self.add_tile(Music)
                  if event.type == pygame.MOUSEWHEEL:
                        self.scroll[0] += event.x * 4
                        self.scroll[0] = self.scroll[0] * 0.93
                        self.scroll[1] += event.y * 4
                        self.scroll[1] = self.scroll[1] * 0.93
                  elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 3:
                              if self.max_zoom == 1: self.max_zoom = 0.5
                              else: self.max_zoom = 1
            if abs(self.smooth_scroll[0]) > abs(self.smooth_scroll[1]):
                  self.max_speed = self.smooth_scroll[0]
            else:
                  self.max_speed = self.smooth_scroll[1]
            self.zoom = max(self.max_zoom - abs(((self.max_speed * 0.8) ** 2 * 0.0007)), 0.2)

            self.handle_scroll(surface)

      def handle_scroll(self, surface):
            for d in [0, 1]:
                  self.scroll[d] -= sign_function(self.scroll[d]) * 0.5
                  self.smooth_scroll[d] += (self.scroll[d] - self.smooth_scroll[d]) * 0.3

                  self.altitude[d] += self.smooth_scroll[d]
      
                  self.absolute_pos[d] = min(self.absolute_pos[d] + self.smooth_scroll[d], 0)
                  
                  self.prediction[d] = find_end_altitude(self.smooth_scroll[d])

                  pos = [self.absolute_pos[0] * d + ((1 - d) * self.altitude[0]), 
                        self.absolute_pos[1] * (1 - d) + (d * self.altitude[1])]
                  origin = self.blit_to_center(surface, pos, self.timeline[self.center[d]])[d]
                  before = self.timeline[:self.center[d]]
                  before.reverse()
                  before = before[:2]
                  b = self.altitude[d] - origin

                  for n in before:
                        pos = [self.absolute_pos[0] * d + ((1 - d) * b), self.absolute_pos[1] * (1 - d) + (d * b)]
                        x = self.blit_to_center(surface, pos, n)
                        b -= x[d]
                  after = self.timeline[(self.center[d] + 1):]
                  after = after[:2]
                  
                  a = self.altitude[d] + origin
                  for n in after:
                        pos = [self.absolute_pos[0] * d + ((1 - d) * a), self.absolute_pos[1] * (1 - d) + (d * a)]
                        x = self.blit_to_center(surface, pos, n)
                        a += x[d]
                  
                  if abs(self.altitude[d] - origin) < abs(self.altitude[d]):
                        if self.center[d] == 0:
                              self.scroll[d] += change_speed(self.scroll[d], 0)
                              self.altitude[d] += change_speed(self.altitude[d], 0) * 0.5
                        else:
                              self.center[d] -= 1
                              self.altitude[d] = self.altitude[d] - origin
                  elif abs(self.altitude[d] + origin) < abs(self.altitude[d]):
                        if self.center[d] == len(self.timeline) - 1:
                              self.scroll[d] += change_speed(self.scroll[d], 0)
                              self.altitude[d] += change_speed(self.altitude[d], 0) * 0.5   
                        else: 
                              self.center[d] += 1
                              self.altitude[d] = self.altitude[d] + origin

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
      a = delta_v * 0.5 * frame_get()
      return a
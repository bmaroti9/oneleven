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
            self.scroll_y = 0
            self.smooth_scroll_y = 0
            self.altitude_y = 0
            self.center_y = 0
            self.prediction_y = 0

            #requirements for vertical scrolling
            self.scroll_x = 0
            self.smooth_scroll_x = 0
            self.altitude_x = 0
            self.center_x = 0
            self.prediction_x = 0
            

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
      
      def blit_to_center(self, surface, pos, zoom, storage):
            size = (zoom - (abs(pos) * 0.0001)) * self.full_set[1]

            if abs(self.scroll_y) < 20 * self.zoom and abs(self.prediction_y - pos) < size / 2:
                  x = change_speed(self.smooth_scroll_y, pos) * 1.4
                  if abs(x) > 0.15:
                        self.altitude_y += x

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
                              self.add_tile(Music)
                  if event.type == pygame.MOUSEWHEEL:
                        self.scroll_y += event.y * 4
                        self.scroll_y = self.scroll_y * 0.93
                  elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 3:
                              if self.max_zoom == 1: self.max_zoom = 0.5
                              else: self.max_zoom = 1
            if abs(self.smooth_scroll_x) > abs(self.smooth_scroll_y):
                  bigger = self.smooth_scroll_x
            else:
                  bigger = self.smooth_scroll_y
            self.zoom = max(self.max_zoom - abs(((bigger * 0.8) ** 2 * 0.0007)), 0.2)

            self.handle_y(surface)

      def handle_y(self, surface):
            self.scroll_y -= sign_function(self.scroll_y) * 0.5
            self.smooth_scroll_y += (self.scroll_y - self.smooth_scroll_y) * 0.3
            self.altitude_y += self.smooth_scroll_y
            
            self.prediction_y = find_end_altitude(self.smooth_scroll_y)

            origin = self.blit_to_center(surface, self.altitude_y, self.zoom, self.timeline[self.center_y])
            before = self.timeline[:self.center_y]
            before.reverse()
            before = before[:2]
            b = self.altitude_y - origin

            for n in before:
                  x = self.blit_to_center(surface, b, self.zoom, n)
                  b -= x
            after = self.timeline[(self.center_y + 1):]
            after = after[:2]
            
            a = self.altitude_y + origin
            for n in after:
                  x = self.blit_to_center(surface, a, self.zoom, n)
                  a += x
            
            if abs(self.altitude_y - origin) < abs(self.altitude_y):
                  if self.center_y == 0:
                        self.scroll_y += change_speed(self.scroll_y, 0)
                        self.altitude_y += change_speed(self.altitude_y, 0) * 0.5
                  else:
                        self.center_y -= 1
                        self.altitude_y = self.altitude_y - origin
            elif abs(self.altitude_y + origin) < abs(self.altitude_y):
                  if self.center_y == len(self.timeline) - 1:
                        self.scroll_y += change_speed(self.scroll_y, 0)
                        self.altitude_y += change_speed(self.altitude_y, 0) * 0.5   
                  else: 
                        self.center_y += 1
                        self.altitude_y = self.altitude_y + origin

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
import pygame
from pygame.locals import*
import random
from os import listdir
from os.path import isfile, join, basename

from helpers import *
from gradient import *
from settings import *
from designs import textbox


class Folder(pygame.sprite.Sprite):
      def __init__(self, surface, path):
            super().__init__()

            self.name = basename(path)
            self.contents = listdir(path)
            if len(self.contents) > 9:
                  self.contents = self.contents[:9]
            self.contents = self.shorten(self.contents)

            #self.colors = uniform_colors(len(self.contents), file_color(path,  0))
            self.points = []
            self.font = pygame.font.Font('fonts/static/Raleway-ExtraLight.ttf', 200)

            for n in self.contents:
                  self.points.append(generate_number_from_string(path + '/' + n, 1000) * surface.get_width() / 1000)
            self.points.append(surface.get_width())

            self.points = sorted(self.points)
            self.points[0] = 0
            self.surf = pygame.Surface((surface.get_width(), surface.get_height()))
            self.surf.fill((0, 0, 0))
            c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for n in range(len(self.contents)):
                  colorx = file_color(path + '/' + self.contents[n])
                  pygame.draw.rect(self.surf, colorx, 
                  Rect(self.points[n], 0, self.surf.get_width() - self.points[n], self.surf.get_height()))
                  c = [255 - colorx[0], 255 - colorx[1], 255 - colorx[2]]
                  wrighting = self.font.render(self.contents[n], True, c)
                  
                  width = self.points[n + 1] - self.points[n]
                  zoomx = min(min(width, 50) / wrighting.get_height(), 70 / wrighting.get_height())
                  wrighting = pygame.transform.rotozoom(wrighting, -90, zoomx)
                  self.surf.blit(wrighting, [self.points[n], 0])
            
            wrighting = self.font.render(self.name, True, c)
            width = min(surface.get_width() - 60, wrighting.get_width())
            zoomx = width / wrighting.get_width()
            wrighting = pygame.transform.rotozoom(wrighting, 0, zoomx)
            self.surf.blit(wrighting, [0, 300])
                  
            self.surf = self.surf.convert_alpha()
    
      def shorten(self, texts):
            for n in range(len(texts)):
                  if len(texts[n]) > 12:
                        texts[n] = texts[n][:12]
                        texts[n] += '...'
            return texts
    
      def update(self, surface):
            surface.blit(self.surf, [0, 0])
        
class Unloadable(pygame.sprite.Sprite):
      def __init__(self, surface, path):
            super().__init__()

            self.font_200 = pygame.font.Font('fonts/static/Raleway-ExtraLight.ttf', 200)
            self.name = basename(path)
            self.color = file_color(path)
            self.surf = pygame.Surface((surface.get_width(), surface.get_height()))
            self.surf.fill(self.color)
            c = [255 - self.color[0], 255 - self.color[1], 255 - self.color[2]]
            #blit_text(self.surf, c, self.name, [0, 300], self.font_200, 0)
            wrighting = self.font_200.render(self.name, True, c)
            width = min(surface.get_width() - 60, wrighting.get_width())
            zoomx = width / wrighting.get_width()
            wrighting = pygame.transform.rotozoom(wrighting, 0, zoomx)
            self.surf.blit(wrighting, [0, 300])
            self.surf = self.surf.convert_alpha()
      
      def update(self, surface):
            surface.blit(self.surf, [0, 0])

class Image_viewer(pygame.sprite.Sprite):
      def __init__(self, surface, path):
            super().__init__()

            self.image = pygame.image.load(path)
            scalex = surface.get_width() / self.image.get_width()
            scaley = surface.get_height() / self.image.get_height()
            zoom = min(scalex, scaley)
            self.image = pygame.transform.rotozoom(self.image, 0, zoom)
            self.image = self.image.convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = [surface.get_width() / 2, surface.get_height() / 2]
      
      def update(self, surface):
            surface.fill((200, 200, 200))
            surface.blit(self.image, self.rect)

class Email(pygame.sprite.Sprite):
      def __init__(self, surface, path):
            super().__init__()

            self.color = (200, 200, 200)
            self.font = pygame.font.Font('fonts/static/Raleway-ExtraLight.ttf', 30)
            self.font_color = (50, 50, 50)
            self.wirghting = 'hihi'
      
      def update(self, surface):
            surface.fill(self.color)
            events = get_event()
            end_pos = textbox(surface, self.wirghting, 
                              surface.get_width(), [5, 5], self.font, self.font_color)[1]
            if len(self.wirghting) > -1:
                  for event in events:
                        if event.type == KEYDOWN:
                              if event.key == pygame.K_BACKSPACE:
                                    self.wirghting = self.wirghting[:-1]
                              else:
                                    self.wirghting += event.unicode
                  if every_ticks(800, 400):
                        pygame.draw.line(surface, self.font_color, [end_pos[0] + 2, end_pos[1] + 9], 
                                          [end_pos[0] + 2, end_pos[1] + 30], 1)
        
class Box(pygame.sprite.Sprite):
      def __init__(self, surface):
            super().__init__()
            
            self.font = pygame.font.Font('fonts/static/Quicksand-Regular.ttf', 100)
            self.c1 = small_change_to_color((200, 200, 200), 50)
            self.c2 = small_change_to_color(self.c1, 100)
      
      def setup(self):
            x = {
                  'title' : 'Box',
                  'color' : random_paste_color(),
            }
            return x
      
      def update(self, surface, storage):
            #surface.fill(storage['color'])
            cent = [surface.get_width() / 2, surface.get_height() / 2]
            blit_text(surface, (255, 255, 255), str(pygame.time.get_ticks()), cent, self.font, 1)

class Music(pygame.sprite.Sprite):
      def __init__(self, surface):
            super().__init__()

            self.backg = pygame.Surface((surface.get_width(), surface.get_height()))
            self.font = pygame.font.Font('fonts/static/Quicksand-Regular.ttf', 100)
            original_c = small_change_to_color((200, 200, 200), 50)
            gradientRect_w(self.backg, original_c, small_change_to_color(original_c, 100), self.backg.get_rect())

      def setup(self):
            x = {
                  'title' : 'Music',
                  'file' : 'hihi'
            }
            return x

      def update(self, surface, storage):
            #surface.fill((200, 200, 200))
            surface.blit(self.backg, [0, 0])
            blit_text(surface, (255, 255, 255), storage['file'], [50, 50], self.font)

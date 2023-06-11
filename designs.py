import math
import random
import sys
import pygame
from pygame.locals import *
import time
import json
from helpers import *

pygame.init()

def textbox(surface, text, max_width, pos, font, color):
      a = text.split(" ")
      startx = pos[0]
      starty = pos[1]
      pos[0] -= 12
      maximum = startx + max_width
      for n in a:
            pos[0] += 12
            b = font.render(n, True, color)

            assert max_width > b.get_width() + 10
            # always has to be true

            if pos[0] + b.get_width() > maximum:
                  pos[0] = startx
                  pos[1] += 40

            surface.blit(b, pos)
            pos[0] += b.get_width()

      return [(pos[1] + b.get_height()) - starty, pos]


def list_content(surface, content, font, color, spacing, start_pos, line_width, number):
      x = start_pos[0]
      y = start_pos[1]

      for n in content:
            hihi = blit_text(surface, n, font, color, [x, y], 0)

            if line_width != 0:
                  mid = hihi.height / 2 + spacing / 2
                  pygame.draw.line(surface, color, [
                              x, y + mid], [x + line_width, y + mid])

            if number != 0:
                  blit_text(surface, str(content.index(n) + 1) +
                        ".", font, number, [x - 40, y], 0)

            y += spacing


def collapsable(surface, title, content, t_font, c_font, t_color, c_color, spacing, start_pos, line_width):
      test = t_font.render(title, True, (0, 0, 0))

      y = test.get_height()
      x = start_pos[0] - 5 - y * 0.7

      pygame.draw.line(surface, (50, 50, 50), [
                        x, start_pos[1] + (y * 0.2)], [x + y * 0.7, start_pos[1] + (y / 2)], y // 15)
      pygame.draw.line(surface, (50, 50, 50), [
                        x + y * 0.7, start_pos[1] + (y / 2)], [x, start_pos[1] + (y * 0.8)], y // 15)

      button(surface, title, t_font, t_color,
            (0, 0, 0), start_pos, -1, (200, 0, 0))

def list_in_box(surface, font, text_color, box_color, tuch_color, content, pos):
      pressed = None

      x = pos[0]
      y = pos[1]

      hihi = [0, 0]

      for n in content:
            hihi[0] = max(hihi[0], test_text_rect(n[1], font).width + 30)
            hihi[1] += test_text_rect(n[1], font).height + 9

      pygame.draw.rect(surface, box_color, (x, y, hihi[0], hihi[1]))

      for n in content:
            if n[0] == "b":
                  if button(surface, n[1], font, text_color, box_color, [x + 25, y + 3.5, 0], 0, tuch_color):
                        pressed = content.index(n)
            elif n[0] == "t":
                  blit_text(surface, n[1], font, text_color, [x + 10, y], 0)

            y += test_text_rect(n[1], font).height + 10

      return pressed


def plus_minus_button(surface, text_c, tuch_c, caption, number, pos, font, choices=0, rev=1, adon=""):
      a = blit_text(surface, caption, font, text_c, pos, 1)
      size = a[3] // 4

      if isinstance(choices, list):
            longest = Rect(0, 0, 0, 0)
            for n in choices:
                  huhu = test_text_rect(str(n) + adon, font)
                  if huhu.width > longest.width:
                        longest = huhu
      
      center = [(a.midright[0] + size * 6) + longest.width // 2, a.midright[1]]

      if choices == 0:
            disp = str(number) + adon
            b = blit_text(surface, disp, font, text_c, center, 4)
      elif isinstance(choices, list):
            disp = str(choices[number]) + adon
            blit_text(surface, disp, font, text_c, center, 4)  
            b = longest
            b.center = center

      left = [b.midleft[0] - size * 1.5, b.midleft[1] - size * 0]
      right = [b.midright[0] + size * 1.5, b.midright[1] - size * 0]

      ret = number
      if draw_plus_or_minus(surface, left, text_c, tuch_c, size, (False)):
            ret = number - rev
      if draw_plus_or_minus(surface, right, text_c, tuch_c, size, (True)):
            ret = number + rev

      ret = max(ret, 0)
      if choices != 0 and ret > len(choices) - 1:
            ret -= 1

      return ret


def draw_plus_or_minus(surface, pos, color, tuch_color, size, plus_or_minus):
      x = pos[0] - 1
      y = pos[1] - 1

      mouse = pygame.mouse.get_pos()
      dis = distance(pos, mouse)

      if dis < size and check_released(0):
            return True

      if dis < size:
            pygame.draw.circle(surface, tuch_color, pos, size, 0)

      pygame.draw.circle(surface, color, pos, size, 2)

      pygame.draw.line(surface, color, (x - size + 4, y), (x + size - 3, y), 2)

      if plus_or_minus:
            pygame.draw.line(surface, color, (x, y - size + 4),
                              (x, y + size - 3), 2)

            return False

def key_controlls(surface, color, list_of_buttons, list_of_function, font, pos):
      x = pos[0]
      y = pos[1]

      largest = 0

      index = 0
      for n in list_of_buttons:
            n = n.capitalize()
            s = blit_text(surface, n, font, color, [x, y], 4)
            new = list(s.topright)
            s[0] -= 5
            s[2] += 10
            s[1] += 2
            pygame.draw.rect(surface, color, s, 2)

            new[0] += 30
            if largest < new[0]:
                  largest = new[0]

            y += s.height * 1.4
            index += 1
      

      y = pos[1]
      index = 0

      for n in list_of_function:
            s = blit_text(surface, n, font, color, [largest, y], 2)

            y += s.height * 1.4
      
      for n in list_of_buttons:
            a = pygame.key.key_code(n)

            if check_released(str(a)):
                  return n

def straight_listing(surface, color1, color2, item1, item2, start_of_2_pos, font, addon = [1, ""]):
      item1 = list(item1)
      item2 = list(item2)

      x = start_of_2_pos[0]
      y = start_of_2_pos[1]
      longest2 = 0

      for n in item2:
            if addon[0] == 0:
                  hihi = addon[1] + str(n)
            elif addon[0] == 1:
                  hihi = str(n) + addon[1]

            a = blit_text(surface, hihi, font, color2, [x, y], 5)
            if a.width > longest2:
                  longest2 = a.width
            y += a.height * 1.3
      
      longest = find_longest(item1, font)
      clear_pos = x - longest - longest2 - a.height

      y = start_of_2_pos[1]
      for n in item1:
            blit_text(surface, n, font, color1, [clear_pos, y], 2)
            y += a.height * 1.3


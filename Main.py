import pygame
from pygame.locals import *
from datetime import datetime, date
import time

from helpers import *
from managers import *
from settings import *
from supertile import *

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEWHEEL])

SCREEN_WIDTH = 1440 * 1
SCREEN_HEIGHT = 900 * 1

print(pygame.font.get_fonts())

CLOCK = pygame.time.Clock()
pygame.display.set_caption("©2022-2023 Eternal")

# SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN, pygame.SCALED)
SURFACE = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED | pygame.FULLSCREEN
)

SURFACE.fill(get_colors()[0])
blit_image(
    SURFACE,
    "images/eternal_whole.png",
    [SURFACE.get_width() / 2, SURFACE.get_height() / 2],
    0.5,
)
pygame.display.update()

pygame.time.delay(1500)
frame_set(CLOCK.tick(65))

events = pygame.event.get()
upload_event(events)

frame_set(CLOCK.tick(65))

SUPERTILE = Supertile(SURFACE)

BACK = upload_gradient(SURFACE, 150)

RUNNING = True
while RUNNING:
      SCROLLING = 0
      events = pygame.event.get()
      upload_event(events)
      for event in events:
            if event.type == QUIT:
                  RUNNING = False
            if event.type == KEYDOWN:
                  if event.key == K_ESCAPE:
                        RUNNING = False
                  elif event.key == K_0:
                        set_theme(0)
                  elif event.key == K_9:
                        BACK = upload_gradient(SURFACE, 150)

      SURFACE.fill(get_colors()[0])
      SURFACE.blit(BACK, (0, 0))

      if False:
            x = find_end_altitude(SMOOTH_SCROLL)
            requested_altitude = TILE_SPACE.any_close(x, ALTITUDE)
            if requested_altitude != None:
                  if abs(requested_altitude) < 0.5:
                        ALLOWED = False
                  else:
                        ALTITUDE += change_speed(SMOOTH_SCROLL, requested_altitude)

      SUPERTILE.update(SURFACE)

      pygame.display.update()
      frame_set(CLOCK.tick(200))

import os
import pygame
from pygame.locals import *


SCALE = 1

SHIPW = 200 * SCALE
SHIPH = 200 * SCALE

CONFORMITY = .55 # conformity is percentage of tiles per component that should be in frame(defaults to .55)
SIZE = .15 # size is % of frame that must be filled to complete component stage(defaults to .15)
COMPONENTS = 400 # how many components to generate. (defaults to 100)
PLASEMENTS = 1 # how many placements to try before giving up on component placement (defaults to 20)
SEED = None # if None, generate a random seed else use this seed (defaults to None)

BUTTONMARGIN = 48

SCREENWIDTH = 900 * SCALE
SCREENHEIGHT = 600 * SCALE + BUTTONMARGIN

# GRID_W = 16
# GRID_H = 12
GRID_W = SCREENWIDTH // SHIPW
GRID_H = SCREENHEIGHT // SHIPH

SCREEN_SIZE = (SCREENWIDTH, SCREENHEIGHT)
CAPTION = 'Pixel Ship Generator'
FPS = 60



WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (240, 20, 10)
YELLOW = (250, 240, 0)
BLUE = (0, 160, 230)

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pygame.display.set_caption(CAPTION)
SCREEN = pygame.display.set_mode(SCREEN_SIZE, HWSURFACE | DOUBLEBUF)
SCREEN_RECT = SCREEN.get_rect()


def scale(n):
    return n * SCALE


def descale(n):
    return n // SCALE

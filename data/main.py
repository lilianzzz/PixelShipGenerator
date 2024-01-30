import pygame
from pygame.locals import *
from .constants import *
from . import generator as gen
from . import title_screen as tit
from .ship.components.basic_hull import *


class Main(object):
    
    """ Main object for the generator. Handles input and the main loop.
    """
    
    def __init__(self):
    
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.end = False
        self.state = None
        self.gen = None

    def handle_input(self):

        self.state.handle_input()

    def draw(self):

        self.state.draw(self.screen)

    def update(self):

        self.state.update()

    def end_main(self):
        self.end = True

    def show_instructions(self):

        self.gen = self.state
        self.state = tit.Instructions(self)

    def start_generator(self):
        screen = pygame.display.get_surface()
        screen.fill(BLACK)
        self.state = gen.Generator(self)

    def continue_generator(self):
        screen = pygame.display.get_surface()
        screen.fill(BLACK)
        self.state = self.gen

    # main loop for the generator
    def main(self):

        self.state = tit.TitleScreen(self)

        while not self.end:

            self.update()

            self.draw()
            pygame.display.update()

            self.clock.tick(FPS)
            self.handle_input()


def main():
    
    control = Main()
    control.main()

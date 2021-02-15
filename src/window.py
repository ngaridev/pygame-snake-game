
# the simulation window
import pygame

class Window:

    def __init__(self, dimensions, ):
        self.dimensions = dimensions

    def render_window(self):
        return pygame.display.set_mode(self.dimensions)
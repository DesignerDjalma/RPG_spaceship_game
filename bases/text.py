from typing import Tuple
from pygame import Color
import pygame

class Text:
    """Create a text object."""
    def __init__(self, text: str, pos: Tuple[int, int] = (20, 20), **options):
        self.app = options['app']
        self.text = text
        self.pos = pos
        self.fontname = None
        self.fontsize = 72
        self.fontcolor = Color('black')
        self.set_font()
        self.render()

    def set_font(self):
        """Set the font from its name and size."""
        self.font = pygame.font.Font(self.fontname, self.fontsize)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self):
        """Draw the text image to the screen."""
        self.app.screen.blit(self.img, self.rect)


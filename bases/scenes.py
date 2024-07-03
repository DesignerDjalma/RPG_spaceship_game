import pygame
from pygame.locals import *


class Scene:
    """Create a new scene (room, level, view)."""
    id = 0
    bg = Color('gray')

    def __init__(self, *args, **kwargs):
        # Append the new scene and make it the current scene
        self.app = kwargs['app']
        self.app.scenes.append(self)
        self.app.scene = self

        # Set the instance id and increment the class id
        self.id = Scene.id
        Scene.id += 1
        self.nodes = []
        self.bg = Scene.bg
        
    def draw(self):
        """Draw all objects in the scene."""
        self.app.screen.fill(self.bg)
        for node in self.nodes:
            node.draw()
        pygame.display.flip()

    def __str__(self):
        return 'Scene {}'.format(self.id)





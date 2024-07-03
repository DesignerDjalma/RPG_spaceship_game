from typing import List
import pygame
from pygame.locals import *
from text import Text
from scenes import Scene

class App:

    """Create a single-window app with multiple scenes."""

    scene: Scene
    scenes: List[Scene] = []
    
    def __init__(self):
        """Initialize pygame and the application."""

        pygame.init()
        flags = RESIZABLE
        App.screen = pygame.display.set_mode((640, 240), flags)
        App.running = True

        App.t = Text('Pygame App', (20, 20), app=App)

        
    def run(self):
        """Run the main event loop."""
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False
                    pygame.quit()

            App.screen.fill(Color('gray'))
            # App.t.draw(App)
            pygame.display.update()

        pygame.quit()

class Demo(App):
    def __init__(self):
        super().__init__()

        Scene(caption='Intro', app=self)
        Text('Scene 0', app=self)
        Text('Introduction screen the app', app=self)
        Scene(bg=Color('yellow'), caption='Options', app=self)
        Text('Scene 1', app=self)
        Text('Option screen of the app', app=self)
        Scene(bg=Color('green'), caption='Main', app=self)
        Text('Scene 2', app=self)
        Text('Main screen of the app', app=self)
        App.scene = App.scenes[1]


if __name__ == '__main__':
    Demo().run()



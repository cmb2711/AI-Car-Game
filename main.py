import pygame
import random
from level import Level
from ui import UIclass

class Game:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.ui = UIclass(self)
        self.level = Level(self, random.randint(0, 1000))
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
                
            winstate = self.level.update()
            self.ui.draw()
            pygame.display.flip()  # Update the display
            self.clock.tick(60)

            if winstate == None:
                pass
            elif winstate == True:
                self.level = Level(self, random.randint(0, 1000))


# In the main script
game = Game()
game.run()
import pygame
from flag import Flag
from track import Track
from car import Car
from ui import UIclass

# Initialize Pygame
pygame.init()

class Level:
    def __init__(self, game, seed):
        self.game = game
        self.end_level_if_false = True
        self.track = Track(self, 10, 100, 50, seed)
        self.car = Car(self)
        pygame.display.set_caption("Car AI")
        self.winstate = False

    def reset(self, win=False):
        self.car = Car(self)
        if win:
            self.game.ui.attempt = 0
            self.game.ui.score += 1
            self.end_level_if_false = False
            self.winstate = True
        else:
            self.game.ui.attempt += 1

    def update(self):
        if self.end_level_if_false != False:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_level_if_false = False

            self.game.screen.fill((255, 255, 255))  # Fill the screen with white
            self.track.draw()
            self.car.check_collision()
            self.track.draw()
            self.car.update()
            return None
        else:
            return self.winstate

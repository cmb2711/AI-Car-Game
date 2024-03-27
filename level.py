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
            reward += 10
        else:
            self.game.ui.attempt += 1
            reward = -10

    def update(self):
        self.reward = 0
        if self.end_level_if_false != False:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_level_if_false = False

            self.game.screen.fill((255, 255, 255))  # Fill the screen with white
            self.track.draw()
            self.car.check_collision()
            self.track.draw()
            self.car.update()
            return None, self.reward
        else:
            return self.winstate, self.reward

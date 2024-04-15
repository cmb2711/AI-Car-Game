import pygame
from flag import Flag
from track import Track
from car import Car
from ui import UIclass
import math

# Initialize Pygame
pygame.init()

class Level:
    def __init__(self, game, seed):
        self.game = game
        self.end_level_if_false = True
        self.track = Track(self, 5, 100, 50, seed)
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
            self.reward += 1000
        else:
            self.game.ui.attempt += 1
            self.reward = -1000

    def update(self, action=None):
        self.reward = 0
        self.reward += self.car.speed*(math.sin(math.radians(self.car.angle)) - math.sin(math.atan((self.car.y - self.track.flag.y)/(self.car.x - self.track.flag.x+.00001)))) + self.car.speed*(math.cos(math.radians(self.car.angle)) - math.cos(math.atan((self.car.y - self.track.flag.y)/(self.car.x - self.track.flag.x+0.00001))))
        self.reward += self.car.speed

        distance_start_to_flag = math.sqrt((self.car.start_x - self.track.flag.x)**2 + (self.car.start_y - self.track.flag.y)**2)

        dx_flag = self.car.x - self.track.flag.x
        dy_flag = self.car.y - self.track.flag.y
        self.reward -= (math.sqrt(dx_flag**2 + dy_flag**2) - distance_start_to_flag)
        if self.end_level_if_false != False:   
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.end_level_if_false = False

            self.game.screen.fill((255, 255, 255))  # Fill the screen with white
            self.track.draw()
            self.car.check_collision()
            self.track.draw()
            self.car.update(keys = action)
            return None, self.reward
        else:
            return self.winstate, self.reward

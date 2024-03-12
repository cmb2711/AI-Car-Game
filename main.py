import pygame
import math
import random
import time
from flag import Flag
from track import Track
from car import Car
from ui import UIclass

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

class Game:
    def __init__(self, screen_width = 800, screen_height = 600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.track = Track(self, 10, 100, 50, 17001)
        self.car = Car(self)
        self.font = pygame.font.Font(None, 24)
        self.ui = UIclass(self, self.font, self.screen)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Car AI")
        

    def reset(self, win=False):
        self.car = Car(self)
        if win == True:
            self.ui.attempt = 0
            self.ui.score += 1
            seed = random.randint(0, 1000)
            self.track = Track(self, 10, 100, 50, seed)
            self.ui.seed = seed
        else:
            self.ui.attempt += 1



    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.screen.fill((255, 255, 255))  # Fill the screen with white
        self.track.draw()
        self.car.check_collision(self.screen)
        self.track.draw()
        self.car.update()
        self.ui.draw()
        pygame.display.flip()  # Update the display
        self.clock.tick(60)  # Limit the frame rate to 60 FPS

    def run(self):
        while self.running:
            self.update()
        pygame.quit()

# In the main script
game = Game()
game.run()
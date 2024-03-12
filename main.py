import pygame
import random
from flag import Flag
from track import Track
from car import Car
from ui import UIclass

# Initialize Pygame
pygame.init()

class Level:
    def __init__(self, seed, screen_width=800, screen_height=600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.track = Track(self, 10, 100, 50, seed)
        self.car = Car(self)
        self.font = pygame.font.Font(None, 24)
        self.ui = UIclass(self, self.font, self.screen)
        pygame.display.set_caption("Car AI")
        self.winstate = False

    def reset(self, win=False):
        self.car = Car(self)
        if win:
            self.ui.attempt = 0
            self.ui.score += 1
            self.running = False
            self.winstate = True
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
        return self.winstate
        pygame.quit()

class Game:
    def __init__(self):
        pass

    def run(self):
        level = Level(random.randint(0, 1000))
        level.run()

# In the main script
game = Game()
game.run()
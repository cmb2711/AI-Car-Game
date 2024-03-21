import pygame
import random
from level import Level
from ui import UIclass
import sys  # Import the sys module

class Game:
    def __init__(self):
        self.running = True
        self.clock = pygame.time.Clock()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.ui = UIclass(self)
        self.start_screen()

    def start_screen(self):
        while True:
            print("Press 1 for Endless Mode, 2 for Seed Mode")
            choice = input()
            if choice == '1':
                self.run_endless()
            elif choice == '2':
                seed = input("Enter a seed: ")
                self.run_seed(int(seed))

    def run_endless(self):
        pygame.init()
        self.running = True
        self.level = Level(self, random.randint(0, 1000))
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

    def run_seed(self, seed):
        pygame.init()
        self.running = True
        self.level = Level(self, seed)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()  # End the program
            winstate = self.level.update()
            self.ui.draw()
            pygame.display.flip()  # Update the display
            self.clock.tick(60)
            if winstate == None:
                pass
            elif winstate == True:
                self.running = False
                pygame.quit()
                sys.exit()  # End the program

# In the main script
game = Game()
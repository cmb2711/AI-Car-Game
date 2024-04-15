import pygame
import random
from level import Level
from ui import UIclass
import sys  # Import the sys module
from agent import train

class Game:
    def __init__(self):
        self.start_screen()

    def start_screen(self):
        while True:
            print("Press 1 for Endless Mode, 2 for Seed Mode, or 3 to train the AI")
            choice = input()
            self.running = True
            self.clock = pygame.time.Clock()
            self.screen_width = 800
            self.screen_height = 600
            self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
            self.ui = UIclass(self)
            if choice == '1':
                self.run_endless()
            elif choice == '2':
                seed = input("Enter a seed: ")
                self.run_seed(int(seed))
            elif choice == '3':
                self.run_AI()

    def run_endless(self):
        self.frame_iteration = 0
        pygame.init()
        self.running = True
        self.level = Level(self, random.randint(0, 1000))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    return
            winstate, reward = self.level.update()
            self.frame_iteration += 1
            self.ui.draw()
            pygame.display.flip()  # Update the display
            self.clock.tick(60)
            if winstate == None:
                pass
            elif winstate == True or self.frame_iteration > 100:
                self.level = Level(self, random.randint(0, 1000))

    def run_seed(self, seed):
        self.frame_iteration = 0
        pygame.init()
        self.running = True
        self.level = Level(self, seed)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()  # End the program
            winstate, reward = self.level.update()
            self.frame_iteration += 1
            self.ui.draw()
            pygame.display.flip()  # Update the display
            self.clock.tick(60)
            if winstate == None:
                pass
            elif winstate == True or self.frame_iteration > 100:
                self.running = False
                pygame.quit()
                sys.exit()  # End the program

    def run_AI(self):
        self.frame_iteration = 0
        pygame.init()
        self.running = True
        self.level = Level(self, random.randint(0, 1000))
        train(self)

    def resetAI(self):
        self.level = Level(self, random.randint(0, 1000))
        self.frame_iteration = 0

    def play_step(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
        winstate, reward = self.level.update(action = action)
        self.frame_iteration += 1
        if winstate == True or self.frame_iteration > 1000:
            winstate = True
        self.ui.draw()
        pygame.display.flip()
        return reward, winstate, self.ui.score

# In the main script
game = Game()
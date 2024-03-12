import pygame
from main import screen
class Flag:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self):
        flag_x = self.x - self.size / 2
        flag_y = self.y - self.size / 2
        pygame.draw.rect(screen, (0, 0, 255), (flag_x, flag_y, self.size, self.size))
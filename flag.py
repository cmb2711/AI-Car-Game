import pygame
class Flag:
    def __init__(self,level, x, y, size=10):
        self.x = x
        self.y = y
        self.size = size
        self.level = level

    def draw(self):
        flag_x = self.x - self.size / 2
        flag_y = self.y - self.size / 2
        pygame.draw.rect(self.level.game.screen, (0, 0, 255), (flag_x, flag_y, self.size, self.size))
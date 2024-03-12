import pygame
import random
import math
from main import screen_width, screen_height, screen
class Car:
    def __init__(self, x=screen_width / 2, y=screen_height / 2, angle=0, width = 3, height = 6, color = (255, 0, 0)):
        self.start_x = x
        self.start_y = y
        self.start_angle = angle
        self.x = x
        self.y = y
        self.angle = angle
        self.width = width
        self.height = height
        self.color = color
        self.speed = 0
        self.dtheta = 0
    def draw(self):
        # Create a new surface that is large enough to accommodate the car when it's rotated
        car_surface = pygame.Surface((max(self.height, self.width) * 2, max(self.height, self.width) * 2), pygame.SRCALPHA)
        # Draw the car in the center of the new surface
        pygame.draw.rect(car_surface, self.color, pygame.Rect(car_surface.get_height() / 2 - self.width / 2, car_surface.get_width() / 2 - self.width / 2, self.height, self.width))
        # Rotate the surface
        rotated_surface = pygame.transform.rotate(car_surface, -self.angle)  # Adjust the angle
        # Get the rectangle enclosing the rotated surface
        rotated_rect = rotated_surface.get_rect()
        # Set the center of the rectangle to the car's position
        rotated_rect.center = (self.x, self.y)
        # Draw the rotated surface on the screen
        screen.blit(rotated_surface, rotated_rect)
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if self.dtheta > -5:
                self.dtheta -= .1
        if keys[pygame.K_RIGHT]:
            if self.dtheta <5:
                self.dtheta += .1
        if keys[pygame.K_UP]:
            if self.speed < 1:
                self.speed += 0.01
        elif keys[pygame.K_DOWN]:
            if self.speed > -1:
                self.speed -= 0.01
        if self.speed > 0:
            self.speed -= 0.005
        elif self.speed < 0:
            self.speed += 0.005
        if self.dtheta > 0:
            self.dtheta -= 0.035
        elif self.dtheta < 0:
            self.dtheta += 0.035

        self.angle += self.dtheta  # Update the angle based on dtheta
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
        self.draw()

    def raytrace(self, screen, trace_color=(0, 0, 0, 255), distance=100):
        directions = [-180, -90, -45, 0, 45, 90]  # Back, left, front left, front, front right, right
        distances = []

        for direction in directions:
            for d in range(distance):
                x = int(self.x + d * math.cos(math.radians(self.angle + direction)))
                y = int(self.y + d * math.sin(math.radians(self.angle + direction)))

                if 0 <= x < screen.get_width() and 0 <= y < screen.get_height():
                    color = screen.get_at((x, y))
                    if color == trace_color:  # If the pixel is the color we're tracing
                        distances.append(d)
                        break
                else:
                    distances.append(d)
                    break
            else:
                distances.append(distance)

        return distances

    def check_collision(self, screen):
        global game
        distances = self.raytrace(screen, (0, 0, 255, 255))  # Raytrace for blue color
        if distances == [0, 0, 0, 0, 0, 0]:  # If the car is touching the flag
            game.reset(win = True)
        else:
            distances = self.raytrace(screen)  # Raytrace for black color
            if distances == [0, 0, 0, 0, 0, 0]:  # If the car is stuck
                game.reset(win = False)
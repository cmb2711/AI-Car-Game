import pygame
import random
import math
class Car:
    def __init__(self, level, angle=0, width = 3, height = 6, color = (255, 0, 0)):
        self.level=level
        self.x = level.game.screen_width / 2
        self.y = level.game.screen_height / 2
        self.start_x = self.x
        self.start_y = self.y
        self.start_angle = angle
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
        self.level.game.screen.blit(rotated_surface, rotated_rect)
    def get_keys_as_array(self):
        keys = pygame.key.get_pressed()
        return [
            keys[pygame.K_LEFT],
            keys[pygame.K_RIGHT],
            keys[pygame.K_UP],
            keys[pygame.K_DOWN]
        ]
    def update(self, keys=None):
        if keys is None:
            keys = self.get_keys_as_array()
        if keys[0]:
            if self.dtheta > -5:
                self.dtheta -= .1
        if keys[1]:
            if self.dtheta <5:
                self.dtheta += .1
        if keys[2]:
            if self.speed < 1:
                self.speed += 0.01
        elif keys[3]:
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

    def raytrace(self, trace_color=(0, 0, 0, 255), distance=100):
        directions = [-180, -90, -45, 0, 45, 90]  # Back, left, front left, front, front right, right
        distances = []

        for direction in directions:
            for d in range(distance):
                x = int(self.x + d * math.cos(math.radians(self.angle + direction)))
                y = int(self.y + d * math.sin(math.radians(self.angle + direction)))

                if 0 <= x < self.level.game.screen.get_width() and 0 <= y < self.level.game.screen.get_height():
                    color = self.level.game.screen.get_at((x, y))
                    if color == trace_color:  # If the pixel is the color we're tracing
                        distances.append(d)
                        break
                else:
                    distances.append(d)
                    break
            else:
                distances.append(distance)

        return distances

    def check_collision(self):
        distances = self.raytrace((0, 0, 255, 255))  # Raytrace for blue color
        if distances == [0, 0, 0, 0, 0, 0]:  # If the car is touching the flag
            self.level.reset(win = True)
        else:
            distances = self.raytrace()  # Raytrace for black color
            if distances == [0, 0, 0, 0, 0, 0]:  # If the car is stuck
                self.level.reset(win = False)
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

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car AI")

class Flag:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self):
        flag_x = self.x - self.size / 2
        flag_y = self.y - self.size / 2
        pygame.draw.rect(screen, (0, 0, 255), (flag_x, flag_y, self.size, self.size))

class Track:
    def __init__(self, segments, segment_length, track_width, screen_width, screen_height, seed):
        self.segments = segments
        self.segment_length = segment_length
        self.track_width = track_width
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.seed = seed
        random.seed(self.seed)
        self.flag = None  # Initialize the flag as None
        self.generate_track()

    def generate_track(self):
        self.track = []
        self.gray_track = []  # Store the positions of the gray track segments
        direction = pygame.math.Vector2(1, 0)
        center = pygame.math.Vector2(self.screen_width / 2, self.screen_height / 2)
        position = center  # Start from the center of the screen
        max_distance = 0  # Initialize the maximum distance as 0
        grid_size = self.track_width  # Set the grid size to be the same as the track width

        for i in range(self.segments):
            # Round the position to the nearest grid point
            grid_position = pygame.math.Vector2(round(position.x / grid_size) * grid_size, round(position.y / grid_size) * grid_size)
            next_position = position + direction * self.segment_length

            # Check if the next position is within the screen boundaries
            if next_position.x < 0 or next_position.x > self.screen_width or next_position.y < 0 or next_position.y > self.screen_height:
                # If the next position is outside the screen boundaries, reverse the direction
                direction = -direction
                next_position = position + direction * self.segment_length

            if random.random() < 0.9:  # 90% chance to change direction
                # Randomly choose the first direction to simulate
                angles = [90, -90]
                random.shuffle(angles)
                # Simulate the track for each possible direction
                for angle in angles:
                    simulated_direction = direction.rotate(angle)
                    simulated_position = position + simulated_direction * self.segment_length
                    # Check if the simulated position is in the list of the last 5 positions in the track
                    if simulated_position not in self.track[-5:]:
                        direction = simulated_direction  # Change direction if there is no intersection
                        next_position = simulated_position  # Update the next position
                        break
                else:
                    # If both simulations result in an intersection, continue straight
                    next_position = position + direction * self.segment_length

            self.track.append((grid_position.x, grid_position.y))
            position = next_position

            # Add the positions of the gray track segment to the gray track
            for j in range(self.segment_length):
                gray_position = position + direction * j
                # Round the position to the nearest grid point
                grid_gray_position = pygame.math.Vector2(round(gray_position.x / grid_size) * grid_size, round(gray_position.y / grid_size) * grid_size)
                self.gray_track.append(grid_gray_position)

        # Place the flag at the farthest point on the gray track from the center
        for i, gray_position in enumerate(self.gray_track):
            for track_position in self.track:
                if pygame.math.Vector2(gray_position).distance_to(track_position) <= self.track_width / 2:
                    distance = gray_position.distance_to(center)
                    if distance > max_distance:
                        max_distance = distance
                        # Calculate the direction of the track at this point
                        if i > 0 and i < len(self.gray_track) - 1:
                            track_direction = pygame.math.Vector2(self.gray_track[i + 1]) - pygame.math.Vector2(self.gray_track[i - 1])
                            track_direction = track_direction.normalize()
                            # Calculate the perpendicular direction
                            perp_direction = pygame.math.Vector2(-track_direction.y, track_direction.x)
                            # Adjust the flag position to be in the middle of the track
                            flag_position = pygame.math.Vector2(gray_position) + perp_direction * (self.track_width / 4)
                            # Round the flag position to the nearest grid point
                            grid_flag_position = pygame.math.Vector2(round(flag_position.x / grid_size) * grid_size, round(flag_position.y / grid_size) * grid_size)
                            self.flag = Flag(grid_flag_position.x, grid_flag_position.y, 10)  # Set the flag to a new Flag instance
                    break

    def draw(self):
        def draw_adjusted_line(screen, color, start, end, width):
            direction = pygame.math.Vector2(end) - pygame.math.Vector2(start)
            direction = direction.normalize() * (width // 2)
            pygame.draw.line(screen, color, start - direction, end + direction, width)

        # Draw all the black lines
        for i in range(len(self.track) - 1):
            start = pygame.math.Vector2(self.track[i])
            end = pygame.math.Vector2(self.track[i + 1])
            draw_adjusted_line(screen, (0, 0, 0), start, end, self.track_width)  # Black border

        # Draw all the grey lines
        for i in range(len(self.track) - 1):
            start = pygame.math.Vector2(self.track[i])
            end = pygame.math.Vector2(self.track[i + 1])
            direction = (end - start).normalize()
            offset = 0  # Adjust this value to change the length of the offset
            draw_adjusted_line(screen, (128, 128, 128), start, end + direction * offset, self.track_width - 2)  # Grey interior

        self.flag.draw()  # Draw the flag


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



class Game:
    def __init__(self, screen_width, screen_height):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.track = Track(10, 100, 50, screen_width, screen_height, 17001)
        self.car = Car()
        self.font = pygame.font.Font(None, 24)
        self.ui = UIclass(self.font, self.screen)

    def reset(self, win=False):
        self.car = Car()
        if win == True:
            self.ui.attempt = 0
            self.ui.score += 1
            seed = random.randint(0, 1000)
            self.track = Track(10, 100, 50, screen_width, screen_height, seed)
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
game = Game(screen_width, screen_height)
game.run()
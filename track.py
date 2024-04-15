import pygame
import random
from flag import Flag

class Track:
    def __init__(self, level, segments, segment_length, track_width, seed):
        self.segments = segments
        self.segment_length = segment_length
        self.track_width = track_width
        self.level=level
        self.seed = seed
        random.seed(self.seed)
        self.flag = None  # Initialize the flag as None
        self.generate_track()

    def generate_track(self):
        self.track = []
        self.gray_track = []  # Store the positions of the gray track segments
        direction = pygame.math.Vector2(1, 0)
        center = pygame.math.Vector2(self.level.game.screen_width / 2, self.level.game.screen_height / 2)
        position = center  # Start from the center of the screen
        max_distance = 0  # Initialize the maximum distance as 0
        grid_size = self.track_width  # Set the grid size to be the same as the track width

        for i in range(self.segments):
            # Round the position to the nearest grid point
            grid_position = pygame.math.Vector2(round(position.x / grid_size) * grid_size, round(position.y / grid_size) * grid_size)
            next_position = position + direction * self.segment_length

            # Check if the next position is within the screen boundaries
            if next_position.x < 0 or next_position.x > self.level.game.screen_width or next_position.y < 0 or next_position.y > self.level.game.screen_height:
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
                            self.flag = Flag(self.level, grid_flag_position.x, grid_flag_position.y)  # Set the flag to a new Flag instance
                    break

    def draw(self):
        def draw_adjusted_line(screen, color, start, end, width):
            direction = pygame.math.Vector2(end) - pygame.math.Vector2(start)
            if direction.length() > 0:  # Check if the direction vector has a non-zero length
                direction = direction.normalize() * (width // 2)
                pygame.draw.line(screen, color, start - direction, end + direction, width)

        # Draw all the black lines
        for i in range(len(self.track) - 1):
            start = pygame.math.Vector2(self.track[i])
            end = pygame.math.Vector2(self.track[i + 1])
            draw_adjusted_line(self.level.game.screen, (0, 0, 0), start, end, self.track_width)  # Black border

        # Draw all the grey lines
        for i in range(len(self.track) - 1):
            start = pygame.math.Vector2(self.track[i])
            end = pygame.math.Vector2(self.track[i + 1])
            if start != end:  # Check if start and end are not the same
                direction = (end - start).normalize()
                offset = 0  # Adjust this value to change the length of the offset
                draw_adjusted_line(self.level.game.screen, (128, 128, 128), start, end + direction * offset, self.track_width - 2)  # Grey interior

        self.flag.draw()  # Draw the flag
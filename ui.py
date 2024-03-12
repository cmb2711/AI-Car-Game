import pygame

class UIclass:
    def __init__(self, font, screen):
        self.font = font
        self.screen = screen
        self.start_time = pygame.time.get_ticks()  # Store the start time
        self.seed = 0
        self.score = 0
        self.attempt = 0

    def draw(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Calculate the elapsed time in seconds
        time_text = self.font.render(f'Time: {elapsed_time:.2f}', True, (255, 255, 255), (0, 0, 0))
        seed_text = self.font.render(f'Seed: {self.seed}', True, (255, 255, 255), (0, 0, 0))
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255), (0, 0, 0))
        attempt_text = self.font.render(f'Attempt: {self.attempt}', True, (255, 255, 255), (0, 0, 0))

        self.screen.blit(time_text, (10, 10))
        self.screen.blit(seed_text, (10, 40))
        self.screen.blit(score_text, (10, 70))
        self.screen.blit(attempt_text, (10, 100))
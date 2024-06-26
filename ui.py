import pygame

class UIclass:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 24)
        self.screen = self.game.screen
        self.start_time = pygame.time.get_ticks()  # Store the start time
        self.seed = 0
        self.score = 0
        self.attempt = 0
        self.frame_iteration = 0

    def draw(self):
        self.seed = self.game.level.track.seed

        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Calculate the elapsed time in seconds
        time_text = self.font.render(f'Time: {elapsed_time:.2f}', True, (255, 255, 255), (0, 0, 0))
        seed_text = self.font.render(f'Seed: {self.seed}', True, (255, 255, 255), (0, 0, 0))
        score_text = self.font.render(f'Score: {self.score}', True, (255, 255, 255), (0, 0, 0))
        attempt_text = self.font.render(f'Attempt: {self.attempt}', True, (255, 255, 255), (0, 0, 0))
        iteration_text = self.font.render(f'Iteration: {self.game.frame_iteration}', True, (255, 255, 255), (0, 0, 0))

        self.screen.blit(time_text, (10, 10))
        self.screen.blit(seed_text, (10, 40))
        self.screen.blit(score_text, (10, 70))
        self.screen.blit(attempt_text, (10, 100))
        self.screen.blit(iteration_text, (10, 130))
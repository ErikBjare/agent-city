import pygame
from typing import Optional
from dataclasses import dataclass

@dataclass
class GameConfig:
    width: int = 800
    height: int = 600
    fps: int = 60
    title: str = "Agent City"

class Game:
    def __init__(self, config: Optional[GameConfig] = None):
        pygame.init()
        self.config = config or GameConfig()
        self.screen = pygame.display.set_mode((self.config.width, self.config.height))
        pygame.display.set_caption(self.config.title)
        self.clock = pygame.time.Clock()
        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Add more event handling here

    def update(self):
        # Will be expanded with city and agent updates
        pass

    def render(self):
        self.screen.fill((255, 255, 255))  # White background
        # Will be expanded with city and agent rendering
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.config.fps)

        pygame.quit()

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
        print("Initializing pygame...")
        pygame.init()
        self.config = config or GameConfig()
        print(f"Creating window {self.config.width}x{self.config.height}")
        self.screen = pygame.display.set_mode((self.config.width, self.config.height))
        pygame.display.set_caption(self.config.title)
        self.clock = pygame.time.Clock()
        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit event received")
                self.running = False

    def update(self):
        pass

    def render(self):
        self.screen.fill((255, 255, 255))  # White background
        pygame.display.flip()

    def run(self):
        print("Base game loop starting...")
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.config.fps)
        print("Game loop ended")
        pygame.quit()

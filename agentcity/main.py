import traceback

import pygame

from .engine.game import Game, GameConfig
from .engine.time_system import TimeSystem
from .entities.agent import Agent
from .world.city import City


class AgentCity(Game):
    def __init__(self):
        super().__init__(GameConfig(width=800, height=600, title="Agent City"))

        # Initialize systems
        self.time_system = TimeSystem()
        self.city = City(self.config.width, self.config.height)

        # Add some initial agents
        self._add_initial_agents()

        # Debug flags
        self.show_debug = False
        self.show_stats = False
        self.time_scale = 1.0

    def _add_initial_agents(self):
        """Add some initial agents to the city"""
        initial_agents = [
            ("Alice", (100, 100)),
            ("Bob", (200, 200)),
            ("Charlie", (300, 300)),
            ("Diana", (400, 400)),
        ]

        for name, pos in initial_agents:
            self.city.add_agent(Agent(name, pos))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)

    def _handle_keypress(self, event):
        if event.key == pygame.K_SPACE:
            # Toggle time scale between 1x and 3x
            self.time_scale = 3.0 if self.time_scale == 1.0 else 1.0
        elif event.key == pygame.K_d:
            # Toggle debug info
            self.show_debug = not self.show_debug
        elif event.key == pygame.K_s:
            # Toggle stats
            self.show_stats = not self.show_stats

    def _handle_mouse_click(self, event):
        # Send nearest agent to clicked location
        pos = event.pos
        if self.city.agents:
            nearest_agent = min(
                self.city.agents,
                key=lambda a: (
                    (a.state.position[0] - pos[0]) ** 2
                    + (a.state.position[1] - pos[1]) ** 2
                ),
            )
            nearest_agent.set_destination(pos)

    def update(self):
        delta_time = self.clock.get_time() / 1000.0  # Convert to seconds

        # Update time system
        self.time_system.update(delta_time * self.time_scale)

        # Update city and agents using game time
        self.city.update(
            time_of_day=self.time_system.time.time_of_day,
            current_hour=self.time_system.time.hour,
            ticks_per_hour=self.time_system.ticks_per_hour,
        )

    def render(self):
        # Clear screen with sky color
        sky_color = (
            (150, 200, 255) if not self.time_system.time.is_night else (20, 20, 50)
        )
        self.screen.fill(sky_color)

        # Render city
        self.city.render(self.screen)

        # Render time
        self.time_system.render(self.screen)

        # Render debug info if enabled
        if self.show_debug:
            self._render_debug_info()

        # Render stats if enabled
        if self.show_stats:
            self._render_stats()

        pygame.display.flip()

    def _render_debug_info(self):
        font = pygame.font.Font(None, 24)
        y = 40  # Start below time display

        for agent in self.city.agents:
            status = agent.get_status()
            text = f"{status['name']}: {status['action']} - {status['needs']}"
            text_surface = font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (10, y))
            y += 20

    def _render_stats(self):
        font = pygame.font.Font(None, 24)
        stats = self.city.get_building_stats()
        y = 40

        for building_type, count in stats.items():
            text = f"{building_type}: {count}"
            text_surface = font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (self.config.width - 150, y))
            y += 20


def main():
    try:
        game = AgentCity()
        game.run()
    except Exception as e:
        print("Error occurred:", str(e))
        print("Traceback:")
        traceback.print_exc()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()

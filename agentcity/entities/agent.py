import hashlib
from dataclasses import dataclass

import pygame

from ..ai.behaviors import Behavior
from ..ai.behaviors.needs import EatBehavior, RestBehavior, SocializeBehavior
from ..ai.behaviors.wandering import WanderingBehavior
from ..ai.needs import NeedsSystem


@dataclass
class AgentState:
    position: tuple[float, float]
    current_action: str = "idle"
    destination: tuple[float, float] | None = None
    speed: float = 3.0  # pixels per tick (180 pixels/sec at 60 FPS)


class Agent:
    def __init__(self, name: str, position: tuple[float, float], city=None):
        self.name = name
        self.state = AgentState(position=position)
        self.needs = NeedsSystem()
        self.city = city

        # Behaviors in priority order (needs first, then wandering)
        self.behaviors = [
            RestBehavior(),
            EatBehavior(),
            SocializeBehavior(),
            WanderingBehavior(),
        ]
        self.active_behavior: Behavior | None = None

        # Temporary visualization
        self.size = 20
        self.color = (0, 0, 255)  # Blue

        # Customization
        self.personality_color = self._generate_personality_color()

    def _generate_personality_color(self) -> tuple[int, int, int]:
        """Generate a unique color based on the agent's name"""
        # Generate a hash from the name
        name_hash = hashlib.md5(self.name.encode()).hexdigest()
        # Use the first 6 characters for RGB values
        r = int(name_hash[:2], 16)
        g = int(name_hash[2:4], 16)
        b = int(name_hash[4:6], 16)
        return (r, g, b)

    def update(self, time_of_day: str, available_buildings: list[str]):
        """Update agent state and behaviors each tick"""
        # Handle behaviors
        if self.active_behavior:
            # Update current behavior
            self.active_behavior.update(self)
            if not self.active_behavior.state.active:
                self.active_behavior = None
        else:
            # Check behaviors in priority order
            highest_priority: float = -1.0  # Allow behaviors with priority 0
            selected_behavior = None

            for behavior in self.behaviors:
                if behavior.should_activate(self):
                    priority = behavior.get_priority(self)
                    if priority > highest_priority:
                        highest_priority = priority
                        selected_behavior = behavior

            if selected_behavior:
                self.active_behavior = selected_behavior

        # Move towards destination if one exists
        if self.state.destination:
            dx = self.state.destination[0] - self.state.position[0]
            dy = self.state.destination[1] - self.state.position[1]
            distance = (dx**2 + dy**2) ** 0.5

            if distance < self.state.speed:  # Can reach destination in this tick
                self.state.position = self.state.destination
                self.state.destination = None

            else:
                # Move one tick's worth of distance
                self.state.position = (
                    self.state.position[0] + (dx / distance) * self.state.speed,
                    self.state.position[1] + (dy / distance) * self.state.speed,
                )

    def set_destination(self, destination: tuple[float, float]):
        """Set a new destination for the agent"""
        self.state.destination = destination
        # Keep the current action, don't override with "moving"

    def render(self, screen: pygame.Surface):
        """Render the agent"""
        # Draw agent circle with personality color
        pygame.draw.circle(
            screen,
            self.personality_color,
            (int(self.state.position[0]), int(self.state.position[1])),
            self.size,
        )

        # Draw a smaller inner circle with color based on most urgent need
        most_urgent_need = self.needs.get_most_urgent_need()
        inner_color = self._get_need_color(most_urgent_need)
        pygame.draw.circle(
            screen,
            inner_color,
            (int(self.state.position[0]), int(self.state.position[1])),
            self.size // 2,
        )

        # Draw destination if exists
        if self.state.destination:
            pygame.draw.circle(
                screen,
                (255, 0, 0),  # Red
                (int(self.state.destination[0]), int(self.state.destination[1])),
                5,
                1,  # Line width
            )

    def _get_need_color(self, need_name: str) -> tuple[int, int, int]:
        """Get color based on need type"""
        need_colors = {
            "energy": (255, 255, 0),  # Yellow
            "hunger": (255, 165, 0),  # Orange
            "social": (147, 112, 219),  # Purple
        }
        return need_colors.get(need_name, (128, 128, 128))  # Gray for unknown needs

    def get_status(self) -> dict:
        """Get a dictionary of the agent's current status"""
        return {
            "name": self.name,
            "position": self.state.position,
            "action": self.state.current_action,
            "most_urgent_need": self.needs.get_most_urgent_need(),
            "needs": {name: need.current for name, need in self.needs.needs.items()},
        }

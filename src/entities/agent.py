import pygame
import hashlib
from typing import Tuple, Optional, List
from dataclasses import dataclass
from src.ai.needs import NeedsSystem
from src.ai.brain import AgentBrain, Decision

@dataclass
class AgentState:
    position: Tuple[float, float]
    current_action: str = "idle"
    destination: Optional[Tuple[float, float]] = None
    speed: float = 100.0  # pixels per second
    last_decision_time: float = 0.0  # Track when we last made a decision

class Agent:
    def __init__(self, name: str, position: Tuple[float, float]):
        self.name = name
        self.state = AgentState(position=position)
        self.needs = NeedsSystem()
        self.brain = AgentBrain()
        
        # Temporary visualization
        self.size = 20
        self.color = (0, 0, 255)  # Blue
        
        # Customization
        self.personality_color = self._generate_personality_color()

    def _generate_personality_color(self) -> Tuple[int, int, int]:
        """Generate a unique color based on the agent's name"""
        # Generate a hash from the name
        name_hash = hashlib.md5(self.name.encode()).hexdigest()
        # Use the first 6 characters for RGB values
        r = int(name_hash[:2], 16)
        g = int(name_hash[2:4], 16)
        b = int(name_hash[4:6], 16)
        return (r, g, b)

    def update(self, delta_time: float, time_of_day: str, available_buildings: List[str]):
        """Update agent state, needs, and make decisions"""
        # Update needs
        self.needs.update(delta_time)
        
        # Update decision timer
        self.state.last_decision_time += delta_time
        
        # Move towards destination if one exists
        if self.state.destination:
            dx = self.state.destination[0] - self.state.position[0]
            dy = self.state.destination[1] - self.state.position[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance < 1:  # Arrived at destination
                self.state.position = self.state.destination
                self.state.destination = None
                if self.state.current_action == "wandering":
                    self.state.current_action = "idle"
            else:
                # Normalize direction and apply speed
                move_distance = min(distance, self.state.speed * delta_time)
                self.state.position = (
                    self.state.position[0] + (dx / distance) * move_distance,
                    self.state.position[1] + (dy / distance) * move_distance
                )

    def _make_decision(self, time_of_day: str, available_buildings: List[str]):
        """Make a decision about what to do next"""
        needs_status = {name: need.current for name, need in self.needs.needs.items()}
        decision = self.brain.make_decision(
            needs_status,
            self.state.current_action,
            time_of_day,
            available_buildings
        )
        
        if self.brain.should_change_action(self.state.current_action, decision):
            self.state.current_action = decision.action
            return decision
        return None

    def set_destination(self, destination: Tuple[float, float], action: str = "moving"):
        """Set a new destination for the agent"""
        self.state.destination = destination
        self.state.current_action = action

    def render(self, screen: pygame.Surface):
        """Render the agent"""
        # Draw agent circle with personality color
        pygame.draw.circle(
            screen, 
            self.personality_color,
            (int(self.state.position[0]), int(self.state.position[1])),
            self.size
        )
        
        # Draw a smaller inner circle with color based on most urgent need
        most_urgent_need = self.needs.get_most_urgent_need()
        inner_color = self._get_need_color(most_urgent_need)
        pygame.draw.circle(
            screen,
            inner_color,
            (int(self.state.position[0]), int(self.state.position[1])),
            self.size // 2
        )
        
        # Draw destination if exists
        if self.state.destination:
            pygame.draw.circle(
                screen,
                (255, 0, 0),  # Red
                (int(self.state.destination[0]), int(self.state.destination[1])),
                5,
                1  # Line width
            )

    def _get_need_color(self, need_name: str) -> Tuple[int, int, int]:
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
            "needs": {name: need.current for name, need in self.needs.needs.items()}
        }

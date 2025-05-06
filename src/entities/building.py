from dataclasses import dataclass
from typing import Tuple, List, Dict
import pygame

@dataclass
class BuildingType:
    name: str
    color: Tuple[int, int, int]
    satisfies_needs: Dict[str, float]  # need_name -> satisfaction_rate_per_hour

class Building:
    def __init__(
        self,
        building_type: BuildingType,
        position: Tuple[float, float],
        size: Tuple[float, float]
    ):
        self.building_type = building_type
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        
        # Entry/exit point for agents
        self.entrance = (
            position[0] + size[0] / 2,
            position[1] + size[1]  # Bottom center
        )

    def render(self, screen: pygame.Surface):
        """Render the building"""
        pygame.draw.rect(screen, self.building_type.color, self.rect)
        
        # Draw entrance point
        pygame.draw.circle(screen, (0, 255, 0), 
                         (int(self.entrance[0]), int(self.entrance[1])), 5)

# Define common building types
BUILDING_TYPES = {
    "house": BuildingType(
        name="House",
        color=(150, 75, 0),  # Brown
        satisfies_needs={"energy": 25.0}  # Recover energy while sleeping
    ),
    "restaurant": BuildingType(
        name="Restaurant",
        color=(255, 0, 0),  # Red
        satisfies_needs={"hunger": 50.0}  # Recover hunger quickly
    ),
    "park": BuildingType(
        name="Park",
        color=(0, 255, 0),  # Green
        satisfies_needs={"social": 10.0}  # Slowly satisfy social needs
    ),
}

from dataclasses import dataclass

import pygame

from .objects import WorldObject


@dataclass
class BuildingType:
    name: str
    color: tuple[int, int, int]
    default_objects: list[str]  # List of object types to place in this building


class Building:
    def __init__(
        self,
        building_type: BuildingType,
        position: tuple[float, float],
        size: tuple[float, float],
    ):
        self.building_type = building_type
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position[0], position[1], size[0], size[1])
        self.objects: list[WorldObject] = []

        # Entry/exit point for agents
        self.entrance = (
            position[0] + size[0] / 2,
            position[1] + size[1],  # Bottom center
        )

        # Place default objects
        self._place_default_objects()

    def _place_default_objects(self):
        """Place the default objects for this building type"""
        from random import randint

        for obj_type in self.building_type.default_objects:
            # Place object at random position within building
            obj_pos = (
                randint(
                    int(self.position[0] + 10),
                    int(self.position[0] + self.size[0] - 10),
                ),
                randint(
                    int(self.position[1] + 10),
                    int(self.position[1] + self.size[1] - 10),
                ),
            )
            from .objects import OBJECT_TYPES, WorldObject

            self.objects.append(
                WorldObject(obj_type, obj_pos, OBJECT_TYPES[obj_type][:])
            )

    def get_available_capabilities(self) -> list[str]:
        """Get list of all capabilities provided by objects in this building"""
        capabilities = set()
        for obj in self.objects:
            for cap in obj.capabilities:
                capabilities.add(cap.name)

        return list(capabilities)

    def find_object_with_capability(
        self, capability: str, agent_name: str
    ) -> WorldObject | None:
        """Find an available object that provides the given capability"""
        for obj in self.objects:
            if any(cap.name == capability for cap in obj.capabilities) and obj.can_use(
                agent_name
            ):
                return obj
        return None

    def render(self, screen: pygame.Surface):
        """Render the building"""
        pygame.draw.rect(screen, self.building_type.color, self.rect)

        # Draw entrance point
        pygame.draw.circle(
            screen, (0, 255, 0), (int(self.entrance[0]), int(self.entrance[1])), 5
        )

        # Draw objects (as small circles)
        for obj in self.objects:
            pygame.draw.circle(
                screen,
                (200, 200, 200),  # Light gray
                (int(obj.position[0]), int(obj.position[1])),
                3,
            )


# Define common building types with their default objects
BUILDING_TYPES = {
    "house": BuildingType(
        name="House",
        color=(150, 75, 0),  # Brown
        default_objects=["bed", "kitchen"],
    ),
    "restaurant": BuildingType(
        name="Restaurant",
        color=(255, 0, 0),  # Red
        default_objects=["table", "table", "kitchen"],  # Multiple tables
    ),
    "park": BuildingType(
        name="Park",
        color=(0, 255, 0),  # Green
        default_objects=["bench", "bench", "trail"],
    ),
}

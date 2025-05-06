import pygame

from ..ai.behaviors.needs import NeedBehavior
from ..entities.agent import Agent
from ..entities.building import BUILDING_TYPES, Building


class City:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.buildings: list[Building] = []
        self.agents: list[Agent] = []
        self.current_tick = 0

        # Create initial city layout
        self._create_initial_layout()

        # Cache available building types
        self.available_building_types = self._get_available_building_types()

    def _create_initial_layout(self):
        """Create a simple initial city layout with some buildings"""
        # Create a row of houses on the top
        house_width, house_height = 60, 80
        for i in range(4):
            self.buildings.append(
                Building(
                    BUILDING_TYPES["house"],
                    position=(50 + i * (house_width + 20), 50),
                    size=(house_width, house_height),
                )
            )

        # Add restaurants in the middle
        self.buildings.append(
            Building(BUILDING_TYPES["restaurant"], position=(200, 200), size=(100, 80))
        )
        self.buildings.append(
            Building(BUILDING_TYPES["restaurant"], position=(400, 200), size=(100, 80))
        )

        # Add parks at the bottom
        self.buildings.append(
            Building(BUILDING_TYPES["park"], position=(50, 350), size=(150, 100))
        )
        self.buildings.append(
            Building(BUILDING_TYPES["park"], position=(300, 350), size=(150, 100))
        )

    def _get_available_building_types(self) -> list[str]:
        """Get a list of all building types present in the city"""
        return list(set(b.building_type.name for b in self.buildings))

    def add_agent(self, agent: Agent):
        """Add a new agent to the city"""
        agent.city = self  # Set the city reference
        self.agents.append(agent)

    def get_nearest_building_of_type(
        self, position: tuple[float, float], building_type: str
    ) -> Building | None:
        """Find the nearest building of a specific type"""
        buildings_of_type = [
            b for b in self.buildings if b.building_type.name == building_type
        ]
        if not buildings_of_type:
            return None

        return min(
            buildings_of_type,
            key=lambda b: (
                (b.entrance[0] - position[0]) ** 2 + (b.entrance[1] - position[1]) ** 2
            ),
        )

    def get_building_at_position(
        self, position: tuple[float, float]
    ) -> Building | None:
        """Get building at the given position, if any"""
        for building in self.buildings:
            if building.rect.collidepoint(position):
                return building
        return None

    def update(self, time_of_day: str, current_hour: int, ticks_per_hour: int):
        """Update all agents in the city on each tick"""
        # Calculate time factors
        hour_progress = 1.0 / ticks_per_hour  # How much of an hour each tick represents

        self.current_tick = (self.current_tick + 1) % ticks_per_hour

        for agent in self.agents:
            # Update agent behavior
            agent.update(time_of_day, self.available_building_types)

            # Update needs based on game time
            agent.needs.update(hour_progress)

            # Handle building interactions
            if not agent.state.destination:  # Agent has stopped moving
                building = self.get_building_at_position(agent.state.position)
                if building:
                    self._handle_building_interaction(agent, building, hour_progress)

    def _handle_building_interaction(
        self, agent: Agent, building: Building, hour_progress: float
    ):
        """Handle agent interaction with objects in a building"""
        if agent.active_behavior and isinstance(agent.active_behavior, NeedBehavior):
            behavior = agent.active_behavior
            if behavior.using_object:
                # Apply object's capability effects
                for cap in behavior.using_object.capabilities:
                    if cap.name == behavior.required_capability:
                        # Scale satisfaction rate to game time
                        tick_satisfaction = cap.satisfaction_rate * hour_progress
                        agent.needs.satisfy_need(behavior.need_name, tick_satisfaction)

    def render(self, screen: pygame.Surface):
        """Render the entire city"""
        # Draw buildings
        for building in self.buildings:
            building.render(screen)

        # Draw agents
        for agent in self.agents:
            agent.render(screen)

        # Draw status table
        self._render_status_table(screen)

    def _render_status_table(self, screen: pygame.Surface):
        """Render a table showing agent status"""
        font = pygame.font.Font(None, 24)
        row_height = 25
        col_widths = [80, 120, 80, 80, 80]  # Widths for each column
        table_width = sum(col_widths)

        # Table position (bottom left)
        x = 10
        y = screen.get_height() - (len(self.agents) + 1) * row_height - 10

        # Draw header
        headers = ["Name", "Action", "Energy", "Hunger", "Social"]
        current_x = x
        for header, width in zip(headers, col_widths):
            text = font.render(header, True, (0, 0, 0))
            screen.blit(text, (current_x, y))
            current_x += width

        # Draw agent rows
        for i, agent in enumerate(self.agents):
            status = agent.get_status()
            y_pos = y + (i + 1) * row_height

            # Draw row background (alternating colors)
            row_rect = pygame.Rect(x, y_pos, table_width, row_height)
            pygame.draw.rect(
                screen, (240, 240, 240) if i % 2 == 0 else (220, 220, 220), row_rect
            )

            # Draw cells
            cells = [
                status["name"],
                status["action"],
                f"{status['needs']['energy']:.1f}",
                f"{status['needs']['hunger']:.1f}",
                f"{status['needs']['social']:.1f}",
            ]

            current_x = x
            for cell, width in zip(cells, col_widths):
                text = font.render(cell, True, (0, 0, 0))
                screen.blit(text, (current_x, y_pos + 5))  # +5 for vertical centering
                current_x += width

    def get_random_position(self) -> tuple[float, float]:
        """Get a random position within the city bounds"""
        from random import randint

        return (
            randint(self.width // 10, self.width * 9 // 10),
            randint(self.height // 10, self.height * 9 // 10),
        )

    def get_building_stats(self) -> dict[str, int]:
        """Get statistics about buildings in the city"""
        stats: dict[str, int] = {}
        for building in self.buildings:
            building_type = building.building_type.name
            stats[building_type] = stats.get(building_type, 0) + 1
        return stats

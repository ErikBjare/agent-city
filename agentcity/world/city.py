from typing import List, Tuple, Optional, Dict
import pygame
from ..entities.building import Building, BUILDING_TYPES
from ..entities.agent import Agent

class City:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.buildings: List[Building] = []
        self.agents: List[Agent] = []
        
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
                    size=(house_width, house_height)
                )
            )
        
        # Add restaurants in the middle
        self.buildings.append(
            Building(
                BUILDING_TYPES["restaurant"],
                position=(200, 200),
                size=(100, 80)
            )
        )
        self.buildings.append(
            Building(
                BUILDING_TYPES["restaurant"],
                position=(400, 200),
                size=(100, 80)
            )
        )
        
        # Add parks at the bottom
        self.buildings.append(
            Building(
                BUILDING_TYPES["park"],
                position=(50, 350),
                size=(150, 100)
            )
        )
        self.buildings.append(
            Building(
                BUILDING_TYPES["park"],
                position=(300, 350),
                size=(150, 100)
            )
        )

    def _get_available_building_types(self) -> List[str]:
        """Get a list of all building types present in the city"""
        return list(set(b.building_type.name for b in self.buildings))

    def add_agent(self, agent: Agent):
        """Add a new agent to the city"""
        self.agents.append(agent)

    def get_nearest_building_of_type(self, position: Tuple[float, float], building_type: str) -> Optional[Building]:
        """Find the nearest building of a specific type"""
        buildings_of_type = [b for b in self.buildings if b.building_type.name == building_type]
        if not buildings_of_type:
            return None
            
        return min(
            buildings_of_type,
            key=lambda b: ((b.entrance[0] - position[0])**2 + (b.entrance[1] - position[1])**2)
        )

    def get_building_at_position(self, position: Tuple[float, float]) -> Optional[Building]:
        """Get building at the given position, if any"""
        for building in self.buildings:
            if building.rect.collidepoint(position):
                return building
        return None

    def update(self, delta_time: float, time_of_day: str):
        """Update all agents in the city"""
        for agent in self.agents:
            # First handle agent's basic update
            agent.update(delta_time, time_of_day, self.available_building_types)
            
            # Handle agent decisions
            if agent.state.last_decision_time >= 1.0:
                decision = agent._make_decision(time_of_day, self.available_building_types)
                agent.state.last_decision_time = 0.0
                
                # If we got a decision with a building type, find nearest building
                if decision and decision.target_building_type:
                    nearest = self.get_nearest_building_of_type(agent.state.position, decision.target_building_type)
                    if nearest:
                        agent.set_destination(nearest.entrance, decision.action)
                elif agent.state.current_action in ["idle", "wandering"]:
                    # Occasionally make agents wander
                    import random
                    if random.random() < 0.1:  # 10% chance each decision time
                        random_pos = self.get_random_position()
                        agent.set_destination(random_pos, "wandering")
            
            # Check if agent has reached a building
            if not agent.state.destination:  # Agent has stopped moving
                building = self.get_building_at_position(agent.state.position)
                if building:
                    self._handle_building_interaction(agent, building, delta_time)

    def _handle_building_interaction(self, agent: Agent, building: Building, delta_time: float):
        """Handle agent interaction with a building"""
        # Apply building effects to agent needs
        for need_name, satisfaction_rate in building.building_type.satisfies_needs.items():
            if need_name in agent.needs.needs:
                agent.needs.satisfy_need(need_name, satisfaction_rate * delta_time)

    def render(self, screen: pygame.Surface):
        """Render the entire city"""
        # Draw buildings
        for building in self.buildings:
            building.render(screen)
            
        # Draw agents
        for agent in self.agents:
            agent.render(screen)

    def get_random_position(self) -> Tuple[float, float]:
        """Get a random position within the city bounds"""
        from random import randint
        return (
            randint(self.width // 10, self.width * 9 // 10),
            randint(self.height // 10, self.height * 9 // 10)
        )

    def get_building_stats(self) -> Dict[str, int]:
        """Get statistics about buildings in the city"""
        stats = {}
        for building in self.buildings:
            building_type = building.building_type.name
            stats[building_type] = stats.get(building_type, 0) + 1
        return stats

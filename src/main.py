import pygame
from engine.game import Game, GameConfig
from engine.time_system import TimeSystem, ScheduledEvent
from world.city import City
from entities.agent import Agent

class AgentCityGame(Game):
    def __init__(self):
        super().__init__(GameConfig(width=1024, height=768, title="Agent City"))
        
        # Initialize systems
        self.time_system = TimeSystem()
        self.city = City(width=self.config.width, height=self.config.height)
        
        # Create some initial agents
        self._create_initial_agents()
        
        # UI settings
        self.debug_mode = True
        self.show_stats = True
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)

    def _create_initial_agents(self):
        """Create initial agents in the city"""
        agent_names = [
            "Bob", "Alice", "Charlie", "Diana", 
            "Eve", "Frank", "Grace", "Henry"
        ]
        
        for name in agent_names:
            pos = self.city.get_random_position()
            self.city.add_agent(Agent(name, pos))

        # Set up some scheduled events
        self._setup_scheduled_events()

    def _setup_scheduled_events(self):
        """Set up scheduled events throughout the day"""
        # Night time - send agents home
        self.time_system.schedule_event(
            ScheduledEvent(
                hour=22,
                callback=lambda: self._send_agents_to_buildings("house"),
                description="Send agents home for the night"
            )
        )
        
        # Morning - wake up time
        self.time_system.schedule_event(
            ScheduledEvent(
                hour=6,
                callback=self._morning_routine,
                description="Morning routine"
            )
        )
        
        # Lunch time
        self.time_system.schedule_event(
            ScheduledEvent(
                hour=12,
                callback=lambda: self._send_some_agents_to_buildings("restaurant", 0.5),
                description="Lunch time"
            )
        )

    def _morning_routine(self):
        """Handle morning activities"""
        for agent in self.city.agents:
            if agent.state.current_action == "going_to_house":
                if agent.needs.needs["hunger"].current < 50:
                    # Send hungry agents to restaurant
                    nearest_restaurant = self.city.get_nearest_building_of_type(
                        agent.state.position, 
                        "restaurant"
                    )
                    if nearest_restaurant:
                        agent.set_destination(nearest_restaurant.entrance, "seeking_food")
                else:
                    # Others can go to park or wander
                    if pygame.time.get_ticks() % 2 == 0:  # Random choice
                        nearest_park = self.city.get_nearest_building_of_type(
                            agent.state.position, 
                            "park"
                        )
                        if nearest_park:
                            agent.set_destination(nearest_park.entrance, "going_to_park")
                    else:
                        agent.set_destination(self.city.get_random_position(), "wandering")

    def _send_agents_to_buildings(self, building_type: str):
        """Send all agents to the nearest building of specified type"""
        for agent in self.city.agents:
            nearest_building = self.city.get_nearest_building_of_type(
                agent.state.position, 
                building_type
            )
            if nearest_building:
                agent.set_destination(nearest_building.entrance, f"going_to_{building_type}")

    def _send_some_agents_to_buildings(self, building_type: str, proportion: float):
        """Send a proportion of agents to buildings of specified type"""
        import random
        agents_to_send = random.sample(
            self.city.agents, 
            int(len(self.city.agents) * proportion)
        )
        for agent in agents_to_send:
            nearest_building = self.city.get_nearest_building_of_type(
                agent.state.position, 
                building_type
            )
            if nearest_building:
                agent.set_destination(nearest_building.entrance, f"going_to_{building_type}")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    # Toggle debug mode
                    self.debug_mode = not self.debug_mode
                elif event.key == pygame.K_s:
                    # Toggle stats
                    self.show_stats = not self.show_stats
                elif event.key == pygame.K_SPACE:
                    # Toggle time speed (normal/fast)
                    self.time_system.time.time_scale = (
                        180.0 if self.time_system.time.time_scale == 60.0 else 60.0
                    )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # On click, make the nearest agent move to the clicked position
                clicked_pos = event.pos
                nearest_agent = min(
                    self.city.agents,
                    key=lambda a: (
                        (a.state.position[0] - clicked_pos[0])**2 + 
                        (a.state.position[1] - clicked_pos[1])**2
                    )
                )
                nearest_agent.set_destination(clicked_pos)

    def update(self):
        # Update time system
        self.time_system.update(1/self.config.fps)
        
        # Update city with delta time in hours
        self.city.update(
            1/self.config.fps * (self.time_system.time.time_scale/3600),
            self.time_system.time.time_of_day
        )

    def render(self):
        # Set background color based on time of day
        bg_color = self._get_background_color()
        self.screen.fill(bg_color)
        
        # Render city and all its contents
        self.city.render(self.screen)
        
        # Render UI elements
        self._render_ui()
        
        pygame.display.flip()

    def _get_background_color(self) -> tuple:
        """Get background color based on time of day"""
        progress = self.time_system.get_day_progress()
        
        if self.time_system.time.is_night:
            return (20, 20, 40)  # Dark blue-gray
        
        # Transition colors for different times of day
        if self.time_system.time.time_of_day == "morning":
            return (135, 206, 235)  # Light blue
        elif self.time_system.time.time_of_day == "afternoon":
            return (155, 226, 255)  # Brighter blue
        elif self.time_system.time.time_of_day == "evening":
            return (255, 190, 150)  # Orange-ish
        
        return (135, 206, 235)  # Default sky blue

    def _render_ui(self):
        """Render all UI elements"""
        # Always show time
        self.time_system.render(self.screen)
        
        # Show speed indicator
        speed_text = f"Speed: {self.time_system.time.time_scale/60.0}x"
        speed_surface = self.font.render(speed_text, True, (0, 0, 0))
        self.screen.blit(speed_surface, (self.config.width - 100, 10))

        if self.show_stats:
            self._render_stats()
        
        if self.debug_mode:
            self._render_debug_info()

    def _render_stats(self):
        """Render city statistics"""
        y_offset = 50
        
        # Building stats
        stats = self.city.get_building_stats()
        title_surface = self.title_font.render("City Statistics:", True, (0, 0, 0))
        self.screen.blit(title_surface, (self.config.width - 200, y_offset))
        
        y_offset += 40
        for building_type, count in stats.items():
            text = f"{building_type}: {count}"
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (self.config.width - 180, y_offset))
            y_offset += 25

    def _render_debug_info(self):
        """Render debug information for agents"""
        y_offset = 50
        for agent in self.city.agents:
            status = agent.get_status()
            
            # Render agent name and current action
            text = f"{status['name']}: {status['action']}"
            text_surface = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(text_surface, (10, y_offset))
            
            # Render needs
            needs_text = f"Needs: " + ", ".join(
                f"{need}:{value:.1f}" for need, value in status['needs'].items()
            )
            needs_surface = self.font.render(needs_text, True, (0, 0, 0))
            self.screen.blit(needs_surface, (10, y_offset + 20))
            
            y_offset += 50

def main():
    game = AgentCityGame()
    game.run()

if __name__ == "__main__":
    main()

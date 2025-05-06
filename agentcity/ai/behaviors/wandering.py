from random import random

from . import Behavior


class WanderingBehavior(Behavior):
    """A behavior where agents wander aimlessly when idle"""

    def __init__(self):
        super().__init__()
        self.min_wander_ticks = 120  # 2 seconds at 60 ticks/sec
        self.chance_to_wander = 0.1  # 10% chance to start wandering when idle
        self.base_priority = 10.0  # Low priority, only when nothing else to do

    def get_priority(self, agent) -> float:
        """Return base priority if should activate"""
        return self.base_priority if self.should_activate(agent) else 0.0

    def should_activate(self, agent) -> bool:
        """
        Activate wandering if:
        - Agent is idle
        - No urgent needs
        - Random chance hits
        """
        if agent.state.current_action != "idle":
            return False

        # Check if any needs are urgent
        for need in agent.needs.needs.values():
            if need.current < 50:
                return False

        # Random chance to start wandering
        return random() < self.chance_to_wander

    def update(self, agent) -> None:
        """Update wandering behavior"""
        if not self.state.active:
            # Start wandering
            self.state.active = True
            self.state.ticks_active = 0
            self.state.target_position = agent.city.get_random_position()
            agent.set_destination(self.state.target_position)
            agent.state.current_action = "wandering"
        else:
            self.state.ticks_active += 1

            # If we've reached destination or been wandering too long, stop
            if (
                not agent.state.destination
                or self.state.ticks_active > self.min_wander_ticks
            ):
                self.deactivate()
                agent.state.current_action = "idle"

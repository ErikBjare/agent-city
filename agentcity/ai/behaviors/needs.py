from . import Behavior


class NeedBehavior(Behavior):
    """Base class for need-driven behaviors"""

    def __init__(
        self,
        need_name: str,
        required_capability: str,
        threshold: float = 50.0,
        critical_threshold: float = 20.0,
    ):
        super().__init__()
        self.need_name = need_name
        self.required_capability = required_capability
        self.threshold = threshold
        self.critical_threshold = critical_threshold
        self.using_object = None

    def should_activate(self, agent) -> bool:
        """Activate when need drops below threshold"""
        need = agent.needs.needs.get(self.need_name)
        if not need:
            return False
        return need.current <= self.threshold

    def get_priority(self, agent) -> float:
        """Calculate priority based on need level"""
        need = agent.needs.needs[self.need_name]
        priority = 100.0 - need.current
        if need.current <= self.critical_threshold:
            priority += 50.0
        return priority

    def update(self, agent) -> None:
        """Find and use an object that provides the required capability"""
        if not self.state.active:
            # Start seeking
            self.state.active = True
            self.state.ticks_active = 0

            # Find a building with the required capability
            for building in agent.city.buildings:
                if self.required_capability in building.get_available_capabilities():
                    obj = building.find_object_with_capability(
                        self.required_capability, agent.name
                    )
                    if obj:
                        self.state.target_position = obj.position
                        agent.set_destination(building.entrance)
                        agent.state.current_action = f"seeking_{self.need_name}"
                        self.using_object = obj
                        obj.start_using(agent.name)
                        break

            if not self.using_object:
                self.deactivate()
        else:
            self.state.ticks_active += 1

            # If we've reached the entrance, move to the object
            if not agent.state.destination and self.using_object:
                if agent.state.current_action == f"seeking_{self.need_name}":
                    agent.set_destination(self.using_object.position)
                    agent.state.current_action = f"using_{self.need_name}"

            # Check if need is satisfied
            need = agent.needs.needs[self.need_name]
            if need.current >= 95.0:
                if self.using_object:
                    self.using_object.stop_using(agent.name)
                    self.using_object = None
                self.deactivate()
                agent.state.current_action = "idle"


class RestBehavior(NeedBehavior):
    """Behavior for satisfying energy needs"""

    def __init__(self):
        super().__init__(
            "energy", "resting_place", threshold=50.0, critical_threshold=20.0
        )


class EatBehavior(NeedBehavior):
    """Behavior for satisfying hunger needs"""

    def __init__(self):
        super().__init__(
            "hunger", "food_source", threshold=60.0, critical_threshold=30.0
        )


class SocializeBehavior(NeedBehavior):
    """Behavior for satisfying social needs"""

    def __init__(self):
        super().__init__(
            "social", "social_space", threshold=40.0, critical_threshold=20.0
        )

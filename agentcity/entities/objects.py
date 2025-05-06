from dataclasses import dataclass, field


@dataclass
class ObjectCapability:
    """A capability that an object provides"""

    name: str
    capacity: int = 1  # How many agents can use it at once
    satisfaction_rate: float = 0.0  # How quickly it satisfies needs


@dataclass
class WorldObject:
    """An object in the world that provides capabilities"""

    name: str
    position: tuple[float, float]
    capabilities: list[ObjectCapability]
    in_use_by: list[str] = field(
        default_factory=list
    )  # List of agent names currently using this object

    def __post_init__(self):
        self.in_use_by = self.in_use_by or []

    def can_use(self, agent_name: str) -> bool:
        """Check if the object can be used by another agent"""
        if agent_name in self.in_use_by:
            return True
        return len(self.in_use_by) < sum(cap.capacity for cap in self.capabilities)

    def start_using(self, agent_name: str) -> bool:
        """Start using the object"""
        if self.can_use(agent_name) and agent_name not in self.in_use_by:
            self.in_use_by.append(agent_name)
            return True
        return False

    def stop_using(self, agent_name: str) -> None:
        """Stop using the object"""
        if agent_name in self.in_use_by:
            self.in_use_by.remove(agent_name)


# Define common object types and their capabilities
OBJECT_TYPES = {
    "bed": [
        ObjectCapability(
            "resting_place", capacity=1, satisfaction_rate=20.0
        ),  # 20% energy per hour
    ],
    "kitchen": [
        ObjectCapability(
            "food_source", capacity=2, satisfaction_rate=40.0
        ),  # 40% hunger per hour
    ],
    "table": [
        ObjectCapability("food_source", capacity=4, satisfaction_rate=40.0),
        ObjectCapability("social_space", capacity=4, satisfaction_rate=15.0),
    ],
    "bench": [
        ObjectCapability("social_space", capacity=2, satisfaction_rate=15.0),
        ObjectCapability(
            "resting_place", capacity=2, satisfaction_rate=5.0
        ),  # Less effective than bed
    ],
    "trail": [
        ObjectCapability("social_space", capacity=10, satisfaction_rate=10.0),
    ],
}

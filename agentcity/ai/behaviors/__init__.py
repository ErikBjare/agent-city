from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BehaviorState:
    """State of a behavior, including whether it's active and for how long"""

    active: bool = False
    ticks_active: int = 0
    target_position: tuple[float, float] | None = None


class Behavior(ABC):
    """Base class for all behaviors"""

    def __init__(self):
        self.state = BehaviorState()

    @abstractmethod
    def should_activate(self, agent) -> bool:
        """Determine if this behavior should become active"""
        pass

    @abstractmethod
    def update(self, agent) -> None:
        """Update the behavior's state and affect the agent"""
        pass

    def deactivate(self) -> None:
        """Reset the behavior's state"""
        self.state = BehaviorState()

    @abstractmethod
    def get_priority(self, agent) -> float:
        """Get the priority of this behavior"""
        pass

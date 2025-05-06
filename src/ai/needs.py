from dataclasses import dataclass
from typing import Dict

@dataclass
class Need:
    current: float  # Current value (0-100)
    decay_rate: float  # How fast it decreases per hour
    critical_threshold: float = 20.0  # When this need becomes urgent
    
    def update(self, delta_time: float):
        """Update need value based on time passed (in hours)"""
        self.current = max(0.0, min(100.0, self.current - (self.decay_rate * delta_time)))

    @property
    def is_critical(self) -> bool:
        return self.current <= self.critical_threshold

class NeedsSystem:
    def __init__(self):
        self.needs: Dict[str, Need] = {
            "energy": Need(current=100.0, decay_rate=4.0),  # Depletes in ~24h
            "hunger": Need(current=100.0, decay_rate=8.0),  # Depletes in ~12h
            "social": Need(current=100.0, decay_rate=2.0),  # Depletes in ~48h
        }
    
    def update(self, delta_time: float):
        """Update all needs based on time passed"""
        for need in self.needs.values():
            need.update(delta_time)
    
    def get_most_urgent_need(self) -> str:
        """Returns the name of the most critical need"""
        return min(self.needs.items(), key=lambda x: x[1].current)[0]

    def satisfy_need(self, need_name: str, amount: float):
        """Satisfy a specific need by the given amount"""
        if need_name in self.needs:
            self.needs[need_name].current = min(100.0, self.needs[need_name].current + amount)

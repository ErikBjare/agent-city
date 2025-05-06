from dataclasses import dataclass


@dataclass
class Need:
    current: float  # Current value (0-100)
    decay_rate: float  # How fast it decreases per hour
    critical_threshold: float = 20.0  # When this need becomes urgent

    def update(self, delta_time: float):
        """Update need value based on time passed (in hours)"""
        self.current = max(
            0.0, min(100.0, self.current - (self.decay_rate * delta_time))
        )

    @property
    def is_critical(self) -> bool:
        return self.current <= self.critical_threshold


class NeedsSystem:
    def __init__(self):
        """Initialize needs system with per-hour decay rates

        Decay rates are percentage points per hour:
        - Energy: -5%/h (depletes in 20h)
        - Hunger: -10%/h (depletes in 10h)
        - Social: -3%/h (depletes in ~33h)

        These rates are balanced against building satisfaction rates:
        - House: +40%/h energy
        - Restaurant: +80%/h hunger
        - Park: +30%/h social
        """
        self.needs: dict[str, Need] = {
            "energy": Need(current=100.0, decay_rate=5.0),
            "hunger": Need(current=100.0, decay_rate=10.0),
            "social": Need(current=100.0, decay_rate=3.0),
        }

    def update(self, delta_time: float):
        """Update all needs based on time passed"""
        for _need_name, need in self.needs.items():
            need.update(delta_time)

    def get_most_urgent_need(self) -> str:
        """Returns the name of the most critical need"""
        return min(self.needs.items(), key=lambda x: x[1].current)[0]

    def satisfy_need(self, need_name: str, amount: float):
        """Satisfy a specific need by the given amount"""
        if need_name in self.needs:
            old_value = self.needs[need_name].current
            self.needs[need_name].current = min(100.0, old_value + amount)

from collections.abc import Callable
from dataclasses import dataclass

import pygame


@dataclass
class GameTime:
    hour: int = 0
    day: int = 1
    time_scale: float = 1.0  # 1.0 = 1 game hour per real second at 60 FPS

    @property
    def is_night(self) -> bool:
        return self.hour < 6 or self.hour >= 22

    @property
    def time_of_day(self) -> str:
        if 6 <= self.hour < 12:
            return "morning"
        elif 12 <= self.hour < 17:
            return "afternoon"
        elif 17 <= self.hour < 22:
            return "evening"
        else:
            return "night"


@dataclass
class ScheduledEvent:
    hour: int
    callback: Callable
    recurring: bool = True
    description: str = ""


class TimeSystem:
    def __init__(self):
        self.time = GameTime(
            hour=6,  # Start at 6 AM
            time_scale=0.2,  # 0.2 = 5 real seconds per game hour
        )
        self.events: list[ScheduledEvent] = []
        self.accumulated_time = 0.0
        self.ticks_per_hour = 60  # 60 ticks/hour = 1 tick per frame at 60 FPS
        self.current_tick = 0

        # Font for rendering time
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)

    def update(self, delta_time: float):
        """Update game time based on real time passed"""
        # Accumulate time
        self.accumulated_time += delta_time * self.time.time_scale

        # Calculate how many ticks should have passed
        time_per_tick = 1.0 / self.ticks_per_hour
        while self.accumulated_time >= time_per_tick:
            self.accumulated_time -= time_per_tick
            self._advance_tick()

    def _advance_tick(self):
        """Advance game by one tick"""
        self.current_tick += 1
        if self.current_tick >= self.ticks_per_hour:
            self.current_tick = 0
            self._advance_hour()

    def _advance_hour(self):
        """Advance time by one hour and handle events"""
        self.time.hour += 1
        if self.time.hour >= 24:
            self.time.hour = 0
            self.time.day += 1

        print(
            f"\nDay {self.time.day} - {self.time.hour:02d}:00 ({self.time.time_of_day})"
        )

        # Handle scheduled events
        self._process_events()

    def _process_events(self):
        """Process any events scheduled for the current hour"""
        for event in self.events:
            if event.hour == self.time.hour:
                event.callback()

    def schedule_event(self, event: ScheduledEvent):
        """Schedule a new event"""
        self.events.append(event)

    def render(self, screen: pygame.Surface):
        """Render current time"""
        time_str = (
            f"Day {self.time.day} - {self.time.hour:02d}:00 ({self.time.time_of_day})"
        )
        text_surface = self.font.render(time_str, True, (0, 0, 0))
        screen.blit(text_surface, (10, 10))

    def get_day_progress(self) -> float:
        """Return progress through the day as a float 0-1"""
        return (self.time.hour + self.accumulated_time) / 24.0

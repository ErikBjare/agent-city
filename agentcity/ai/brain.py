from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class Decision:
    action: str
    target_building_type: Optional[str] = None
    priority: float = 0.0
    
    def __repr__(self):
        return f"Decision({self.action}, building={self.target_building_type}, priority={self.priority:.2f})"

class AgentBrain:
    def __init__(self):
        # Map needs to building types that can satisfy them
        self.need_satisfaction_mapping = {
            "energy": ["house"],
            "hunger": ["restaurant"],
            "social": ["park", "restaurant"]
        }
        
        # Basic schedule preferences (hour -> preferred activities)
        self.schedule_preferences = {
            "morning": ["restaurant", "park"],
            "afternoon": ["park", "restaurant"],
            "evening": ["restaurant", "house"],
            "night": ["house"]
        }

    def make_decision(
        self,
        needs: Dict[str, float],
        current_action: str,
        time_of_day: str,
        available_buildings: List[str]
    ) -> Decision:
        """
        Make a decision based on current needs, time of day, and available options
        """
        decisions = []

        # Check critical needs first
        for need_name, need_value in needs.items():
            if need_value <= 20.0:  # Critical threshold
                for building_type in self.need_satisfaction_mapping.get(need_name, []):
                    if building_type in available_buildings:
                        decisions.append(Decision(
                            action=f"seeking_{need_name}",
                            target_building_type=building_type,
                            priority=100.0 - need_value  # Lower need = higher priority
                        ))

        # Consider time-based preferences if no critical needs
        if not decisions:
            preferred_buildings = self.schedule_preferences.get(time_of_day, [])
            for building_type in preferred_buildings:
                if building_type in available_buildings:
                    # Calculate priority based on time appropriateness
                    priority = 50.0 if building_type == preferred_buildings[0] else 30.0
                    decisions.append(Decision(
                        action=f"visiting_{building_type}",
                        target_building_type=building_type,
                        priority=priority
                    ))

        # If no other decisions, wander
        if not decisions:
            decisions.append(Decision(
                action="wandering",
                priority=10.0
            ))

        # Return the highest priority decision
        return max(decisions, key=lambda d: d.priority)

    def should_change_action(self, current_action: str, new_decision: Decision) -> bool:
        """Determine if the agent should change their current action"""
        # Always change if wandering
        if current_action == "wandering":
            return True
            
        # Don't interrupt critical actions unless new action is more critical
        if current_action.startswith("seeking_"):
            return new_decision.priority > 90.0
            
        # Otherwise, change if the new decision has higher priority
        return new_decision.priority >= 50.0

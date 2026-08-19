from pydantic import BaseModel, Field
from typing import Dict, Any, List

class LifeOSState(BaseModel):
    # Vitality Wing Indicating States
    calorie_target: int = Field(default=2000, description="Daily calorie burn threshold limit.")
    water_intake_ml: int = Field(default=0, description="Logged liquid consumption today.")
    health_alerts: List[str] = Field(default_factory=list, description="Critical wellness warning tracks.")
    
    # Intellect Wing Indicating States
    study_hours_today: float = Field(default=0.0, description="Focused academic target tracking hours.")
    career_skills: List[str] = Field(default_factory=list, description="Active target capability matrices.")
    
    # Resource Wing Indicating States
    weekly_budget: float = Field(default=5000.0, description="Financial transaction allowance scale.")
    current_weekly_spend: float = Field(default=0.0, description="Aggregated monetary outflows this week.")
    calendar_events: List[Dict[str, Any]] = Field(default_factory=list, description="Active schedule metrics.")
    
    # Environmental Indicating States
    domestic_chores: List[str] = Field(default_factory=list, description="Active household task cleanup loops.")

    # Utility method to compute remaining budget dynamically
    @property
    def remaining_budget(self) -> float:
        return self.weekly_budget - self.current_weekly_spend
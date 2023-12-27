from typing import Optional
from pydantic import BaseModel, validator
from sqlmodel import Relationship
from app.models.common import UserBase
from app.models.Facilities import Facility
from app.models.Users import Manager


class DashboardData(BaseModel):
    total_members: int
    total_revenue: float
    average_member_retention_rate: float

    @validator("total_revenue", "average_member_retention_rate")
    def must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("Value must be non-negative")
        return v

    @validator("average_member_retention_rate")
    def must_be_less_than_100(cls, v):
        if v > 100:
            raise ValueError("Value must be less than 100")
        return v


class Owner(UserBase, table=True):
    dashboard_data: Optional[DashboardData] = None
    facilities: list["Facility"] = Relationship(back_populates="owner")
    managers: Optional[list["Manager"]] = Relationship(back_populates="owner")

    # def calculate_roi(self, investment: float, current_value: float) -> float:
    #     if investment <= 0:
    #         raise ValueError("Investment must be greater than zero")
    #     roi = (current_value - investment) / investment
    #     return round(roi, 2)

    # def analyze_market_trends(self, market_data: dict) -> dict:
    #     # Placeholder for market trend analysis logic
    #     return market_data

    # def communicate_with_gym_managers(self, message: str, mode: str = "email") -> str:
    #     # Enhanced communication logic to include different modes (email, SMS, etc.)
    #     return f"Message sent to gym managers via {mode}: {message}"

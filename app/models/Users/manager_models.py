from typing import Optional
from pydantic import BaseModel, validator
from sqlmodel import Field, Relationship
from app.models.Users import Owner, Staff
from app.models.Facilities import Facility
from app.models.common import UserBase


class FinancialData(BaseModel):
    # Assuming a structured format, this can be modified as needed
    budget: float
    expenses: float

    @validator("budget", "expenses")
    def must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Financial values must be positive")
        return v


class Manager(UserBase, table=True):
    financial_data: Optional[FinancialData] = None
    facilities: list["Facility"] = Relationship(back_populates="manager")
    staff: list["Staff"] = Relationship(back_populates="manager")
    owner_id: int = Field(foreign_key="owner.id")
    owner: Owner = Relationship(back_populates="managers")

    # def manage_staff(self, staff_id: int, action: str) -> str:
    #     # Placeholder for staff management logic
    #     return f"Action {action} executed for staff ID {staff_id}"

    # def handle_finances(self, action: str, amount: float) -> str:
    #     # Placeholder for financial handling logic
    #     return f"Financial action {action} with amount {amount} executed"

    # def organize_community_event(self, event_details: dict) -> str:
    #     # Placeholder for event organization logic
    #     return f"Community event organized with details: {event_details}"

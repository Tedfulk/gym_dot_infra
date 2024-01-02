from typing import Optional, TYPE_CHECKING, List

from pydantic import validator, constr
from sqlmodel import Relationship, Field
from .common_models import Role
from datetime import datetime
import dns.resolver

if TYPE_CHECKING:
    from .manager_models import Manager, ManagerRead
    from .database import SQLModel

    # from ..Facilities import Facility


# class DashboardData(BaseModel):
#     total_members: int
#     total_revenue: float
#     average_member_retention_rate: float

#     @validator("total_revenue", "average_member_retention_rate")
#     def must_be_non_negative(cls, v):
#         if v < 0:
#             raise ValueError("Value must be non-negative")
#         return v

#     @validator("average_member_retention_rate")
#     def must_be_less_than_100(cls, v):
#         if v > 100:
#             raise ValueError("Value must be less than 100")
#         return v


class OwnerBase(SQLModel):
    name: constr(min_length=3, max_length=100)
    email: str
    role: Optional[Role] = None
    created_at: datetime = Field(default_factory=datetime.now)

    @validator("name")
    def validate_name(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name must only contain alphabetic characters")
        return v.title()

    @validator("email")
    def validate_email(cls, v):
        # Verify's that the email's domain has valid MX (Mail Exchange) records, indicating that it is capable of receiving emails.
        domain = v.split("@")[1]
        try:
            dns.resolver.resolve(domain, "MX")
        except dns.resolver.NoAnswer:
            raise ValueError("Email domain has no MX records")

        # TODO: Email verification logic should be handled by a separate service

        return v.lower()


class Owner(OwnerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # dashboard_data: Optional[DashboardData] = None
    # facilities: List["Facility"] = Relationship(back_populates="owner")
    managers: Optional[List["Manager"]] = Relationship(back_populates="owner")

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


class OwnerCreate(OwnerBase):
    pass


class OwnerRead(OwnerBase):
    id: int


class OwnerUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[Role] = None


# class OwnerReadWithFacilities(OwnerRead):
#     facilities: List[FacilityRead] = []


# class OwnerReadWithManagers(OwnerRead):
#     managers: List[ManagerRead] = []

# generate example json of a OwnerCretae object
# OwnerCreate(name='Test Owner', email='test@gmail.com', role='Owner')
# {id: 1, name: 'Test Owner', email: 'test@gmail', role: 'Owner'}

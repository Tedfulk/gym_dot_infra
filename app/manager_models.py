from typing import Optional, TYPE_CHECKING, List
from pydantic import field_validator, constr
from sqlmodel import Field, Relationship
from datetime import datetime
import dns.resolver
from .common_models import Role

if TYPE_CHECKING:
    from .owner_models import Owner, OwnerRead
    from .database import SQLModel

    # from .staff_models import Staff, StaffRead, Trainer, TrainerRead
    # from ..Facilities import Facility


# class FinancialData(SQLModel, table=True):
#     # Assuming a structured format, this can be modified as needed
#     budget: float
#     expenses: float

#     @validator("budget", "expenses")
#     def must_be_positive(cls, v):
#         if v < 0:
#             raise ValueError("Financial values must be positive")
#         return v


class ManagerBase(SQLModel):
    name: constr(min_length=3, max_length=100)
    email: str
    role: Optional[Role] = None
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator("name")
    def validate_name(cls, v):
        if not v.replace(" ", "").isalpha():
            raise ValueError("Name must only contain alphabetic characters")
        return v.title()

    @field_validator("email")
    def validate_email(cls, v):
        # Verify's that the email's domain has valid MX (Mail Exchange) records, indicating that it is capable of receiving emails.
        domain = v.split("@")[1]
        try:
            dns.resolver.resolve(domain, "MX")
        except dns.resolver.NoAnswer:
            raise ValueError("Email domain has no MX records")

        # TODO: Email verification logic should be handled by a separate service

        return v.lower()


class Manager(ManagerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # financial_data: Optional[FinancialData] = None
    # facilities: List["Facility"] = Relationship(back_populates="manager")
    # staff: List["Staff"] = Relationship(back_populates="manager")
    # trianers: List["Trainer"] = Relationship(back_populates="manager")

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


class ManagerCreate(ManagerBase):
    pass


class ManagerRead(ManagerBase):
    id: int


class ManagerUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    owner_id: Optional[int] = None


# class ManagerReadWithOwner(ManagerRead):
#     owner: OwnerRead

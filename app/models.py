from typing import List, Optional
from pydantic import constr, field_validator
from datetime import datetime
from enum import StrEnum
import dns.resolver

from sqlmodel import SQLModel, Field, Relationship


class Role(StrEnum):
    OWNER = "Owner"
    MANAGER = "Manager"
    TRAINER = "Trainer"
    STAFF = "Staff"
    MEMBER = "Member"
    GUEST = "Guest"
    VENDOR = "Vendor"


class OwnerBase(SQLModel):
    name: constr(min_length=3, max_length=100)
    email: str
    role: Optional[Role] = Field(default=Role.OWNER)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

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


class Owner(OwnerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # dashboard_data: Optional[DashboardData] = None
    facilities: List["Facility"] = Relationship(back_populates="owner")
    managers: List["Manager"] = Relationship(back_populates="owner")
    trainers: List["Trainer"] = Relationship(back_populates="owner")
    staff: List["Staff"] = Relationship(back_populates="owner")

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


class ManagerBase(SQLModel):
    name: constr(min_length=3, max_length=100)
    email: str
    role: Optional[Role] = Field(default=Role.MANAGER)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    owner_id: Optional[int] = Field(default=None, foreign_key="owner.id")

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
    facilities: List["Facility"] = Relationship(back_populates="manager")
    staff: List["Staff"] = Relationship(back_populates="manager")
    trainers: List["Trainer"] = Relationship(back_populates="manager")

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


class ManagerRead(ManagerBase):
    id: int


class ManagerCreate(ManagerBase):
    pass


class ManagerUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    owner_id: Optional[int] = None
    trainer_ids: Optional[List[int]] = None
    staff_ids: Optional[List[int]] = None


class FacilityBase(SQLModel):
    name: str
    street: str
    city: str
    state: str
    state_abbr: Optional[str]
    zip_code: str

    owner_id: int = Field(default=None, foreign_key="owner.id")
    manager_id: Optional[int] = Field(default=None, foreign_key="manager.id")

    @field_validator("zip_code")
    def must_be_valid_zip_code(cls, v):
        if not v.isnumeric() or len(v) != 5:
            raise ValueError("Zip code must be a 5-digit number")
        return v

    # @field_validator("state")
    # def must_be_valid_state(cls, v):
    #     if v not in cls.states.values():
    #         raise ValueError("Invalid state")
    #     return v

    # @field_validator("state_abbr")
    # def must_be_valid_state_abbr(cls, v):
    #     if v not in cls.states.keys():
    #         raise ValueError("Invalid state abbreviation")
    #     return v

    # @field_validator("state_abbr")
    # def set_state_abbr(cls, v, values):
    #     if "state" in values:
    #         return cls.states[values["state"]]
    #     return v

    # trainer_ids: Optional[List[int]] = Field(
    #     default_factory=List, foreign_key="trainer.id"
    # )
    # staff_ids: Optional[List[int]] = Field(default_factory=List, foreign_key="staff.id")


class Facility(FacilityBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    owner: Owner = Relationship(back_populates="facilities")
    manager: Optional[Manager] = Relationship(back_populates="facilities")

    trainers: List["Trainer"] = Relationship(back_populates="facility")
    staff: List["Staff"] = Relationship(back_populates="facility")


class FacilityCreate(FacilityBase):
    pass


class FacilityRead(FacilityBase):
    id: int


class FacilityUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    state_abbr: Optional[str] = None
    zip_code: Optional[str] = None
    owner_id: Optional[int] = None
    manager_id: Optional[int] = None


class TrainerBase(SQLModel):
    name: constr(min_length=3, max_length=100)
    email: Optional[str] = None
    bio: Optional[str] = None
    role: Optional[Role] = Field(default=Role.TRAINER)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    employment_date: Optional[datetime] = Field(default_factory=datetime.now)

    owner_id: Optional[int] = Field(default=None, foreign_key="owner.id")
    manager_id: Optional[int] = Field(default=None, foreign_key="manager.id")
    facility_id: Optional[int] = Field(default=None, foreign_key="facility.id")


class Trainer(TrainerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # appointments: List["TrainingAppointment"] = Relationship(back_populates="trainer")
    owner: Optional[Owner] = Relationship(back_populates="trainers")
    manager: Optional[Manager] = Relationship(back_populates="trainers")
    facility: Optional[Facility] = Relationship(back_populates="trainers")


class TrainerCreate(TrainerBase):
    pass


class TrainerRead(TrainerBase):
    id: int


class TrainerUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    role: Optional[str] = None
    owner_id: Optional[int] = None
    manager_id: Optional[int] = None
    facility_id: Optional[int] = None


# {
#     "name": "Trainer",
#     "email": "trainer@gmail.com",
#     "bio": "this is my life story",
#     "role": "Trainer",
#     "created_at": "2024-01-03T17:44:54.232Z",
#     "employment_date": "2024-01-03T17:44:54.232Z",
#     "owner_id": 1,
#     "manager_id": 2,
#     "facility_id": 1,
# }

# class TrainingAppointmentBase(SQLModel):
#     trainer_id: int = Field(foreign_key="trainer.id")
#     appointment_time: datetime


# class TrainingAppointment(TrainingAppointmentBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     # member_id: int = Field(foreign_key="member.id")
#     trainer: Trainer = Relationship(back_populates="appointments")


# class TrainingAppointmentRead(TrainingAppointmentBase):
#     id: int


# class TrainingAppointmentCreate(TrainingAppointmentBase):
#     pass


# class TrainingAppointmentUpdate(SQLModel):
#     id: Optional[int] = None
#     trainer_id: Optional[int] = None
#     appointment_time: Optional[datetime] = None


class StaffBase(SQLModel):
    name: constr(min_length=3, max_length=100)
    email: str
    bio: Optional[str] = None
    role: Optional[Role] = Field(default=Role.STAFF)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    owner_id: Optional[int] = Field(default=None, foreign_key="owner.id")
    manager_id: Optional[int] = Field(default=None, foreign_key="manager.id")
    facility_id: int = Field(default=None, foreign_key="facility.id")


class Staff(StaffBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    employment_date: datetime = Field(default_factory=datetime.now)

    owner: Owner = Relationship(back_populates="staff")
    manager: Manager = Relationship(back_populates="staff")
    facility: Facility = Relationship(back_populates="staff")


class StaffRead(StaffBase):
    id: int


class StaffCreate(StaffBase):
    pass


class StaffUpdate(SQLModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    owner_id: Optional[int] = None
    manager_id: Optional[int] = None
    facility_id: Optional[int] = None


class ManagerReadWithOwner(ManagerRead):
    owner: Optional[OwnerRead] = None


class OwnerReadWithManagers(OwnerRead):
    managers: List[ManagerRead] = []


class FacilityReadWithStaffAndTrainers(FacilityRead):
    trainers: List[TrainerRead] = []
    staff: List[StaffRead] = []


class FacilityReadWithOwner(FacilityRead):
    owner: OwnerRead


class FacilityReadWithManager(FacilityRead):
    manager: Optional[ManagerRead] = None


class TrainerReadWithOwner(TrainerRead):
    owner: OwnerRead


class TrainerReadWithManager(TrainerRead):
    manager: ManagerRead


class TrainerReadWithFacility(TrainerRead):
    facility: FacilityRead


class StaffReadWithOwner(StaffRead):
    owner: OwnerRead


class StaffReadWithManager(StaffRead):
    manager: ManagerRead


class StaffReadWithFacility(StaffRead):
    facility: FacilityRead

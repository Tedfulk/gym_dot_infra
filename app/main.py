from typing import List, Optional
from contextlib import asynccontextmanager
import httpx
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from pydantic import constr, field_validator
from datetime import datetime
from enum import StrEnum
import dns.resolver

from sqlmodel import Session, select, SQLModel, create_engine, Field, Relationship


states = {
    "AK": "ALASKA",
    "AL": "ALABAMA",
    "AR": "ARKANSAS",
    "AZ": "ARIZONA",
    "CA": "CALIFORNIA",
    "CO": "COLORADO",
    "CT": "CONNECTICUT",
    "DC": "DISTRICT OF COLUMBIA",
    "DE": "DELAWARE",
    "FL": "FLORIDA",
    "GA": "GEORGIA",
    "HI": "HAWAII",
    "IA": "IOWA",
    "ID": "IDAHO",
    "IL": "ILLINOIS",
    "IN": "INDIANA",
    "KS": "KANSAS",
    "KY": "KENTUCKY",
    "LA": "LOUISIANA",
    "MA": "MASSACHUSETTS",
    "MD": "MARYLAND",
    "ME": "MAINE",
    "MI": "MICHIGAN",
    "MN": "MINNESOTA",
    "MO": "MISSOURI",
    "MS": "MISSISSIPPI",
    "MT": "MONTANA",
    "NC": "NORTH CAROLINA",
    "ND": "NORTH DAKOTA",
    "NE": "NEBRASKA",
    "NH": "NEW HAMPSHIRE",
    "NJ": "NEW JERSEY",
    "NM": "NEW MEXICO",
    "NV": "NEVADA",
    "NY": "NEW YORK",
    "OH": "OHIO",
    "OK": "OKLAHOMA",
    "OR": "OREGON",
    "PA": "PENNSYLVANIA",
    "RI": "RHODE ISLAND",
    "SC": "SOUTH CAROLINA",
    "SD": "SOUTH DAKOTA",
    "TN": "TENNESSEE",
    "TX": "TEXAS",
    "UT": "UTAH",
    "VA": "VIRGINIA",
    "VT": "VERMONT",
    "WA": "WASHINGTON",
    "WI": "WISCONSIN",
    "WV": "WEST VIRGINIA",
    "WY": "WYOMING",
}


class Address(SQLModel):
    street: str
    city: str
    state: str
    state_abbr: Optional[str]
    zip_code: str

    @field_validator("zip_code")
    def must_be_valid_zip_code(cls, v):
        if not v.isnumeric() or len(v) != 5:
            raise ValueError("Zip code must be a 5-digit number")
        return v

    @field_validator("state")
    def must_be_valid_state(cls, v):
        if v not in cls.states.values():
            raise ValueError("Invalid state")
        return v

    @field_validator("state_abbr")
    def must_be_valid_state_abbr(cls, v):
        if v not in cls.states.keys():
            raise ValueError("Invalid state abbreviation")
        return v

    @field_validator("state_abbr")
    def set_state_abbr(cls, v, values):
        if "state" in values:
            return cls.states[values["state"]]
        return v


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
    role: Optional[Role] = None
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
    # facilities: List["Facility"] = Relationship(back_populates="owner")
    managers: List["Manager"] = Relationship(back_populates="owner")

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
    role: Optional[Role] = None
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
    # facilities: List["Facility"] = Relationship(back_populates="manager")
    # staff: List["Staff"] = Relationship(back_populates="manager")
    # trianers: List["Trainer"] = Relationship(back_populates="manager")

    owner: Optional[Owner] = Relationship(back_populates="managers")

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


class ManagerReadWithOwner(ManagerRead):
    owner: Optional[OwnerRead] = None


class OwnerReadWithManagers(OwnerRead):
    managers: List[ManagerRead] = []


# DB_FILE = "gym_dot_infra_dev_db.sqlite3"
# connect_args = {"check_same_thread": False}
# engine = create_engine(f"sqlite:///{DB_FILE}", echo=True, connect_args=connect_args)


# def create_tables():
#     """Create the tables registered with SQLModel.metadata (i.e classes with table=True).
#     More info: https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata
#     """
#     SQLModel.metadata.create_all(engine)
from .database import engine, create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(app=app) as client:
        print("client created")
        create_tables()
        yield {"client": client}
        print("client closed")


app = FastAPI(lifespan=lifespan)


def get_session():
    with Session(engine) as session:
        yield session


@app.post("/managers/", response_model=ManagerRead)
def create_manager(*, session: Session = Depends(get_session), manager: ManagerCreate):
    db_manager = Manager.model_validate(manager)
    session.add(db_manager)
    session.commit()
    session.refresh(db_manager)
    return db_manager


@app.get("/managers/{manager_id}", response_model=ManagerReadWithOwner)
def get_manager(*, session: Session = Depends(get_session), manager_id: int):
    manager = session.get(Manager, manager_id)
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    return manager


@app.get("/managers/", response_model=List[ManagerRead])
def read_managers(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    managers = session.exec(select(Manager).offset(offset).limit(limit)).all()
    return managers


@app.patch("/managers/{manager_id}", response_model=ManagerRead)
def update_manager(
    *,
    session: Session = Depends(get_session),
    manager_id: int,
    manager_update: ManagerUpdate,
):
    manager = session.get(Manager, manager_id)
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    manager_data = manager_update.dict(exclude_unset=True)
    for key, value in manager_data.items():
        setattr(manager, key, value)
    session.add(manager)
    session.commit()
    session.refresh(manager)
    return manager


@app.delete("/managers/{manager_id}", response_model=ManagerRead)
def delete_manager(*, session: Session = Depends(get_session), manager_id: int):
    manager = session.get(Manager, manager_id)
    if not manager:
        raise HTTPException(status_code=404, detail="Manager not found")
    session.delete(manager)
    session.commit()
    return manager


@app.post("/owners/", response_model=OwnerRead)
def create_owner(*, session: Session = Depends(get_session), owner: OwnerCreate):
    db_owner = Owner.model_validate(owner)
    session.add(db_owner)
    session.commit()
    session.refresh(db_owner)
    return db_owner


@app.get("/owners/{owner_id}", response_model=OwnerReadWithManagers)
def get_owner(*, session: Session = Depends(get_session), owner_id: int):
    owner = session.get(Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    return owner


@app.get("/owners/", response_model=List[OwnerRead])
def read_owners(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    owners = session.exec(select(Owner).offset(offset).limit(limit)).all()
    return owners


@app.patch("/owners/{owner_id}", response_model=OwnerRead)
def update_owner(
    *,
    session: Session = Depends(get_session),
    owner_id: int,
    owner_update: OwnerUpdate,
):
    owner = session.get(Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    owner_data = owner_update.model_dump(exclude_unset=True)
    for key, value in owner_data.items():
        setattr(owner, key, value)
    session.add(owner)
    session.commit()
    session.refresh(owner)
    return owner


@app.delete("/owners/{owner_id}", response_model=OwnerRead)
def delete_owner(*, session: Session = Depends(get_session), owner_id: int):
    owner = session.get(Owner, owner_id)
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")
    session.delete(owner)
    session.commit()
    return owner

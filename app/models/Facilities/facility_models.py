from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from app.models.Users import Manager, Trainer, Owner, Staff
from app.models.common import Address


class Facility(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    location: Address
    created_at: datetime = Field(default_factory=datetime.now)

    manager_id: Optional[int] = Field(default=None, foreign_key="manager.id")
    manager: Optional[Manager] = Relationship(back_populates="facilities")

    owner_id: int = Field(foreign_key="owner.id")
    owner: Owner = Relationship(back_populates="facility")

    trainers: list["Trainer"] = Relationship(back_populates="facility")
    staff: list["Staff"] = Relationship(back_populates="facility")

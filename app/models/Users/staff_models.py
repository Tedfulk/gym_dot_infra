from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from app.models.common import UserBase
from app.models.Users import Owner, Manager
from app.models.Facilities import Facility


class Trainer(UserBase, table=True):
    employment_date: datetime = Field(default_factory=datetime.now)
    bio: Optional[str]
    appointments: List["TrainingAppointment"] = Relationship(back_populates="trainer")
    owner_id: int = Field(foreign_key="owner.id")
    owner: Owner = Relationship(back_populates="trainers")
    manager_id: Optional[int] = Field(default=None, foreign_key="manager.id")
    facility_id: int = Field(foreign_key="facility.id")
    facility: Facility = Relationship(back_populates="trainers")


class TrainingAppointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    trainer_id: int = Field(foreign_key="trainer.id")
    trainer: Trainer = Relationship(back_populates="appointments")
    appointment_time: datetime


class Shift(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    staff_id: int = Field(foreign_key="staff.id")
    start_time: datetime
    end_time: datetime


class Staff(UserBase, table=True):
    employment_date: datetime = Field(default_factory=datetime.now)
    owner_id: int = Field(foreign_key="owner.id")
    owner: Owner = Relationship(back_populates="staff")
    manager_id: Optional[int] = Field(default=None, foreign_key="manager.id")
    shifts: List[Shift] = Relationship(back_populates="staff")
    facility_id: int = Field(foreign_key="facility.id")
    facility: Facility = Relationship(back_populates="staff")

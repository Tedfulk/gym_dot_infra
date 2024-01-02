# from typing import Optional, TYPE_CHECKING, List
# from sqlmodel import SQLModel, Field, Relationship
# from datetime import datetime
# from ..common import Address

# if TYPE_CHECKING:
#     from ..Users import Owner, Manager, Staff, Trainer


# class FacilityBase(SQLModel):
#     name: str
#     location: Address


# class Facility(FacilityBase, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     created_at: datetime = Field(default_factory=datetime.now)

#     manager_id: Optional[int] = Field(default=None, foreign_key="manager.id")
#     manager: Optional[Manager] = Relationship(back_populates="facilities")

#     owner_id: int = Field(foreign_key="owner.id")
#     owner: "Owner" = Relationship(back_populates="facilities")

#     trainers: List["Trainer"] = Relationship(back_populates="facility")
#     staff: List["Staff"] = Relationship(back_populates="facility")


# class FacilityCreate(FacilityBase):
#     pass


# class FacilityRead(FacilityBase):
#     id: int


# class FacilityUpdate(SQLModel):
#     id: Optional[int] = None
#     name: Optional[str] = None
#     location: Optional[Address] = None


# class FacilityReadWithStaffAndTrainers(FacilityRead):
#     trainers: List[TrainerRead] = []
#     staff: List[StaffRead] = []


# class FacilityReadWithOwner(FacilityRead):
#     owner: OwnerRead


# class FacilityReadWithManager(FacilityRead):
#     manager: Optional[ManagerRead] = None

from contextlib import asynccontextmanager
from typing import List, Optional

import httpx
from fastapi import Depends, FastAPI, HTTPException, Query, Request
from sqlmodel import Session, select

from .database import create_tables, engine
from .models import (
    Manager,
    ManagerCreate,
    ManagerRead,
    ManagerReadWithOwner,
    ManagerUpdate,
    Owner,
    OwnerCreate,
    OwnerRead,
    OwnerReadWithManagers,
    OwnerUpdate,
    FacilityRead,
    FacilityReadWithOwner,
    FacilityReadWithManager,
    FacilityReadWithStaffAndTrainers,
    FacilityUpdate,
    FacilityCreate,
    Facility,
    TrainerRead,
    TrainerReadWithOwner,
    TrainerReadWithManager,
    TrainerReadWithFacility,
    TrainerUpdate,
    TrainerCreate,
    Trainer,
    StaffRead,
    StaffReadWithOwner,
    StaffReadWithManager,
    StaffReadWithFacility,
    StaffUpdate,
    StaffCreate,
    Staff,
)


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
def get_managers(
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
def get_owners(
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


@app.post("/facilities/", response_model=FacilityRead)
def create_facility(
    *, session: Session = Depends(get_session), facility: FacilityCreate
):
    db_facility = Facility.model_validate(facility)
    session.add(db_facility)
    session.commit()
    session.refresh(db_facility)
    return db_facility


@app.get("/facilities/", response_model=List[FacilityRead])
def get_facilities(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    facilities = session.exec(select(Facility).offset(offset).limit(limit)).all()
    return facilities


@app.get("/facilities/{facility_id}/owner/", response_model=FacilityReadWithOwner)
def get_facility(*, session: Session = Depends(get_session), facility_id: int):
    facility = session.get(Facility, facility_id)
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    return facility


@app.get("/facilities/{facility_id}/manager/", response_model=FacilityReadWithManager)
def get_facility_with_manager(
    *, session: Session = Depends(get_session), facility_id: int
):
    facility = session.get(Facility, facility_id)
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    return facility


@app.get(
    "/facilities/{facility_id}/staff/trainers/",
    response_model=FacilityReadWithStaffAndTrainers,
)
def get_facility_with_staff_and_trainers(
    *, session: Session = Depends(get_session), facility_id: int
):
    facility = session.get(Facility, facility_id)
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    return facility


@app.patch("/facilities/{facility_id}", response_model=FacilityRead)
def update_facility(
    *,
    session: Session = Depends(get_session),
    facility_id: int,
    facility_update: FacilityUpdate,
):
    facility = session.get(Facility, facility_id)
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    facility_data = facility_update.dict(exclude_unset=True)
    for key, value in facility_data.items():
        setattr(facility, key, value)
    session.add(facility)
    session.commit()
    session.refresh(facility)
    return facility


@app.delete("/facilities/{facility_id}", response_model=FacilityRead)
def delete_facility(*, session: Session = Depends(get_session), facility_id: int):
    facility = session.get(Facility, facility_id)
    if not facility:
        raise HTTPException(status_code=404, detail="Facility not found")
    session.delete(facility)
    session.commit()
    return facility


@app.post("/trainers/", response_model=TrainerRead)
def create_trainer(*, session: Session = Depends(get_session), trainer: TrainerCreate):
    db_trainer = Trainer.model_validate(trainer)
    session.add(db_trainer)
    session.commit()
    session.refresh(db_trainer)
    return db_trainer


@app.get("/trainers/", response_model=List[TrainerRead])
def get_trainers(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    trainers = session.exec(select(Trainer).offset(offset).limit(limit)).all()
    return trainers


@app.get("/trainers/{trainer_id}/owner/", response_model=TrainerReadWithOwner)
def get_trainer_with_owner(*, session: Session = Depends(get_session), trainer_id: int):
    trainer = session.get(Trainer, trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return trainer


@app.get("/trainers/{trainer_id}/manager/", response_model=TrainerReadWithManager)
def get_trainer_with_manager(
    *, session: Session = Depends(get_session), trainer_id: int
):
    trainer = session.get(Trainer, trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return trainer


@app.get("/trainers/{trainer_id}/facility/", response_model=TrainerReadWithFacility)
def get_trainer_with_facility(
    *, session: Session = Depends(get_session), trainer_id: int
):
    trainer = session.get(Trainer, trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    return trainer


@app.patch("/trainers/{trainer_id}", response_model=TrainerRead)
def update_trainer(
    *,
    session: Session = Depends(get_session),
    trainer_id: int,
    trainer_update: TrainerUpdate,
):
    trainer = session.get(Trainer, trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    trainer_data = trainer_update.dict(exclude_unset=True)
    for key, value in trainer_data.items():
        setattr(trainer, key, value)
    session.add(trainer)
    session.commit()
    session.refresh(trainer)
    return trainer


@app.delete("/trainers/{trainer_id}", response_model=TrainerRead)
def delete_trainer(*, session: Session = Depends(get_session), trainer_id: int):
    trainer = session.get(Trainer, trainer_id)
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")
    session.delete(trainer)
    session.commit()
    return trainer


@app.post("/staff/", response_model=StaffRead)
def create_staff(*, session: Session = Depends(get_session), staff: StaffCreate):
    db_staff = Staff.model_validate(staff)
    session.add(db_staff)
    session.commit()
    session.refresh(db_staff)
    return db_staff


@app.get("/staff/", response_model=List[StaffRead])
def read_staff(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
):
    staff = session.exec(select(Staff).offset(offset).limit(limit)).all()
    return staff


@app.get("/staff/{staff_id}/owner/", response_model=StaffReadWithOwner)
def get_staff_with_owner(*, session: Session = Depends(get_session), staff_id: int):
    staff = session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff


@app.get("/staff/{staff_id}/manager/", response_model=StaffReadWithManager)
def get_staff_with_manager(*, session: Session = Depends(get_session), staff_id: int):
    staff = session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff


@app.get("/staff/{staff_id}/facility/", response_model=StaffReadWithFacility)
def get_staff_with_facility(*, session: Session = Depends(get_session), staff_id: int):
    staff = session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    return staff


@app.patch("/staff/{staff_id}", response_model=StaffRead)
def update_staff(
    *,
    session: Session = Depends(get_session),
    staff_id: int,
    staff_update: StaffUpdate,
):
    staff = session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    staff_data = staff_update.dict(exclude_unset=True)
    for key, value in staff_data.items():
        setattr(staff, key, value)
    session.add(staff)
    session.commit()
    session.refresh(staff)
    return staff


@app.delete("/staff/{staff_id}", response_model=StaffRead)
def delete_staff(*, session: Session = Depends(get_session), staff_id: int):
    staff = session.get(Staff, staff_id)
    if not staff:
        raise HTTPException(status_code=404, detail="Staff not found")
    session.delete(staff)
    session.commit()
    return staff

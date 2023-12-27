from sqlmodel import Session, create_engine
from app.models.Users import Owner
from typing import Optional


class OwnerRepo:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)

    def create_owner(self, owner: Owner):
        with Session(self.engine) as session:
            session.add(owner)
            session.commit()
            session.refresh(owner)
            return owner

    def read_owner(self, owner_id: int):
        with Session(self.engine) as session:
            owner = session.get(Owner, owner_id)
            return owner

    def update_owner(self, owner: Owner):
        with Session(self.engine) as session:
            session.merge(owner)
            session.commit()
            return owner

    def delete_owner(self, owner_id: int):
        with Session(self.engine) as session:
            owner = session.get(Owner, owner_id)
            if owner:
                session.delete(owner)
                session.commit()
            return owner

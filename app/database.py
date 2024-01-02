from sqlmodel import SQLModel, create_engine

DB_FILE = "db.sqlite3"
connect_args = {"check_same_thread": False}
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True, connect_args=connect_args)


def create_tables():
    """Create the tables registered with SQLModel.metadata (i.e classes with table=True).
    More info: https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata
    """
    SQLModel.metadata.create_all(engine)

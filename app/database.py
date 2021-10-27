from sqlmodel import create_engine, SQLModel, Session
from .models import User
from .settings import DATABASE_URI

connect_args = {
    "check_same_thread": False
}


engine = create_engine(DATABASE_URI, echo=False, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


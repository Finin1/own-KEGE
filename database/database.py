from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, StudentAnswer, Student, Task  # noqa


engine = create_engine("sqlite:///database.sqlite3")
# /to_compile/database

def create_db() -> None:
    Base.metadata.create_all(engine)


def create_session() -> Session:
    Session = sessionmaker(engine)
    return Session()

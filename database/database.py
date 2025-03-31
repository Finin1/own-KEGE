from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base, Answer, Student


engine = create_engine("sqlite:///database/database.sqlite3")

def create_db() -> None:
    Base.metadata.create_all(engine)


def create_session() -> Session:
    Session = sessionmaker(engine)
    return Session()

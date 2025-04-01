from random import randint
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def random_code():
    min_ = 1000
    max_ = 9999
    rand = randint(min_, max_)

    return rand


class Base(DeclarativeBase):
    ...


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    code: Mapped[int] = mapped_column(unique=True, default=random_code)

    answers: Mapped[list["Answer"]] = relationship(back_populates="student")


class Answer(Base):
    __tablename__ = "answers"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    task_number: Mapped[int]
    task_type: Mapped[int] = mapped_column(nullable=True)
    answer: Mapped[str]

    student: Mapped["Student"] = relationship(back_populates="answers")

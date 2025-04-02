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
    done: Mapped[bool] = mapped_column(default=False)
    
    answers: Mapped[list["StudentAnswer"]] = relationship(back_populates="student")


class StudentAnswer(Base):
    __tablename__ = "students_answers"
    id: Mapped[int] = mapped_column(primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    student_answer: Mapped[str]

    task: Mapped["Task"] = relationship(back_populates="students_answers")
    student: Mapped["Student"] = relationship(back_populates="answers")


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    task_number: Mapped[int] = mapped_column(unique=True)
    task_type: Mapped[int] = mapped_column(nullable=True)
    task_answer: Mapped[str]

    students_answers: Mapped[list["StudentAnswer"]] = relationship(back_populates="task")

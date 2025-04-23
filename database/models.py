from random import randint
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship


def random_code():
    min_ = 1000
    max_ = 9999
    rand = randint(min_, max_)
    return rand


try:
    from sqlalchemy.orm import DeclarativeBase
    from sqlalchemy.orm import mapped_column


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
        files: Mapped[list["File"]] = relationship(back_populates="task")


    class File(Base):
        __tablename__ = "files"
        id: Mapped[int] = mapped_column(primary_key=True)
        file_name: Mapped[str]
        task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))

        task: Mapped["Task"] = relationship(back_populates="files")

except:
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String, Boolean

    Base = declarative_base()


    class Student(Base):
        __tablename__ = "students"
        id: Mapped[int] = Column(Integer, primary_key=True)
        name: Mapped[str] = Column(String)
        surname: Mapped[str] = Column(String)
        code: Mapped[int] = Column(Integer, unique=True, default=random_code)
        done: Mapped[bool] = Column(Boolean, default=False)

        answers = relationship("StudentAnswer", back_populates="student")


    class StudentAnswer(Base):
        __tablename__ = "students_answers"
        id: Mapped[int] = Column(Integer, primary_key=True)
        student_id: Mapped[int] = Column(Integer, ForeignKey("students.id"))
        task_id: Mapped[int] = Column(Integer, ForeignKey("tasks.id"))
        student_answer: Mapped[str] = Column(String)

        task: Mapped["Task"] = relationship("Task", back_populates="students_answers")
        student = relationship("Student", back_populates="answers")


    class Task(Base):
        __tablename__ = "tasks"
        id: Mapped[int] = Column(Integer, primary_key=True)
        task_number: Mapped[int] = Column(Integer, unique=True)
        task_type: Mapped[int] = Column(Integer, nullable=True)
        task_answer: Mapped[str] = Column(String)

        students_answers = relationship("StudentAnswer", back_populates="task")
        files = relationship("File", back_populates="task")


    class File(Base):
        __tablename__ = "files"
        id: Mapped[int] = Column(Integer, primary_key=True)
        file_name: Mapped[str] = Column(String)
        task_id: Mapped[int] = Column(Integer, ForeignKey("tasks.id"))

        task: Mapped["Task"] = relationship("Task", back_populates="files")

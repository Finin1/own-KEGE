from pathlib import Path
from openpyxl import load_workbook

from main import app
from word_parser import parse_document
from database import Student, create_session, create_db


def get_students_list(path_to_students_list: Path) -> None:
    students_workbook = load_workbook(path_to_students_list)
    workbook_sheet = students_workbook.active

    row_iterator = workbook_sheet.iter_rows()

    new_students: list[Student] = []
    for name_cell, surname_cell in row_iterator:
        name: str = name_cell.internal_value
        surname: str = surname_cell.internal_value
        student: Student = Student(name=name, surname=surname)
        new_students.append(student)

    with create_session() as session:
        try:
            for student in new_students:
                session.add(student)
            session.commit()
        except Exception as ex:
            print(ex)
            session.rollback()


if __name__ == "__main__":
    create_db()
    get_students_list(Path("students_list.xlsx"))
    # parse_document(Path("test.docx"))

    # app.run(host="localhost", port=80)
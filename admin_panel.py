import os
from pathlib import Path
from openpyxl import load_workbook, Workbook
from sqlalchemy import Select

from main import app
from word_parser import parse_Poliacov_document
from database import Student, Task, StudentAnswer, create_session, create_db


def parse_students_list(path_to_students_list: Path) -> bool:
    confirmation = input("Delete all old data? Y/N \n")
    if confirmation != "Y":
        exit(0)

    with create_session() as session:
        statement: Select = Select(Student)
        students = session.scalars(statement=statement).all()
        try:
            for student_to_remove in students:
                session.delete(student_to_remove)
            session.commit()
        except Exception as ex:
            print(ex)
            session.rollback()

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
        except Exception:
            session.rollback()
            return False

        workbook_with_codes = Workbook()
        active_sheet = workbook_with_codes.active
    
        for student in new_students:
            active_sheet.append([student.name, student.surname, student.code])
        
        workbook_with_codes.save("students_with_codes.xlsx")
    return True


def init_test(path_to_root: Path) -> None:
    create_db()
    
    path_to_excel = path_to_root / "students_list.xlsx"
    path_to_word = path_to_root / "test2.docx"
    while not parse_students_list(path_to_excel):
        pass
    parse_Poliacov_document(path_to_word)
    
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8080))
    app.run(host=host, port=port)


def get_results() -> None:
    conversion_scale = {0: 0, 1: 7, 2: 14, 3: 20, 4: 27,
                        5: 34, 6: 40, 7: 43, 8: 46, 9: 48, 
                        10: 51, 11: 54, 12: 56, 13: 59, 14: 62, 
                        15: 64, 16: 67, 17: 70, 18: 72, 19: 75, 
                        20: 78, 21: 80, 22: 83, 23: 85, 24: 88,
                        25: 90, 26: 93, 27: 95, 28: 98, 29: 100}
    result_workbook = Workbook()
    active_sheet = result_workbook.active
    with create_session() as db_session:
        students_statement: Select = Select(Student)
        students = db_session.scalars(students_statement).all()
        active_sheet.append(["Имя", "Фамилия"] 
                            + [num for num in range(1, 28)] 
                            + ["Первичные баллы", "Вторичные баллы"])
        for student in students:
            name = student.name
            surname = student.surname
            new_row = [name, surname]
            new_row.extend([0] * 27)
            total = 0
            answers = student.answers
            for answer in answers:
                task: Task = answer.task
                number: int = task.task_number
                correct_answer: str = task.task_answer
                student_answer: str = answer.student_answer
                if number == "26":  # Делать пустую ячейку "None"
                    splited_student_answer = student_answer.split()
                    splited_correct_answer = correct_answer.split()
                    new_row[number + 1] = 0
                    if splited_student_answer[0] == splited_correct_answer[0]:
                        new_row[number + 1] += 1
                        total += 1
                    if splited_student_answer[1] == splited_correct_answer[1]:
                        new_row[number + 1] += 1
                        total += 1
                elif number == "27":
                    splited_student_answer = student_answer.split("\n")
                    splited_correct_answer = correct_answer.split("\n")
                    new_row[number + 1] = 0
                    if splited_student_answer[0] == splited_correct_answer[0]:
                        new_row[number + 1] += 1
                        total += 1
                    if splited_student_answer[1] == splited_correct_answer[1]:
                        new_row[number + 1] += 1
                        total += 1
                else:
                    if student_answer == correct_answer:
                        new_row[number + 1] = 1
                        total += 1
                    else:
                        new_row[number + 1] = 0
            new_row.append(total)
            new_row.append(conversion_scale[total])
            active_sheet.append(new_row)
        result_workbook.save("results.xlsx")


if __name__ == "__main__":
    inp = input("Init or result?\n")
    if inp == "init":
        init_test(Path(""))
    elif inp == "result":
        get_results()

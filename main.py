from flask import Flask, render_template, session, request
from typing import NamedTuple, List, Union

try:
    from sqlalchemy import select as Select
except:
    from sqlalchemy import Select
from openpyxl import Workbook
import datetime
from database import create_db, create_session
from database import Student, StudentAnswer, Task as TaskModel


class Task(NamedTuple):
    num: int
    type: Union[str,tuple] = 'line'
    files: List[str] = []


app = Flask(__name__)
app.app_context()
app.config['SECRET_KEY'] = "0"
current_task_nums = [Task(1,'line',['baloon.gif','style.css']), Task(2), Task(3), Task(4), Task(5),
                     Task(6), Task(7), Task(8), Task(9), Task(10), Task(25, (2,12)), Task(27, (2,2),['baloon.gif','style.css'])]


@app.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')


@app.route('/task/', methods=["GET", "POST"])
def task():
    term = datetime.timedelta(0,0,0,0,55,3)
    print('time',term)
    # print('time',dir(term))
    caption = "ЕГЭ инфа [<Имя ученика>]"
    if request.method == 'GET':
        if 'code' in session:
            return render_template('task.html', tasks=current_task_nums,term=term,caption=caption)
        else:
            return render_template('error.html', title='Много хочешь, ВВЕДИ КОД')
    elif request.method == 'POST':
        try:
            with create_session() as db_session:
                current_code = int(request.form['code'])

                student_statement = Select(Student).where(Student.code == current_code)
                student = db_session.scalars(student_statement).one_or_none()

                if student is None:
                    return render_template("error.html", title="СВОЙ КОД ВВЕДИ")

                if student.done:
                    return render_template("error.html", title="Ты уже всё решил")
        except Exception:
            return render_template('error.html', title='Думаешь самый умный ?')
        if len(request.form['code']) == 0:
            return render_template('error.html', title='Код активации нужно ВВЕСТИ')
        session['code'] = request.form['code']
        return render_template('task.html', tasks=current_task_nums,term=term,caption=caption)


@app.route('/finish/', methods=["POST"])
def finish():
    if 'code' not in session:
        return render_template('error.html', title='Ты сломал систему, МОЛОДЕЦ')
    code = session['code']
    with create_session() as db_session:
        student_statement = Select(Student).where(Student.code == code)
        student = db_session.scalars(student_statement).one()
        try:
            request_items = request.form.items()
            for number, answer in request_items:
                if "answer" in number:
                    number = int(number.replace("answer", ""))
                else:
                    continue
                task_statement = Select(TaskModel).where(TaskModel.task_number == number)
                task = db_session.scalars(task_statement).one_or_none()

                if task is None:
                    return render_template("error.html", title="Чё-то многова-то номеров")

                new_student_answer = StudentAnswer(student_id=student.id,
                                                   task_id=task.id,
                                                   student_answer=answer)
                db_session.add(new_student_answer)
            student.done = True
            db_session.merge(student)
            db_session.commit()
        except Exception as ex:
            print(ex)
            db_session.rollback()
    session.pop('code')
    return render_template('finish.html')


@app.route("/result/", methods=["GET"])
def result():
    result_workbook = Workbook()
    active_sheet = result_workbook.active
    with create_session() as db_session:
        students_statement = Select(Student)
        students = db_session.scalars(students_statement).all()
        active_sheet.append(["Имя", "Фамилия"] + [str(num) for num in range(1, 28)] + ["Результат"])
        for student in students:
            name = student.name
            surname = student.surname
            new_row = [name, surname]
            new_row.extend([0] * 27)
            total = 0
            answers = student.answers
            for answer in answers:
                task = answer.task
                number = task.task_number
                correct_answer = task.task_answer
                student_answer = answer.student_answer
                if student_answer == correct_answer:
                    new_row[number + 1] = 1
                    total += 1
                else:
                    new_row[number + 1] = 0
            new_row.append(total)
            active_sheet.append(new_row)
        result_workbook.save("results.xlsx")
    return render_template("task1.html")


@app.route("/task/<num>")
def get_number(num: int):
    print(num)
    return render_template(f"task{num}.html")


if __name__ == '__main__':
    create_db()
    app.run(host='localhost', port=8080)  # , debug=True

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
                     Task(6), Task(7), Task(8), Task(9), Task(10), 
                     Task(11), Task(12), Task(13), Task(14), Task(15),
                     Task(16), Task(17), Task(18), Task(19), Task(20),
                     Task(25, files=['baloon.gif','style.css'])]
# (2,2),

@app.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')


@app.route('/task/', methods=["GET", "POST"])
def task():
    term = datetime.timedelta(minutes=55, hours=3)
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


@app.route("/task/<num>")
def get_number(num: int):
    print(num)
    return render_template(f"task{num}.html")


if __name__ == '__main__':
    create_db()
    app.run(host='localhost', port=8080)  # , debug=True

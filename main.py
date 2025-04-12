import datetime

from flask import Flask, render_template, session, request
from typing import NamedTuple, List, Union

try:
    from sqlalchemy import select as Select
except Exception:
    from sqlalchemy import Select

from database import create_db, create_session
from database import Student, StudentAnswer, Task as TaskModel


class Task(NamedTuple):
    num: int
    type: Union[str, tuple] = 'line'
    files: List[str] = []


app = Flask(__name__)
app.app_context()
app.config['SECRET_KEY'] = "0"
current_task_nums = [Task(1, (2, 2)), Task(2), Task(3, (3, 2)), Task(4), Task(5)]


@app.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')


@app.route('/task/', methods=["GET", "POST"])
def task():
    term = datetime.timedelta(minutes=55, hours=3)
    print('time', term)
    # print('time',dir(term))
    caption = "ЕГЭ инфа [<Имя ученика>]"
    if request.method == 'GET':
        if 'code' in session:
            return render_template('task.html', tasks=current_task_nums, term=term, caption=caption)
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
        return render_template('task.html', tasks=current_task_nums, term=term, caption=caption)


@app.route('/finish/', methods=["POST"])
def finish():
    if 'code' not in session:
        return render_template('error.html', title='Ты сломал систему, МОЛОДЕЦ')
    code = session['code']

    request_items = request.form.items()
    request_items = filter(lambda el: "answer" in el[0], request_items)
    request_items = [(el[0].replace("answer", ""), el[1]) for el in request_items]

    line_items = filter(lambda el: el[0].isdigit(), request_items)

    table_items = filter(lambda el: not el[0].isdigit(), request_items)
    table_items = map(lambda el: (tuple(el[0].split("x")), el[1]), table_items)

    all_answers = {}
    for number, answer in line_items:
        if answer == "":
            answer = "None"
        number = int(number)
        all_answers[number] = answer.strip().lower()
    
    table_answers = {}
    for answer_info, answer in table_items:
        number, column, row = map(int, answer_info)
        if number not in table_answers:
            number = int(number)
            table_answers[number] = {"data": [], "rows_count": 0, "columns_count": 0}
        current_number = table_answers[number]
        current_number["data"].append(answer)
        current_number["rows_count"] = max(current_number["rows_count"], row + 1)
        current_number["columns_count"] = max(current_number["columns_count"], column + 1)

    for number, table in table_answers.items():
        data = table["data"]
        columns_count = table["columns_count"]
        answer = ""
        element_pos = 1
        for element in data:
            if element_pos % columns_count == 0:
                space_symbol = "\n"
            else:
                space_symbol = " "
            element_pos += 1
            answer += f"{element.strip().lower()}{space_symbol}"
        all_answers[number] = answer.strip()

    with create_session() as db_session:
        student_statement = Select(Student).where(Student.code == code)
        student = db_session.scalars(student_statement).one()
        try:
            for number, answer in all_answers.items():
                task_statement = Select(TaskModel).where(TaskModel.task_number == number)
                task = db_session.scalars(task_statement).one_or_none()
                if task is None:
                    return render_template("error.html", title="Чё-то многова-то номеров")

                new_student_answer = StudentAnswer(student_id=student.id,
                                                   task_id=task.id,
                                                   student_answer=answer)
                
                db_session.add(new_student_answer)
                student.done = False  # ! CHANGE IN THE END
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

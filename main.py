from flask import Flask, render_template, session, redirect, request
from typing import NamedTuple, List

from sqlalchemy import Select
from database import create_db, create_session
from database import Student


class Task(NamedTuple):
    num: int
    answer_input_type: str = 'line'
    files: List[str] = []


app = Flask(__name__)
app.app_context()
app.config['SECRET_KEY'] = "0"
current_task_nums = [Task(1), Task(2), Task(3), Task(4), Task(5),
                     Task(6), Task(7), Task(8), Task(9), Task(10)]


@app.route('/', methods=["GET"])
def index():
    if request.method == "GET":
        return render_template('index.html')


@app.route('/task/', methods=["GET", "POST"])
def task():
    if request.method == 'GET':
        if 'code' in session:
            return render_template('task.html', tasks=current_task_nums)
        else:
            return render_template('error.html', title='Много хочешь, ВВЕДИ КОД')
    elif request.method == 'POST':
        try:
            with create_session() as db_session:
                statement = Select(Student.code)
                codes = db_session.scalars(statement=statement).all()
                # Возможно изменить
                if int(request.form['code']) not in codes:
                    print("bad")
                    return render_template("error.html", title="СВОЙ КОД ВВЕДИ")
        except Exception:
            return render_template('error.html', title='Думаешь самый умный ?')
        if len(request.form['code']) == 0:
            return render_template('error.html', title='Код активации нужно ВВЕСТИ')
        session['code'] = request.form['code']
        return render_template('task.html', tasks=current_task_nums)


@app.route('/finish/', methods=["POST"])
def finish():
    if 'code' not in session:
        return render_template('error.html', title='Ты сломал систему, МОЛОДЕЦ')
    print(session['code'])
    print(request.form)
    session.pop('code')
    return render_template('finish.html')


@app.route("/task/<num>")
def get_number(num: int):
    print(num)
    return render_template(f"task{num}.html")


if __name__ == '__main__':
    create_db()
    app.run(host='localhost', port=8080)  # , debug=True

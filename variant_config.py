from pathlib import Path
from tkinter import Toplevel, Frame, X, Y, LEFT, Listbox, BOTTOM, BOTH, END, \
    SINGLE, TOP, Text, SUNKEN, Label

try:
    from sqlalchemy import Select
except:
    from sqlalchemy import select as Select
from bs4 import BeautifulSoup
from gui import BG, FG, CustomButton
from tkinter.simpledialog import askstring
from typing import Union
import logging
from PIL import Image, ImageGrab, ImageTk
# import winsound
from tkinter.filedialog import askopenfilename
import os
from database import Task as DBTask, create_session


# TODO
class Task(Frame):
    def __init__(self, master, name: str, task_type: int, answer: Union[str, None] = None):
        super().__init__(master)
        self['bg'] = BG
        self.name = name
        self.type = int(task_type)
        icf_width = 30
        self.image = None
        self.p_image = None
        self.image_control_frame = Frame(self, bg=BG)
        self.image_control_frame.pack(side=LEFT, fill=Y, pady=10, padx=10)
        self.clipboard_button = CustomButton(self.image_control_frame, text='Взять из буфера обмена',
                                             command=self.get_image_from_clipboard, width=icf_width)
        self.clipboard_button.pack(side=TOP)
        self.open_image_button = CustomButton(self.image_control_frame, text='Открыть', command=self.open_image,
                                              width=icf_width)
        self.open_image_button.pack(side=TOP, pady=10)
        self.answer_field = Text(self.image_control_frame, height=12, width=icf_width)
        if answer:
            self.answer_field.insert(0.0, answer)
        self.answer_field.pack()
        self.files_control_frame = Frame(self.image_control_frame, bg=BG, height=30)
        self.files_control_frame.pack(side=TOP, fill=X, pady= 10)
        self.add_file_button = CustomButton(self.files_control_frame, text='Добавить', command=self.add_file)
        self.add_file_button.place(x=0, y=0, relwidth=0.5, relheight=1)
        self.add_file_button = CustomButton(self.files_control_frame, text='Убрать', command=self.remove_file)
        self.add_file_button.place(relx=0.5, y=0, relwidth=0.5, relheight=1)
        self.files_listbox = Listbox(self.image_control_frame, selectmode=SINGLE)
        self.files_listbox.pack(side=TOP, fill=X)
        self.image_preview = Label(self, text='', bg=BG, justify=LEFT)
        self.image_preview.pack(fill=BOTH, expand=1)

    def add_file(self):
        path = askopenfilename()
        if path:
            self.files_listbox.insert(END, path)
            # TODO copy file to static

    def remove_file(self):
        file_path = self.files_listbox.get(self.files_listbox.curselection())
        try:
            print('remove')
            # TODO removal from static
        except:
            pass

        self.files_listbox.delete(self.files_listbox.curselection())

    def update_image(self):
        self.p_image = ImageTk.PhotoImage(self.image)
        self.image_preview['image'] = self.p_image
        
        number = self.name
        
        path_to_save_file = Path("static", "img", f"{number}.png")
        self.image.save(path_to_save_file)

        with open(f"task{number}.html", encoding="utf-8") as html_file:
            soup = BeautifulSoup("<div></div>", "html.parser")
            img_tag = soup.new_tag("img", src=f"../static/img/{number}.png")
            soup.div.append(img_tag)
            html_file.write(str(soup))

    def open_image(self):
        path = askopenfilename()
        if path:
            self.image = Image.open(path)
            self.update_image()

    def get_image_from_clipboard(self):
        image = ImageGrab.grabclipboard()
        if isinstance(image, Image.Image):
            self.image = image
            self.update_image()
            print('LOL')
        # else:
        #     winsound.MessageBeep()

    def pack(self):
        super().pack(fill=BOTH, expand=1)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class VariantConfigForm(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self['bg'] = BG
        self.title("KEGE - Редактирование варианта")
        self.geometry('500x500')
        self.left_frame = Frame(self, bg=FG, width=200)
        self.left_frame.pack(fill=Y, side=LEFT)
        self.task_control_frame = Frame(self.left_frame, bg=BG)
        self.task_control_frame.pack(side=BOTTOM, fill=X)
        self.add_task_btn = CustomButton(self.task_control_frame, text='Добавить', command=self.add_task)
        self.add_task_btn.pack(fill=X)
        self.task_listbox = Listbox(self.left_frame, selectmode=SINGLE)
        self.task_listbox.pack(fill=BOTH, expand=1)
        self.right_frame = Frame(self, bg=BG)
        self.right_frame.pack(expand=1, fill=BOTH)
        self.task_listbox.bind('<<ListboxSelect>>', self.task_selected)
        self.last_selected = None
        self.task_dict = {}

        self.delete_task_button = CustomButton(self.task_control_frame, text='Удалить', command=self.delete_task,
                                               width=10)
        self.delete_task_button.pack(side=TOP, fill=X)

        with create_session() as session:
            tasks_statement = Select(DBTask)
            all_tasks = session.scalars(tasks_statement).all()
            for task in all_tasks:
                number = str(task.task_number)
                answer = task.task_answer
                task_type = task.task_type
                self.task_dict[number] = Task(self.right_frame, number, task_type, answer)
                self.task_listbox.insert(END, number)

    def task_selected(self, e):
        try:
            tasks = self.task_dict
            last = self.last_selected

            with create_session() as session:
                try:
                    task_stm = Select(DBTask).where(DBTask.task_number == int(last))
                    db_task = session.scalars(task_stm).one()
                    last_answer = tasks[last].answer_field.get(0.0, END).strip()
                    db_task.task_answer = last_answer
                    session.merge(db_task)
                    session.commit()
                except Exception as ex:
                    print(ex)
                    session.rollback()

            selected = self.task_listbox.get(self.task_listbox.curselection())
            if selected != self.last_selected:
                try:
                    tasks[self.last_selected].pack_forget()
                except:
                    pass
                tasks[selected].pack()
                self.last_selected = selected
        except:
            pass

    def add_task(self):
        task_name = askstring('KEGE',
                              "Введите индекс задания (непрерывная последовательность цифр")
        task_type = askstring('KEGE',
                              "Введите тип задания (число от 1 до 27)")
        if task_name and task_type:
            # print(self.task_listbox.get(0,END))
            f = True
            for task in self.task_listbox.get(0, END):
                if task == task_name:
                    f = False
                    break
            if f:
                self.task_listbox.insert(END, task_name)
                self.task_dict[task_name] = Task(self.right_frame, str(task_name), task_type)
                with create_session() as session:
                    try:
                        new_task = DBTask(task_number=task_name, task_type=task_type, task_answer="")
                        session.add(new_task)
                        session.commit()
                    except Exception as ex:
                        print(ex)
                        session.rollback()

    def delete_task(self):
        selected = self.task_listbox.get(self.task_listbox.curselection())
        selected_task = self.task_dict[selected]

        with create_session() as session:
            try:
                task_statement = Select(DBTask).where(DBTask.task_number == selected_task.name)
                task = session.scalars(task_statement).one_or_none()

                if task is None:
                    pass

                for answer in task.students_answers:
                    session.delete(answer)
                session.delete(task)
                session.commit()
            except Exception as ex:
                print(ex)
                session.rollback()

        selected_task.pack_forget()
        self.task_listbox.delete(self.task_listbox.curselection())
        del self.task_dict[selected]

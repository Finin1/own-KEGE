from tkinter import Tk, X, LEFT, NW, StringVar, Frame, TOP, BOTH, Radiobutton

try:
    from sqlalchemy import Select
except:
    from sqlalchemy import select as Select
from admin_panel import parse_students_list, init_test, get_score_results, POLIACOV_PARSE, IMAGES_PARSE, start_test
from gui import ConfirmButton, FolderSelect, BG, SCL, ECL, FG, FileSelect, CustomButton
import multiprocessing
from variant_config import VariantConfigForm
from database import create_session, create_db, Student, Task as DBTask


class Form(Tk):
    def __init__(self):
        super().__init__()
        self['bg'] = BG
        self.geometry('600x220')
        self.minsize(600, 220)
        # self.attributes("-toolwindow", True)
        self.title("KEGE")
        # self.wm_attributes("-topmost", True)
        self.folder_select = FolderSelect(self)
        self.folder_select.pack(fill=X, padx=10, pady=5)
        
        self.parse_method = StringVar(self, POLIACOV_PARSE)

        self.startup_buttons_frame = Frame(self, bg=BG)
        self.results_buttons_frame = Frame(self, bg=BG)

        self.start_button = ConfirmButton(self.startup_buttons_frame, text='Запустить',
                                                command=lambda: self.after(1, self.start_test),
                                                bg=SCL, font=12)        
        self.check_preparations_for_startup()

        self.stop_button = ConfirmButton(self.startup_buttons_frame, text='Остановить', command=self.stop_test,
                                         message="Остановить тестирование ?", bg=ECL, font=12, state='disabled')
        self.init_button = ConfirmButton(self.startup_buttons_frame, text='Загрузить список учеников',
                                         command=lambda: self.after(1, self.init_test),
                                         message="Предыдущие данные удаляться. Продолжить ?", font=12)
        self.get_res_button = CustomButton(self.results_buttons_frame, text='Получить результаты по баллам', command=self.get_score_results,
                                           font=12)
        
        self.start_button.pack(side=LEFT, anchor=NW, padx=10, pady=10)
        self.stop_button.pack(side=LEFT, anchor=NW, padx=0, pady=10)
        self.init_button.pack(side=LEFT, anchor=NW, padx=10, pady=10)
        self.startup_buttons_frame.pack(side=TOP, fill=X)
        
        self.get_res_button.pack(side=LEFT, anchor=NW, padx=10, pady=0)
        self.results_buttons_frame.pack(side=TOP, fill=X)
        
        self.flask_process: multiprocessing.Process = None

        self.parse_rbs_frame = Frame(self, bg=BG, padx=5)
        self.poliacov_rb = Radiobutton(self.parse_rbs_frame, text='Файл полякова', value=POLIACOV_PARSE,
                                       variable=self.parse_method, bg=BG, fg=FG, font=('Verdana', 10),
                                       activebackground=BG, activeforeground=FG, cursor='hand2')
        self.poliacov_rb.pack(side=LEFT)
        self.images_rb = Radiobutton(self.parse_rbs_frame, text='Произвольный вариант', value=IMAGES_PARSE,
                                     variable=self.parse_method, bg=BG, fg=FG, font=('Verdana', 10),
                                     activebackground=BG, activeforeground=FG, cursor='hand2')
        self.images_rb.pack(side=LEFT)
        self.parse_rbs_frame.pack(side=TOP, fill=X)

        self.poliacov_frame = Frame(self, bg=BG)
        self.poliacov_frame.pack(side=TOP, fill=X,padx=10)
        self.word_select = FileSelect(self.poliacov_frame)
        self.word_select.pack(fill=X)

        self.images_frame = Frame(self, bg=BG)
        # self.poliacov_frame.pack(side=TOP, fill=X)
        self.images_folder_select = FolderSelect(self.images_frame)
        self.images_folder_select.pack(fill=X)
        self.images_config = CustomButton(self.images_frame, text="Редактировать вариант",font=12, command=self.variant_config)
        self.images_config.pack(side=LEFT, pady=10)

        self.resizable(True, False)
        self.parse_method.trace('w',self.__parse_method_change)
        self.vc_form = None

    def variant_config(self):
        self.vc_form = VariantConfigForm(self)
        self.vc_form.grab_set()

    def __parse_method_change(self, a, b, c):
        meth = self.parse_method.get()
        if meth == POLIACOV_PARSE:
            self.geometry('600x220')
            try:
                self.poliacov_frame.pack_info()
            except:
                self.poliacov_frame.pack(side=TOP, fill=X,padx=10)
                self.images_frame.pack_forget()
        elif meth == IMAGES_PARSE:
            self.geometry('600x240')
            try:
                self.images_frame.pack_info()
            except:
                self.images_frame.pack(side=TOP, fill=X,padx=10)
                self.poliacov_frame.pack_forget()

        self.check_preparations_for_startup()

    def start_test(self):
        self.flask_process = multiprocessing.Process(target=start_test)
        self.flask_process.daemon = True
        self.flask_process.start()
        self.start_button.deactivate()
        self.stop_button.activate()

    def init_test(self):
        self.flask_process = multiprocessing.Process(target=init_test, args=(self.folder_select.get_path(),))
        self.flask_process.daemon = True
        self.flask_process.start()
        self.check_preparations_for_startup()

    def get_score_results(self):
        get_score_results()

    def stop_test(self):
        if self.flask_process:
            if self.flask_process.is_alive():
                self.flask_process.terminate()
                self.start_button.activate()
                self.stop_button.deactivate()

    def check_preparations_for_startup(self):
        with create_session() as session:
            students_statement = Select(Student)
            students = session.scalars(students_statement).all()
            
            tasks_statement = Select(DBTask)
            tasks = session.scalars(tasks_statement).all()
            
            meth = self.parse_method.get()
            
            if not students or (not tasks and meth == IMAGES_PARSE):
                self.start_button.deactivate()
            else:
                self.start_button.activate()


if __name__ == '__main__':
    create_db()
    form = Form()
    form.mainloop()

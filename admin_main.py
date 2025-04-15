from tkinter import Tk, X, LEFT, NW, StringVar, Frame, TOP, BOTH, Radiobutton
from admin_panel import parse_students_list, init_test, get_results, POLIACOV_PARSE, IMAGES_PARSE
from gui import ConfirmButton, FolderSelect, BG, SCL, ECL, FG, FileSelect, CustomButton
import multiprocessing
from variant_config import VariantConfigForm


class Form(Tk):
    def __init__(self):
        super().__init__()
        self['bg'] = BG
        self.geometry('400x185')
        self.minsize(400,185)
        # self.attributes("-toolwindow", True)
        self.title("KEGE")
        # self.wm_attributes("-topmost", True)
        self.folder_select = FolderSelect(self)
        self.folder_select.pack(fill=X, padx=10, pady=5)
        self.buttons_frame = Frame(self, bg=BG)
        self.init_button = ConfirmButton(self.buttons_frame, text='Запуск',
                                         command=lambda: self.after(1, self.init_test),
                                         message="Предыдущие данные удаляться. Продолжить ?", bg=SCL, font=12)
        self.stop_button = ConfirmButton(self.buttons_frame, text='Остановить', command=self.stop_test,
                                         message="Остановить тестирование ?", bg=ECL, font=12, state='disabled')
        self.get_res_button = CustomButton(self.buttons_frame, text='Получить результат', command=self.get_results,
                                            font=12)
        self.init_button.pack(side=LEFT, anchor=NW, padx=10, pady=10)
        self.stop_button.pack(side=LEFT, anchor=NW, padx=0, pady=10)
        self.get_res_button.pack(side=LEFT, anchor=NW, padx=10, pady=10)
        self.buttons_frame.pack(side=TOP, fill=X)
        self.flask_process: multiprocessing.Process = None
        self.parse_method = StringVar(self, POLIACOV_PARSE)
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
        self.images_config.pack(side=LEFT,pady=10)

        self.resizable(True, False)
        self.parse_method.trace('w',self.__parse_method_change)
        self.vc_form = None

    def variant_config(self):
        self.vc_form = VariantConfigForm(self)
        self.vc_form.grab_set()

    def __parse_method_change(self,a,b,c):
        meth = self.parse_method.get()
        if meth == POLIACOV_PARSE:
            try:
                self.poliacov_frame.pack_info()
            except:
                self.poliacov_frame.pack(side=TOP, fill=X,padx=10)
                self.images_frame.pack_forget()
        elif meth == IMAGES_PARSE:
            try:
                self.images_frame.pack_info()
            except:
                self.images_frame.pack(side=TOP, fill=X,padx=10)
                self.poliacov_frame.pack_forget()

    def init_test(self):
        self.flask_process = multiprocessing.Process(target=init_test, args=(self.folder_select.get_path(),))
        self.flask_process.daemon = True
        self.flask_process.start()
        self.init_button.deactivate()
        self.stop_button.activate()

    def get_results(self):
        get_results()

    def stop_test(self):
        if self.flask_process:
            if self.flask_process.is_alive():
                self.flask_process.terminate()
                self.init_button.activate()
                self.stop_button.deactivate()


if __name__ == '__main__':
    form = Form()
    form.mainloop()

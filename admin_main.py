from tkinter import Tk, X, LEFT, NW
from admin_panel import parse_students_list, init_test, get_results
from gui import ConfirmButton, FolderSelect, BG, SCL, ECL
import multiprocessing


class Form(Tk):
    def __init__(self):
        super().__init__()
        self['bg'] = BG
        self.geometry('400x95')
        self.attributes("-toolwindow", True)
        self.title("KEGE")
        self.wm_attributes("-topmost", True)
        self.init_button = ConfirmButton(self, text='Запуск', command=lambda : self.after(1,self.init_test),
                                         message="Предыдущие данные удаляться. Продолжить ?", bg=SCL, font=12)
        self.stop_button = ConfirmButton(self, text='Остановить', command=self.stop_test,
                                         message="Остановить тестирование ?", bg=ECL, font=12, state='disabled')
        self.get_res_button = ConfirmButton(self, text='Получить результат', command=self.get_results, font=12)
        self.folder_select = FolderSelect(self)
        self.folder_select.pack(fill=X, padx=10, pady=10)
        self.init_button.pack(side=LEFT, anchor=NW, padx=10, pady=10)
        self.stop_button.pack(side=LEFT, anchor=NW, padx=0, pady=10)
        self.get_res_button.pack(side=LEFT, anchor=NW, padx=10, pady=10)
        self.flask_process: multiprocessing.Process = None
        self.resizable(False, False)

    def init_test(self):
        self.flask_process = multiprocessing.Process(target= init_test,args=(self.folder_select.get_path(),))
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

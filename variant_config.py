from tkinter import Toplevel, Frame, X, Y, LEFT, Listbox, BOTTOM, BOTH, END, \
    SINGLE, TOP, Text, SUNKEN, Label
from gui import BG, FG, CustomButton
from tkinter.simpledialog import askstring
import logging
from PIL import Image, ImageGrab, ImageTk
import winsound
from tkinter.filedialog import askopenfilename


# TODO
class Task(Frame):
    def __init__(self, master, name: str):
        super().__init__(master)
        self['bg'] = BG
        self.name = name
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
        self.answer_field.pack(expand=1,fill=Y)
        self.image_preview = Label(self, text='',bg=BG,justify=LEFT)
        self.image_preview.pack(fill=BOTH, expand=1)

    def update_image(self):
        self.p_image = ImageTk.PhotoImage(self.image)
        self.image_preview['image']=self.p_image

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
        else:
            winsound.MessageBeep()

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
        self.task_dict = {}
        self.right_frame = Frame(self, bg=BG)
        self.right_frame.pack(expand=1, fill=BOTH)
        self.task_listbox.bind('<<ListboxSelect>>', self.task_selected)
        self.last_selected = None

    def task_selected(self, e):
        try:
            selected = self.task_listbox.get(self.task_listbox.curselection())
            if selected != self.last_selected:
                try:
                    self.task_dict[self.last_selected].pack_forget()
                except:
                    logging.exception('')
                self.task_dict[self.task_listbox.get(self.task_listbox.curselection())[0]].pack()
                self.last_selected = selected
        except:
            logging.exception('')

    def add_task(self):
        task_name = askstring('KEGE',
                              "Введите индекс задания (непрерывная последовательность цифр и/или английских символов)")
        if task_name:
            # print(self.task_listbox.get(0,END))
            f = True
            for task in self.task_listbox.get(0, END):
                if task == task_name:
                    f = False
                    break
            if f:
                self.task_listbox.insert(END, task_name)
                self.task_dict[task_name] = Task(self.right_frame, str(task_name))

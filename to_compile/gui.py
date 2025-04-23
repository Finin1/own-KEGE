from tkinter import Button, Frame, Label, RIGHT, BOTH, Y, SUNKEN, FLAT, SOLID, RIGHT, LEFT
from tkinter.messagebox import askyesno
from pathlib import Path
from tkinter.filedialog import askdirectory, askopenfilename

BG = '#fff'
FG = '#2599F2'
SCL = '#00E176'
ECL = '#f00'


class CustomButton(Button):
    def __init__(self, master, **kw):
        if 'font' in kw.keys() and type(kw['font']) == int:
            kw['font'] = ('Verdana', kw['font'])
        else:
            kw['font'] = ('Verdana', 10)
        if not 'bg' in kw.keys():
            kw['bg'] = FG
        kw['relief'] = FLAT
        self.bg = kw['bg']
        self.fg = BG
        kw['fg'] = BG
        kw['disabledforeground'] = self.bg

        kw['cursor'] = 'hand2'
        super().__init__(master, **kw)
        if 'state' in kw.keys() and kw['state'] == 'disabled':
            self.__enter()
        self.bind('<Enter>', self.__enter)
        self.bind('<Leave>', self.__leave)
        # self.bind('<Deactivate>', self.__deactivate)
        # self.bind('<Activate>', self.__activate)

    def __enter(self, e=None):
        if e is not None:
            if self['state'] == 'disabled': return
        self['fg'] = self.bg
        self['bg'] = self.fg

    def __leave(self, e=None):
        if e is not None:
            if self['state'] == 'disabled': return
        self['fg'] = self.fg
        self['bg'] = self.bg

    def deactivate(self, e=None):
        self['state'] = 'disabled'
        self.__enter()

    def activate(self, e=None):
        self['state'] = 'normal'
        self.__leave()


class ConfirmButton(CustomButton):
    def __init__(self, master, **kw):
        self.message = 'Совершаем действие ?'

        if 'command' in kw.keys():
            if 'message' in kw.keys():
                self.message = kw['message']
            self._command = kw['command']
            kw['command'] = lambda: self._command() if askyesno('Подтверждение', self.message) else None
        try:
            kw.pop('message')
        except:
            pass
        super().__init__(master, **kw)


class FolderSelect(Frame):
    ask_func = lambda e: askdirectory()

    def __init__(self, master, **kw):
        self.path: Path = Path('')
        if 'path' in kw:
            self.path = kw['path']

        super().__init__(master, **kw)

        self.label = Label(self, text=self.path.absolute(), borderwidth=1, fg=FG, bg=BG, justify=LEFT, anchor='w',
                           font="Verdana 8")
        self.button = CustomButton(self, text='Изменить', command=self.ask_directory, font=8)

    def get_path(self):
        return self.path

    def ask_directory(self):
        path = self.ask_func()
        if path:
            print(path)
            self.path = Path(path)
        self.label['text'] = self.path.absolute()

    def pack_own(self):
        self.button.pack(side=LEFT, fill=Y)
        self.label.pack(fill=BOTH, expand=1)

    def pack_own_forget(self):
        self.button.pack_forget()
        self.label.pack_forget()

    def pack(self, **kw):
        super().pack(**kw)
        self.pack_own()

    def place(self, **kw):
        super().pack(**kw)
        self.pack_own()

    def pack_forget(self):
        super().pack_forget()
        self.pack_own_forget()

    def place_forget(self):
        super().place_forget()
        self.pack_own_forget()


class FileSelect(FolderSelect):
    ask_func = lambda e: askopenfilename()

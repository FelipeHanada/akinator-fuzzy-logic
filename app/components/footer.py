import tkinter as tk

class Footer(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.text1 = tk.Label(
            self,
            text='Desenvolvido por',
            font=('Open Sans', 10),
            fg='#67AAE1',
            bg=self['bg']
        )
        self.text1.pack(side=tk.TOP, fill=tk.BOTH)

        self.names_frame = tk.Frame(self)
        self.name1 = tk.Label(
            self.names_frame,
            text='Breno de Carvalho',
            font=('Open Sans', 10),
            fg='#67AAE1',
            bg=self['bg']
        )
        self.name1.pack(side=tk.LEFT)
        self.name_and = tk.Label(
            self.names_frame,
            text=' & ',
            font=('Open Sans', 10),
            fg='white',
            bg=self['bg']
        )
        self.name_and.pack(side=tk.LEFT)
        self.name2 = tk.Label(
            self.names_frame,
            text='Felipe Hanada',
            font=('Open Sans', 10),
            fg='#67AAE1',
            bg=self['bg']
        )
        self.name2.pack(side=tk.RIGHT)

        self.names_frame.pack(side=tk.BOTTOM)

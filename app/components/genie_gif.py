import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle

class GenieGIF(tk.Label):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        self.parent_width = self.parent.winfo_width()
        self.parent_height = self.parent.winfo_height()

        super().__init__(self.parent, *args, **kwargs)

        self.load('app/assets/genie.gif')
        
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames[1:])

        print(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

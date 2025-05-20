from tkinter import *
from tkinter import ttk
from loging import Login
from loging import Registro
from container import Container
import sys
import os

class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Punto de venta")
        self.geometry("1100x650+120+20")
        self.resizable(False, False)

        container = Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.configure(bg="#95c799")

        self.frames = {}
        self.container_frame = None
        for i in (Login, Registro, Container):
            frame = i(container, self)
            self.frames[i] = frame
            if i == Container:
                self.container_frame = frame

        self.show_frame(Login)

        self.style = ttk.Style()
        self.style.theme_use("clam")

    def show_frame(self, frame_class, logged_user=None):
        frame = self.frames[frame_class]
        if frame_class == Container:
            frame.tkraise()
            if logged_user and self.container_frame:
                self.container_frame.set_logged_user(logged_user)
        else:
            frame.tkraise()

def main():
    app = Manager()
    app.mainloop()

if __name__ == "__main__":
    main()
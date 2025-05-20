import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from container import Container
from abstracs import AuthInterface

class Login(tk.Frame, AuthInterface):
    db_name = "database.db"
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.widgets()

    def validacion(self, user, pasword):
        return len(user) > 0 and len(pasword) > 0

    def login(self):
        user = self.username.get()
        pasword = self.paswordus.get()

        if self.validacion(user, pasword):
            consulta = "SELECT * FROM usuarios WHERE username = ? AND paswordus = ?"
            parametros = (user, pasword)

            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute(consulta, parametros)
                    result = cursor.fetchone()  # Usamos fetchone() porque esperamos un solo usuario

                    if result:
                        logged_user = result[1]  # El nombre de usuario está en la segunda columna (índice 1)
                        self.control1(logged_user) # Pasamos el nombre de usuario
                    else:
                        self.username.delete(0, 'end')
                        self.paswordus.delete(0, 'end')
                        messagebox.showerror(title="Error", message="Usuario y/o contraseña incorrectos")
            except sqlite3.Error as e:
                messagebox.showerror(title="Error", message="No se conecto a la base de datos {}".format(e))
        else:
            messagebox.showerror(title="Error", message="Llene todas las casillas")

    def control1(self, logged_user):
        self.controlador.show_frame(Container, logged_user=logged_user) # Pasamos el usuario al Container

    def control2(self):
        self.controlador.show_frame(Registro)

    def widgets(self):
        fondo = tk.Frame(self, bg="#95c799")
        fondo.pack()
        fondo.place(x=0, y=0, width=1100, height=650)

        self.bg_image = Image.open("imagenes/fondo.png")
        self.bg_image = self.bg_image.resize((1100,650))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ttk.Label(fondo, image=self.bg_image)
        self.bg_label.place(x=0, y=0, width=1100, height=650)

        frame1 = tk.Frame(self, bg="#FFFFFF", highlightbackground="black", highlightthickness=1)
        frame1.place(x=350, y=70, width=400, height=560)

        self.logo_image = Image.open("imagenes/logo.png")
        self.logo_image = self.logo_image.resize((200,200))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = ttk.Label(frame1, image=self.logo_image, background="#FFFFFF")
        self.logo_label.place(x=100, y=20)

        user = ttk.Label(frame1, text="Nombre de usuario:", font="arial 16 bold", background="#FFFFFF")
        user.place(x=100, y=250)
        self.username = ttk.Entry(frame1, font="arial 16 bold")
        self.username.place(x=80, y=290, width=240, height=40)

        pasword = ttk.Label(frame1, text="Contraseña:", font="arial 16 bold", background="#FFFFFF")
        pasword.place(x=100, y=340)
        self.paswordus = ttk.Entry(frame1, show="*", font="arial 16 bold")
        self.paswordus.place(x=80, y=380, width=240, height=40)

        btn1 = tk.Button(frame1, text="Iniciar sesion", font="arial 16 bold", command=self.login)
        btn1.place(x=80, y=440, width=240, height=40)

        btn2 = tk.Button(frame1, text="Registrar", font="arial 16 bold", command=self.control2)
        btn2.place(x=80, y=490, width=240, height=40)

class Registro(tk.Frame, AuthInterface):
    db_name = "database.db"
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.widgets()

    def validacion(self, user, pasword):
        return len(user) > 0 and len(pasword) > 0

    def eje_consulta(self, consulta, parametros=()):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(consulta, parametros)
                conn.commit
        except sqlite3.Error as e:
            messagebox.showerror(title="Error", message="Error al ejecutar la consulta: {}".format(e))

    def registro(self):
        user = self.username.get()
        pasword = self.paswordus.get()
        key = self.keyus.get()
        if self.validacion(user, pasword):
            if len(pasword) < 6:
                messagebox.showinfo(title="Error", message="Contraseña demasiado corta")
                self.username.delete(0, 'end')
                self.paswordus.delete(0, 'end')
            else:
                if key == "1234":
                    consulta = "INSERT INTO usuarios VALUES (?,?,?)"
                    parametros = (None, user, pasword)
                    self.eje_consulta(consulta, parametros)
                    self.control1()
                else:
                    messagebox.showerror(title="Registro", message="Error al ingresar el codigo de registro")
        else:
            messagebox.showerror(title="Error", message="Llene sus datos")

    def control1(self):
        self.controlador.show_frame(Container)

    def control2(self):
        self.controlador.show_frame(Login)

    def widgets(self):
        fondo = tk.Frame(self, bg="#95c799")
        fondo.pack()
        fondo.place(x=0, y=0, width=1100, height=650)

        self.bg_image = Image.open("imagenes/fondo.png")
        self.bg_image = self.bg_image.resize((1100,650))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ttk.Label(fondo, image=self.bg_image)
        self.bg_label.place(x=0, y=0, width=1100, height=650)

        frame1 = tk.Frame(self, bg="#FFFFFF", highlightbackground="black", highlightthickness=1)
        frame1.place(x=350, y=10, width=400, height=630)

        self.logo_image = Image.open("imagenes/logo.png")
        self.logo_image = self.logo_image.resize((200,200))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = ttk.Label(frame1, image=self.logo_image, background="#FFFFFF")
        self.logo_label.place(x=100, y=20)

        user = ttk.Label(frame1, text="Nombre de usuario:", font="arial 16 bold", background="#FFFFFF")
        user.place(x=100, y=250)
        self.username = ttk.Entry(frame1, font="arial 16 bold")
        self.username.place(x=80, y=290, width=240, height=40)

        pasword = ttk.Label(frame1, text="Contraseña:", font="arial 16 bold", background="#FFFFFF")
        pasword.place(x=100, y=340)
        self.paswordus = ttk.Entry(frame1, show="*", font="arial 16 bold")
        self.paswordus.place(x=80, y=380, width=240, height=40)

        key = ttk.Label(frame1, text="Codigo de registro", font="arial 16 bold", background="#FFFFFF")
        key.place(x=100, y=430)
        self.keyus = ttk.Entry(frame1, show="*", font="arial 16 bold")
        self.keyus.place(x=80, y=470, width=240, height=40)

        btn3 = tk.Button(frame1, text="Registrar", font="arial 16 bold", command=self.registro)
        btn3.place(x=80, y=520, width=240, height=40)

        btn4 = tk.Button(frame1, text="Regresar", font="arial 16 bold", command=self.control2)
        btn4.place(x=80, y=570, width=240, height=40)
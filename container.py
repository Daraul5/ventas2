from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from categorias import Categorias
from proveedor import Proveedor
from informacion import Informacion
from abstracs import ModuleInterface
import sys
import os

class Container(tk.Frame, ModuleInterface):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.place(x=0, y=0, width=1100, height=650)
        self.logged_user = tk.StringVar()
        self.widgets()
        self.frames = {}

        for i in (Ventas, Inventario, Categorias, Proveedor, Informacion):
            try:
                frame = i(self)
                self.frames[i] = frame
                print(f"Frame {i.__name__} inicializado correctamente: {frame}") # Depuración
                frame.config(bg="#95c799", highlightbackground="gray", highlightthickness=1)
                frame.place(x=0, y=40, width=1100, height=610)
            except Exception as e:
                print(f"Error al inicializar {i.__name__}: {e}")

        self.show_frames(Ventas)
        self.mostrar_usuario_logueado() 

    def set_logged_user(self, username):
        """Método para establecer el nombre de usuario logueado."""
        self.logged_user.set(username)
        self.mostrar_usuario_en_informacion()

    def mostrar_usuario_en_informacion(self):
        """Actualiza el label de usuario en el frame de Información."""
        informacion_frame = self.frames.get(Informacion)
        if informacion_frame and hasattr(informacion_frame, 'cargar_usuario'):
            informacion_frame.cargar_usuario(self.logged_user.get())
        elif not informacion_frame:
            print("Error: El frame Información no está disponible.")
        elif not hasattr(informacion_frame, 'cargar_usuario'):
            print("Error: El frame Información no tiene el método cargar_usuario.")

    def mostrar_usuario_logueado(self):
        """Para depuración: muestra el usuario logueado en la consola."""
        print(f"Usuario logueado en Container: {self.logged_user.get()}")

    def show_frames(self, container):
        frame = self.frames.get(container)
        if frame:
            print(f"Levantando frame: {container.__name__}") # Confirmar el frame que se está levantando
            frame.tkraise()
        else:
            print(f"Error: El frame {container.__name__} no está inicializado o fue destruido.")

    def ventas(self):
        self.show_frames(Ventas)

    def inventario(self):
        print("Frames disponibles en self.frames:", self.frames.keys()) # Depuración adicional
        if Inventario in self.frames:
            self.show_frames(Inventario)
        else:
            print("Error: El frame Inventario no está disponible.")

    def categorias(self):
        self.show_frames(Categorias)
        # Asegurarse de que el frame de Categorias se haya inicializado
        if Categorias in self.frames:
            self.frames[Categorias].cargar_categoria()
            print("Cargando categorías al mostrar el frame.") # Depuración
        else:
            print("Error: El frame Categorias no está disponible para cargar datos.")

    def proveedor(self):
        self.show_frames(Proveedor)

    def informacion(self):
        self.show_frames(Informacion)
        self.mostrar_usuario_en_informacion() # Asegurarse de que se muestre el usuario al volver a Información
        if Informacion in self.frames:
            self.frames[Informacion].cargar_datos_facturacion()
        else:  
            print("Error: El frame Información no está disponible para cargar datos.")
            
    def widgets(self):
        frame2 = tk.Frame(self)
        frame2.place(x=0, y=0, width=1100, height=40)

        self.btn_ventas = Button(frame2, fg="white", bg="#0288d1",text="Ventas", font="sans 16 bold", command=self.ventas)
        self.btn_ventas.place(x=0, y=0, width=220, height=40)

        self.btn_inventario = Button(frame2, fg="white", bg="#43a047", text="Inventario", font="sans 16 bold", command=self.inventario)
        self.btn_inventario.place(x=220, y=0, width=220, height=40)

        self.btn_categorias = Button(frame2, fg="white", bg="#e53935", text="Categorias", font="sans 16 bold", command=self.categorias)
        self.btn_categorias.place(x=440, y=0, width=220, height=40)

        self.btn_proveedores = Button(frame2, fg="white", bg="#9c27b0",text="Proveedores", font="sans 16 bold", command=self.proveedor)
        self.btn_proveedores.place(x=660, y=0, width=220, height=40)

        self.btn_informacion = Button(frame2, fg="white", bg="#f57c00", text="Informacion", font="sans 16 bold", command=self.informacion)
        self.btn_informacion.place(x=880, y=0, width=220, height=40)

        self.buttons = [self.btn_ventas, self.btn_inventario, self.btn_categorias, self.btn_proveedores, self.btn_informacion]
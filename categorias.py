import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from abstracs import Modulos
import threading
import sys
import os

class Categorias(tk.Frame, Modulos):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.categorias_combobox()
        self.cargar_categoria()
        self.timer_categoria = None
        self.img_folder = "im"
        if not os.path.exists(self.img_folder):
            os.makedirs(self.img_folder)
            
    def widgets(self):
        
        frame = tk.Frame(self, bg="#ef5350")
        frame.place(x=0, y=0, width=1100, height=650)
        
        canvas_categorias = tk.LabelFrame(frame, text="Categorias", font="arial 14 bold", bg="#ef5350")
        canvas_categorias.place(x=300, y=10, width=780, height=580)
        
        self.canvas = tk.Canvas(canvas_categorias, bg="#ef5350")
        self.scrollbar = tk.Scrollbar(canvas_categorias, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#ef5350")
        
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        
        
        lblframe_buscar= LabelFrame(self, text="Buscar", font="arial 14 bold", bg="#ef5350")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)
        
        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.comboboxbuscar.place(x=5, y=5, width=260, height=40)
        self.comboboxbuscar.bind("<<ComboboxSelected>>", self.on_combobox_select)
        self.comboboxbuscar.bind("<KeyRelease>", self.filtrar_categorias)
        
        
        lblframe_seleccion = LabelFrame(self, text="Selección", font="arial 14 bold", bg="#ef5350")
        lblframe_seleccion.place(x=10, y=95, width=280, height=180)
        
        self.label1 = tk.Label(lblframe_seleccion, text="Categoria", font="arial 12 bold", bg="#ef5350")
        self.label1.place(x=5, y=5)
        
        self.label2 = tk.Label(lblframe_seleccion, text="Stock", font="arial 12 bold", bg="#ef5350")
        self.label2.place(x=5, y=40)
        
        self.label3 = tk.Label(lblframe_seleccion, text="Descripcion", wraplength=200 , font="arial 12 bold", bg="#ef5350")
        self.label3.place(x=5, y=75)
        
        lblframe_botones = LabelFrame(self, bg="#ef5350", text="Opciones", font="arial 14 bold")
        lblframe_botones.place(x=10, y=300, width=280, height=300)
        
        btn1 = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_categoria)
        btn1.place(x=20, y=20, width=180, height=40)
        
        btn2 = tk.Button(lblframe_botones, text="Editar", font="arial 14 bold", command=self.editar_categoria)
        btn2.place(x=20, y=80, width=180, height=40)
        
        btn3 = tk.Button(lblframe_botones, text="Eliminar", font="arial 14 bold", command=self.eliminar_categoria)
        btn3.place(x=20, y=140, width=180, height=40)
        
    def load_image(self):
        file_rut = filedialog.askopenfilename()  
        if file_rut:
            image = Image.open(file_rut)
            image = image.resize((200, 200), Image.LANCZOS)
            image_name = os.path.basename(file_rut)  
            image_save_rut = os.path.join(self.img_folder, image_name) 
            image.save(image_save_rut)
            
            self.image_tk = ImageTk.PhotoImage(image)
            
            self.producto_image = self.image_tk
            self.image_rut = image_save_rut  
            
            img_label = tk.Label(self.frameimg, image=self.image_tk)
            img_label.place(x=0, y=0, width=200, height=200)
            
    def categorias_combobox(self):
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.cur.execute('SELECT categoria FROM categorias')
        self.categoria =[row[0] for row in self.cur.fetchall()]
        self.comboboxbuscar['values'] = self.categoria
    
    def agregar_categoria(self):
        top = tk.Toplevel(self)
        top.title("Agregar categoria")
        top.geometry("700x400+200+50")
        top.config(bg="#ef5350")
        top.resizable(False,False)
        
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()
        
        tk.Label(top, text="Categoría: ", font="arial 12 bold", bg="#ef5350").place(x=20, y=20, width=80, height=25)
        entry_categoria = ttk.Entry(top, font="arial 12 bold")
        entry_categoria.place(x=120, y=20, width=250, height=30)

        tk.Label(top, text="Descripción: ", font="arial 12 bold", bg="#ef5350").place(x=20, y=60, width=80, height=25)
        entry_descripcion = ttk.Entry(top, font="arial 12 bold")
        entry_descripcion.place(x=120, y=60, width=250, height=30)

        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)

        btn_image = tk.Button(top, text="Cargar imagen", font="arial 12 bold", command=self.load_image)
        btn_image.place(x=470, y=260, width=150, height=40)
        
        def guardar():
            categoria = entry_categoria.get()
            descripcion = entry_descripcion.get()

            if not categoria or not descripcion:
                messagebox.showerror("Error", "Todos los campos deben ser llenados.")
                return

            stock = 0

            if hasattr(self, 'image_rut'):
                image_rut = self.image_rut
            else:
                image_rut = (r"im/def.png")

            try:
                self.cur.execute(
                    "INSERT INTO categorias (categoria, stock, descripcion, image_rut) VALUES (?, ?, ?, ?)",
                    (categoria, stock, descripcion, image_rut)
                )
                self.con.commit()
                self.cargar_categoria()  
                self.categorias_combobox()  
                top.destroy()
                messagebox.showinfo("Éxito", "Categoría agregada correctamente.")
            except sqlite3.Error as e:
                print("Error al agregar la categoría:", e)
                messagebox.showerror("Error", "No se pudo agregar la categoría. Intenta nuevamente.")
            
        tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar).place(x=50, y=260, width=150, height=40)
        tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy).place(x=260, y=260, width=150, height=40)
    
    def cargar_categoria(self, filtro=None, tip=None):
        self.after(0, self._cargar_categoria, filtro, tip)
    
    def _cargar_categoria(self, filtro=None, tip=None):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        query = "SELECT categoria, stock, descripcion, image_rut FROM categorias"
        params = []
        
        if filtro:
            query += " WHERE categoria LIKE ?"
            params.append(f"%{filtro}%")
        
        self.cur.execute(query, params)
        categorias = self.cur.fetchall()
        
        self.row = 0
        self.columns = 0
        
        for categoria, stock, descripcion, image_rut in categorias:
            self.mostrar_categorias(categoria, stock, descripcion, image_rut)
    
    def mostrar_categorias(self, categoria, stock, descripcion, image_rut):
        categoriaframe = tk.Frame(self.scrollable_frame, bg="#ef9a9a", relief="solid")
        categoriaframe.grid(row=self.row, column=self.columns, padx=10, pady=10)
        
        
        if image_rut and os.path.exists(image_rut):
            image = Image.open(image_rut)
            image = image.resize((200,200), Image.LANCZOS)
            imagen = ImageTk.PhotoImage(image)
            image_label = tk.Label(categoriaframe, image=imagen)
            image_label.image = imagen
            image_label.pack(expand=True, fill="both")
            
                
            image_label.bind("<Button-1>", lambda event: self.mostrar_click(categoria))
            image_label.pack(expand=True, fill="both")

        name_label = tk.Label(categoriaframe, text=categoria, bg="#ef9a9a", anchor="w", wraplength=450, font="arial 14 bold", width=60)
        name_label.pack(side="top", fill="both")
        
        stock_label = tk.Label(categoriaframe,text=f"Stock: {stock}",bg="#ef9a9a", anchor="w",wraplength=450,font="arial 14 bold", width=60)
        stock_label.pack(fill="x", anchor="w")
        
        desc_label = tk.Label(categoriaframe, text=f"Descripcion: {descripcion}", bg="#ef9a9a", anchor="w", wraplength=650, font="arial 14 bold", width=60)
        desc_label.pack(fill="x", anchor="w")
        
        self.columns += 1
        if self.columns > 0:
            self.columns = 0
            self.row += 1
            
    def on_combobox_select(self, event):
        self.actualizar_label()
    
    def actualizar_label(self, event=None):
        categoriaseleccionada = self.comboboxbuscar.get()
        
        try:
            self.cur.execute(
                "SELECT categoria, stock, descripcion FROM categorias WHERE categoria=?",
                (categoriaseleccionada,)
            )
            resultado = self.cur.fetchone() 
            
            if resultado is not None:
                categoria, stock, descripcion = resultado
                
                self.label1.config(text=f"Categoria: {categoria}")
                self.label2.config(text=f"Stock: {stock}")
                self.label3.config(text=f"Stock: {descripcion}")
            else:
                self.label1.config(text="Categoria no encontrado")
                self.label2.config(text="Stock no encontrado")
                
        except sqlite3.Error as e:
            print("Error al obtener los datos de la categoria:", e)
            messagebox.showerror("Error", "Error al obtener los datos de la categoria")
            
    def mostrar_click(self, categoria):
        try:
            self.comboboxbuscar.set(categoria)
            
            self.cur.execute("SELECT categoria, stock, descripcion FROM categorias WHERE categoria=?", (categoria,))
            resultado = self.cur.fetchone()
            
            if resultado is not None:
                categoria, stock, descripcion = resultado
                
                self.label1.config(text=f"Categoria: {categoria}")
                self.label2.config(text=f"Stock: {stock}")
                self.label3.config(text=f"Descripcion: {descripcion}")
            else:
                self.label1.config(text="Categoria no encontrado")
                self.label2.config(text="Stock no encontrado")
                self.label3.config(text=f"Descripcion no encontrada")
        except sqlite3.Error as e:
            print("Error al obtener los datos de la categoria:", e)
            messagebox.showerror("Error", "Error al obtener los datos de la categoria")
            
    def filtrar_categorias(self, event):
            
        if self.timer_categoria:
            self.timer_categoria.cancel()
        self.timer_categoria = threading.Timer(0.5, self._filter_categoria)
        self.timer_categoria.start()
        
    def _filter_categoria(self):
        typed = self.comboboxbuscar.get()
        
        if typed == '':
            data = self.categoria
        else:
            data = [item for item in self.categoria if typed.lower() in item.lower()]
        
        if data:
            self.comboboxbuscar['values'] = data
            self.comboboxbuscar.event_generate('<Down>')
        else:
            self.comboboxbuscar['values'] = ['No se encontroa la categoria']
            self.comboboxbuscar.event_generate('<Down>')
            
        self.cargar_categoria(filtro=typed)

    def editar_categoria(self):
        selected_item = self.comboboxbuscar.get()
        
        if not selected_item:
            messagebox.showerror("Error", "Debe seleccionar una categoría")
            return
        
        self.cur.execute("SELECT categoria, stock, descripcion, image_rut FROM categorias WHERE categoria = ?", (selected_item,))
        resultado = self.cur.fetchone()
        
        if not resultado:
            messagebox.showerror("Error", "Categoría no encontrada")
            return
        
        (categoria, stock, descripcion, image_rut) = resultado
      
        top = tk.Toplevel(self)
        top.title("Editar categoría")
        top.geometry("700x400+200+50")
        top.config(bg="#ef5350")
        top.resizable(False, False)
        
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()
        
        # Campo para la categoría
        tk.Label(top, text="Categoría: ", font="arial 12 bold", bg="#ef5350").place(x=20, y=20, width=80, height=25)
        entry_categoria = ttk.Entry(top, font="arial 12 bold")
        entry_categoria.place(x=120, y=20, width=250, height=30)
        entry_categoria.insert(0, categoria)
        
        # Mostrar el stock actual como un label
        tk.Label(top, text="Stock: ", font="arial 12 bold", bg="#ef5350").place(x=20, y=60, width=80, height=25)
        stock_label = tk.Label(top, text=f"{stock}", font="arial 12", bg="#ffffff", relief="solid", anchor="w")
        stock_label.place(x=120, y=60, width=250, height=30)
        
        # Campo para la descripción
        tk.Label(top, text="Descripción: ", font="arial 12 bold", bg="#ef5350").place(x=20, y=100, width=80, height=25)
        entry_descripcion = ttk.Entry(top, font="arial 12 bold")
        entry_descripcion.place(x=120, y=100, width=250, height=30)
        entry_descripcion.insert(0, descripcion)
        
        # Frame para la imagen
        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)
        
        if image_rut and os.path.exists(image_rut):
            image = Image.open(image_rut)
            image = image.resize((200, 200), Image.LANCZOS)
            imagen = ImageTk.PhotoImage(image)
            image_label = tk.Label(self.frameimg, image=imagen)
            image_label.image = imagen
            image_label.pack(side="left", padx=5)
        
        btn_image = tk.Button(top, text="Cargar imagen", font="arial 12 bold", command=self.load_image)
        btn_image.place(x=470, y=260, width=150, height=40)
        
        def guardar():
            nueva_categoria = entry_categoria.get()
            nueva_descripcion = entry_descripcion.get()
            
            if not nueva_categoria or not nueva_descripcion:
                messagebox.showerror("Error", "Llene todos los campos")
                return
            

            if hasattr(self, "image_rut"):
                image_rut = self.image_rut
            else:
                image_rut = (r"im/def.png")
            
            self.cur.execute(
                "UPDATE categorias SET categoria = ?, descripcion = ?, image_rut = ? WHERE categoria = ?",
                (nueva_categoria, nueva_descripcion, image_rut, selected_item)
            )
            self.con.commit()
            
            self.categorias_combobox()
            self.after(0, lambda: self.cargar_categoria(filtro=nueva_categoria))
            top.destroy()
            messagebox.showinfo("Éxito", "Categoría editada correctamente")
        
        btnguardar = tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar)
        btnguardar.place(x=80, y=260, width=150, height=40)
        
        btnsalir = tk.Button(top, text="Salir", font="arial 12 bold", command=top.destroy)
        btnsalir.place(x=260, y=260, width=150, height=40)
    
    def eliminar_categoria(self):
        categoria_seleccionada = self.comboboxbuscar.get()
        
        if not categoria_seleccionada:
            messagebox.showerror("Error", "Por favor selecciona una categoría para eliminar")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar la categoría '{categoria_seleccionada}'?")
        
        if confirmar:
            try:
                self.cur.execute("DELETE FROM categorias WHERE categoria = ?", (categoria_seleccionada,))
                self.con.commit()
                
                self.categoria.remove(categoria_seleccionada)  
                self.comboboxbuscar['values'] = self.categoria  
                self.cargar_categoria()  
                messagebox.showinfo("Éxito", f"La categoría '{categoria_seleccionada}' fue eliminada exitosamente")
                
            except sqlite3.Error as e:
                print(f"Error al eliminar la categoría: {e}")
                messagebox.showerror("Error", "No se pudo eliminar la categoría. Por favor, intenta nuevamente.")
        
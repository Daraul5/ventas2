import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from abstracs import Modulos
import threading
import sys
import os

class Inventario(tk.Frame, Modulos):
    
    def __init__(self, padre):
        super().__init__(padre)
        self.con = sqlite3.connect('database.db', check_same_thread=False) 
        self.cur = self.con.cursor()  
        self.articulos = []  
        self.categoria = [] 
        self.widgets()
        self.articulos_combobox()
        self.cargar_articulos()
        self.cargar_categorias()  
        self.timer_articulos = None
        self.images_folder = "fotos"
        
        
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)
        
    def widgets(self):
        
        frame = tk.Frame(self, bg="#66bb6a")
        frame.place(x=0, y=0, width=1100, height=650)
    #--------------------------------------------------------------------------------------------------------
        canvas_articulos = tk.LabelFrame(frame, text="Articulos", font="arial 14 bold", bg="#66bb6a")
        canvas_articulos.place(x=300, y=10, width=780, height=580)
        
        self.canvas = tk.Canvas(canvas_articulos, bg="#66bb6a")
        self.scrollbar = tk.Scrollbar(canvas_articulos, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#66bb6a")
        
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
        
    #-------------------------------------------------------------------------------------------------------
        lblframe_buscar= LabelFrame(self, text="Buscar", font="arial 14 bold", bg="#66bb6a")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)
        
        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.comboboxbuscar.place(x=5, y=5, width=260, height=40)
        self.comboboxbuscar.bind("<<ComboboxSelected>>", self.on_combobox_select)
        self.comboboxbuscar.bind("<KeyRelease>", self.filtrar_articulos)
        
    #-------------------------------------------------------------------------------------------------------
    
        lblframe_seleccion = LabelFrame(self, text="Selección", font="arial 14 bold", bg="#66bb6a")
        lblframe_seleccion.place(x=10, y=95, width=280, height=270)
        
        self.label7 = tk.Label(lblframe_seleccion, text="Categorias", font="arial 12", bg="#66bb6a")
        self.label7.place(x=5,y=5)
        
        self.label1 = tk.Label(lblframe_seleccion, text="Articulo:", font="arial 12", bg="#66bb6a", wraplength=150)
        self.label1.place(x=5,y=40)
        
        self.label2 = tk.Label(lblframe_seleccion, text="Precio:", font="arial 12", bg="#66bb6a")
        self.label2.place(x=5,y=70)
        
        self.label3 = tk.Label(lblframe_seleccion, text="Costo:", font="arial 12", bg="#66bb6a")
        self.label3.place(x=5,y=100)
        
        self.label4 = tk.Label(lblframe_seleccion, text="Stock:", font="arial 12", bg="#66bb6a")
        self.label4.place(x=5,y=130)

        self.label5 = tk.Label(lblframe_seleccion, text="Estado:", font="arial 12", bg="#66bb6a")
        self.label5.place(x=5,y=160)
        
    #-------------------------------------------------------------------------------------------------------

        lblframe_botones = LabelFrame(self, bg="#66bb6a", text="Opciones", font="arial 14 bold")
        lblframe_botones.place(x=10, y=360, width=280, height=300)
        
        btn1 = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_articulo)
        btn1.place(x=20, y=10, width=180, height=40)
        
        btn2 = tk.Button(lblframe_botones, text="Editar", font="arial 14 bold", command=self.editar_articulos)
        btn2.place(x=20, y=60, width=180, height=40)
        
        btn3 = tk.Button(lblframe_botones, text="Eliminar", font="arial 14 bold", command=self.eliminar_articulo)
        btn3.place(x=20, y=110, width=180, height=40)
        
        btn4 = tk.Button(lblframe_botones, text="Sumar stock", font="arial 14 bold", command=self.sumar_stock)
        btn4.place(x=20, y=160, width=180, height=40)
        
    def cargar_categorias(self):
        try:
            self.cur.execute("SELECT DISTINCT categoria FROM categorias")
            self.categoria = [row[0] for row in self.cur.fetchall()]  
        except sqlite3.Error as e:
            print(f"Error al cargar categorías: {e}")
            messagebox.showerror("Error", "No se pudieron cargar las categorías.")
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            image = image.resize((200,200), Image.LANCZOS)
            image_name = os.path.basename(file_path)
            image_save_path = os.path.join(self.images_folder, image_name)
            image.save(image_save_path)
            
            self.image_tk = ImageTk.PhotoImage(image)
            
            self.producto_image = self.image_tk
            self.image_path = image_save_path
            
            img_label = tk.Label(self.frameimg, image = self.image_tk)
            img_label.place(x=0, y=0, width=200, height=200)
            
    def articulos_combobox(self):
        try:
            self.cur.execute('SELECT articulo FROM articulos')
            self.articulos = [row[0] for row in self.cur.fetchall()]  
            self.comboboxbuscar['values'] = self.articulos 
        except sqlite3.Error as e:
            print(f"Error al cargar artículos: {e}")
            messagebox.showerror("Error", "No se pudieron cargar los artículos.")

    def sumar_stock(self):
        articulo_seleccionado = self.comboboxbuscar.get()

        if not articulo_seleccionado:
            messagebox.showerror("Error", "Selecciona un artículo para agregar stock")
            return

        try:
            self.cur.execute("SELECT id, stock FROM articulos WHERE articulo = ?", (articulo_seleccionado,))
            resultado = self.cur.fetchone()

            if not resultado:
                messagebox.showerror("Error", "El artículo seleccionado no fue encontrado.")
                return

            producto_id, stock_actual = resultado

        except sqlite3.Error as e:
            print(f"Error al obtener el producto_id: {e}")
            messagebox.showerror("Error", "No se pudo obtener el producto.")
            return

        top = tk.Toplevel(self)
        top.title(f"Sumar Stock - {articulo_seleccionado}")
        top.geometry("400x300")
        top.config(bg="#66bb6a")
        top.resizable(False, False)

        tk.Label(top, text=f"Artículo: {articulo_seleccionado}", font="arial 12 bold", bg="#66bb6a").pack(pady=5)
        
        stock_label = tk.Label(top, text=f"Stock: {stock_actual}", font="arial 12 bold", bg="#66bb6a")
        stock_label.pack(pady=5)

        tk.Label(top, text="Escanea el nuevo código de barras:", font="arial 12 bold", bg="#66bb6a").pack(pady=5)
        entry_codigo = ttk.Entry(top, font="arial 12 bold")
        entry_codigo.pack(pady=10, fill="x", padx=20)
        entry_codigo.focus()

        def guardar_codigo():
            codigo_barras = entry_codigo.get().strip()

            if not codigo_barras:
                messagebox.showerror("Error", "El campo está vacío. Escanea un código válido.")
                return

            try:
                self.con.execute("BEGIN TRANSACTION")

                self.cur.execute(
                    "INSERT INTO inventario (producto_id, codigo_barras) VALUES (?, ?)", 
                    (producto_id, codigo_barras)
                )
                self.con.commit()

                self.cur.execute("UPDATE articulos SET stock = stock + 1 WHERE id = ?", (producto_id,))
                self.con.commit()

                self.cur.execute("SELECT stock FROM articulos WHERE id = ?", (producto_id,))
                stock_actualizado = self.cur.fetchone()[0]
                stock_label.config(text=f"Stock: {stock_actualizado}")

                entry_codigo.delete(0, tk.END)
                entry_codigo.focus()

            except sqlite3.IntegrityError:
                messagebox.showerror("Error", f"El código de barras '{codigo_barras}' ya existe en este producto.")
                self.con.rollback()
            except sqlite3.Error as e:
                print(f"Error al agregar código de barras: {e}")
                messagebox.showerror("Error", "No se pudo agregar el código de barras.")
                self.con.rollback()

      
        entry_codigo.bind("<Return>", lambda event: guardar_codigo())

        tk.Button(top, text="Guardar Código", font="arial 12 bold", command=guardar_codigo).pack(pady=10)

        tk.Button(top, text="Salir", font="arial 12 bold", command=lambda: [self.cargar_articulos(), top.destroy()]).pack(pady=10)

    def agregar_articulo(self):
        self.cargar_categorias()

        top = tk.Toplevel(self)
        top.title("Agregar artículo")
        top.geometry("700x400+200+50")  
        top.config(bg="#66bb6a")
        top.resizable(False, False)

        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        # Campo para la categoría
        tk.Label(top, text="Categoría:", font="arial 12 bold", bg="#66bb6a").place(x=20, y=20, width=150, height=25)
        combobox_categoria = ttk.Combobox(top, font="arial 12 bold", values=self.categoria, state="readonly")
        combobox_categoria.place(x=180, y=20, width=250, height=30)

        # Campo para el nombre del artículo
        tk.Label(top, text="Artículo:", font="arial 12 bold", bg="#66bb6a").place(x=20, y=70, width=150, height=25)
        entry_articulo = ttk.Entry(top, font="arial 12 bold")
        entry_articulo.place(x=180, y=70, width=250, height=30)

        # Campo para el precio
        tk.Label(top, text="Precio:", font="arial 12 bold", bg="#66bb6a").place(x=20, y=120, width=150, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=180, y=120, width=250, height=30)

        # Campo para el costo
        tk.Label(top, text="Costo:", font="arial 12 bold", bg="#66bb6a").place(x=20, y=170, width=150, height=25)
        entry_costo = ttk.Entry(top, font="arial 12 bold")
        entry_costo.place(x=180, y=170, width=250, height=30)

        # Label para mostrar el stock dinámico
        tk.Label(top, text="Stock:", font="arial 12 bold", bg="#66bb6a").place(x=20, y=220, width=150, height=25)
        stock_label = tk.Label(top, text="Stock: 0", font="arial 12 bold", bg="#66bb6a") 
        stock_label.place(x=180, y=220, width=250, height=30)

        # Campo para el estado
        tk.Label(top, text="Estado:", font="arial 12 bold", bg="#66bb6a").place(x=20, y=270, width=150, height=25)
        combobox_estado = ttk.Combobox(top, font="arial 12 bold", values=["Activo", "Inactivo"], state="readonly")
        combobox_estado.place(x=180, y=270, width=250, height=30)

        # Frame para mostrar la imagen
        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=470, y=30, width=200, height=200)
        self.default_image = Image.open("fotos/default.png")  
        self.default_image = self.default_image.resize((200, 200), Image.LANCZOS)
        self.default_image_tk = ImageTk.PhotoImage(self.default_image)
        default_image_label = tk.Label(self.frameimg, image=self.default_image_tk, bg="white")
        default_image_label.pack(expand=True, fill="both")
        self.frameimg_label = default_image_label 

        # Botón para cargar imagen
        btnimage = tk.Button(top, text="Cargar imagen", font="arial 12 bold", command=self.load_image)
        btnimage.place(x=470, y=240, width=150, height=40)

        def guardar():
            categoria = combobox_categoria.get()
            articulo = entry_articulo.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            estado = combobox_estado.get()

            if not categoria or not articulo or not precio or not costo or not estado:
                messagebox.showerror("Error", "Todos los campos deben ser llenados.")
                return

            try:
                precio = float(precio)
                costo = float(costo)
            except ValueError:
                messagebox.showerror("Error", "Precio y costo deben ser valores válidos.")
                return

            if hasattr(self, "image_path"):
                image_path = self.image_path
            else:
                image_path = "fotos/default.png"

            try:
                self.con.execute("BEGIN TRANSACTION")

                self.cur.execute(
                    "INSERT INTO articulos (categoria, articulo, precio, costo, stock, estado, image_path) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (categoria, articulo, precio, costo, 0, estado, image_path)
                )
                self.con.commit()

                self.cur.execute("SELECT id FROM articulos WHERE articulo = ?", (articulo,))
                resultado = self.cur.fetchone()

                if resultado is None:
                    messagebox.showerror("Error", "No se pudo obtener el producto_id del artículo.")
                    return

                producto_id = resultado[0]

                self.cur.execute(
                    "INSERT INTO inventario (producto_id) VALUES (?)", 
                    (producto_id,)
                )
                self.con.commit()

                stock_label.config(text="Stock: 1")

                self.cargar_articulos()
                self.cargar_categorias()

                # Limpiar los campos
                combobox_categoria.set("")
                entry_articulo.delete(0, tk.END)
                entry_precio.delete(0, tk.END)
                entry_costo.delete(0, tk.END)
                combobox_estado.set("")
                self.image_path = "fotos/default.png" 
                self.frameimg_label.config(image=self.default_image_tk) 
                self.frameimg_label.image = self.default_image_tk 

                top.destroy()
                messagebox.showinfo("Éxito", "Artículo agregado correctamente.")

            except sqlite3.Error as e:
                self.con.rollback()
                print(f"Error al agregar artículo: {e}")
                messagebox.showerror("Error", "No se pudo agregar el artículo.")

        tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar).place(x=470, y=300, width=150, height=40)
        tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy).place(x=470, y=350, width=150, height=40)

        entry_articulo.focus() 
        
        
    def cargar_articulos(self, filtro=None, categoria=None):
        try:
            query = "SELECT categoria, articulo, precio, stock, image_path FROM articulos"
            params = []

           
            if filtro:
                query += " WHERE articulo LIKE ?"
                params.append(f"%{filtro}%")
            elif categoria:
                query += " WHERE categoria LIKE ?"
                params.append(f"%{categoria}%")

           
            self.cur.execute(query, params)
            articulos = self.cur.fetchall()

            
            self.articulos = [articulo[1] for articulo in articulos] if articulos else []
            
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()

            
            if not articulos:
                tk.Label(self.scrollable_frame, text="No hay artículos que mostrar", bg="white", font="arial 12 italic").pack()
                return

            
            self.row, self.column = 0, 0

            for categoria, articulo, precio, stock, image_path in articulos:
                self.mostrar_articulo(categoria, articulo, precio, stock, image_path)
        except sqlite3.Error as e:
            print(f"Error al cargar artículos: {e}")
            messagebox.showerror("Error", "No se pudieron cargar los artículos correctamente.")
            
    
    def mostrar_articulo(self, categoria, articulo, precio, stock, image_path=None):
        articuloframe = tk.Frame(self.scrollable_frame, bg="#a5d6a7", relief="solid")
        articuloframe.grid(row=self.row, column=self.column, padx=10, pady=10)

        if image_path and os.path.exists(image_path): 
            image = Image.open(image_path)
            image = image.resize((150, 150), Image.LANCZOS)
            imagen = ImageTk.PhotoImage(image)
            image_label = tk.Label(articuloframe, image=imagen, bg="#a5d6a7")
            image_label.image = imagen
            image_label.pack(expand=True, fill="both")
            image_label.bind("<Button-1>", lambda event: self.mostrar_click(articulo))
            image_label.pack(expand=True, fill="both")

        category_label = tk.Label(articuloframe, text=f"Categoría: {categoria}", bg="#a5d6a7", anchor="w", wraplength=150, font="arial 10 bold")
        category_label.pack(side="top", fill="both")

        name_label = tk.Label(articuloframe, text=f"Nombre: {articulo}", bg="#a5d6a7", anchor="w", wraplength=150, font="arial 10 bold")
        name_label.pack(side="top", fill="both")

        price_label = tk.Label(articuloframe, text=f"Precio: ${precio:.2f}", bg="#a5d6a7", anchor="w", wraplength=150, font="arial 10")
        price_label.pack(fill="x", anchor="w")

        stock_label = tk.Label(articuloframe, text=f"Stock: {stock}", bg="#a5d6a7", anchor="w", wraplength=150, font="arial 10")
        stock_label.pack(fill="x", anchor="w")

        self.column += 1
        if self.column > 3: 
            self.column = 0
            self.row += 1
    def on_combobox_select(self, event):
        self.actualizar_label()
    
    def actualizar_label(self, event=None):
        articulo_seleccionado = self.comboboxbuscar.get()
        
        try:
            self.cur.execute("SELECT categoria, articulo, precio, costo, stock, estado FROM articulos WHERE articulo=?", (articulo_seleccionado,))
            resultado = self.cur.fetchone()
            
            if resultado is not None:
                categoria,articulo, precio, costo, stock, estado = resultado
                
                self.label7.config(text=f"Categoria: {categoria}")
                self.label1.config(text=f"Artículo: {articulo}")
                self.label2.config(text=f"Precio: {precio}")
                self.label3.config(text=f"Costo: {costo}")
                self.label4.config(text=f"Stock: {stock}")
                self.label5.config(text=f"Estado: {estado}")
                
                
                if estado and estado.lower() == "activo":
                    self.label5.config(fg="green")
                elif estado and estado.lower() == "inactivo":
                    self.label5.config(fg="red")
                else:
                    self.label5.config(fg="black")
            else:
                self.label7.config(text="Categoria no encontrada")
                self.label1.config(text="Artículo no encontrado")
                self.label2.config(text="Precio no encontrado")
                self.label3.config(text="Costo no encontrado")
                self.label4.config(text="Stock no encontrado")
                self.label5.config(text="Estado no encontrado", fg="black")
                
        except sqlite3.Error as e:
            print("Error al obtener los datos del articulo:", e)
            messagebox.showerror("Error", "Error al obtener los datos del articulo")
    def mostrar_click(self, articulo):
        try:
            self.comboboxbuscar.set(articulo)
            
            
            self.cur.execute("SELECT categoria, articulo, precio, costo, stock, estado FROM articulos WHERE articulo=?", (articulo,))
            resultado = self.cur.fetchone()
            
            if resultado is not None:
                categoria, articulo, precio, costo, stock, estado = resultado
                
                
                self.label7.config(text=f"Categoria: {categoria}")
                self.label1.config(text=f"Artículo: {articulo}")
                self.label2.config(text=f"Precio: {precio}")
                self.label3.config(text=f"Costo: {costo}")
                self.label4.config(text=f"Stock: {stock}")
                self.label5.config(text=f"Estado: {estado}")
                
                if estado and estado.lower() == "activo":
                    self.label5.config(fg="green")
                elif estado and estado.lower() == "inactivo":
                    self.label5.config(fg="red")
                else:
                    self.label5.config(fg="black")
            else:
                self.label7.config(text="Categoria no encontrada")
                self.label1.config(text="Artículo no encontrado")
                self.label2.config(text="Precio no encontrado")
                self.label3.config(text="Costo no encontrado")
                self.label4.config(text="Stock no encontrado")
                self.label5.config(text="Estado no encontrado", fg="black")
                
        except sqlite3.Error as e:
            print("Error al obtener los datos del artículo:", e)
            messagebox.showerror("Error", "Error al obtener los datos del artículo")
    
    def filtrar_articulos(self, event):
        
        if self.timer_articulos:
            self.timer_articulos.cancel()
        self.timer_articulos = threading.Timer(0.5, self._filter_articulos)
        self.timer_articulos.start()
        
    def _filter_articulos(self):
        try:
            typed = self.comboboxbuscar.get()

            if not self.articulos:
                self.articulos_combobox()  
            if typed == '':
                data = self.articulos  
            else:
                data = [item for item in self.articulos if typed.lower() in item.lower()]

            if data:
                self.comboboxbuscar['values'] = data
                self.comboboxbuscar.event_generate('<Down>')
            else:
                self.comboboxbuscar['values'] = ['No se encontraron resultados']
                self.comboboxbuscar.event_generate('<Down>')
        except AttributeError as e:
            print(f"Error en _filter_articulos: {e}")
            messagebox.showerror("Error", "Ocurrió un problema al filtrar los artículos.")
                
    def editar_articulos(self):
        selected_item = self.comboboxbuscar.get()
        
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un artículo para editar")
            return
        
        try:
            self.cur.execute("SELECT categoria, articulo, precio, costo, estado, image_path FROM articulos WHERE articulo = ?", (selected_item,))
            resultado = self.cur.fetchone()
            
            if not resultado:
                messagebox.showerror("Error", "Artículo no encontrado")
                return
        except sqlite3.Error as e:
            print(f"Error al buscar artículo: {e}")
            messagebox.showerror("Error", "No se pudo acceder a la base de datos.")
            return
        
        (categoria, articulo, precio, costo, estado, image_path) = resultado
        print(resultado)
        top = tk.Toplevel(self)
        top.title("Editar artículo")
        top.geometry("700x400+200+50")
        top.config(bg="#66bb6a")
        top.resizable(False, False)
        
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()
        
        # Campo para la categoría
        tk.Label(top, text="Categoría:", font="arial 12 bold", bg="#66bb6a").place(x=20, y=20, width=150, height=25)
        combobox_categoria = ttk.Combobox(top, font="arial 12 bold", values=self.categoria, state="readonly")
        combobox_categoria.place(x=180, y=20, width=250, height=30)
        combobox_categoria.set(categoria)
        
        # Campo para el nombre del artículo
        tk.Label(top, text="Artículo:", font="arial 12 bold", bg="#66bb6a").place(x=20, y=70, width=150, height=25)
        entry_articulo = ttk.Entry(top, font="arial 12 bold")
        entry_articulo.place(x=180, y=70, width=250, height=30)
        entry_articulo.insert(0, articulo)
        
        # Campo para el precio
        tk.Label(top, text="Precio:", font="arial 12 bold", bg="#66bb6a").place(x=20, y=120, width=150, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=180, y=120, width=250, height=30)
        entry_precio.insert(0, precio)
        
        # Campo para el costo
        tk.Label(top, text="Costo:", font="arial 12 bold", bg="#66bb6a").place(x=20, y=170, width=150, height=25)
        entry_costo = ttk.Entry(top, font="arial 12 bold")
        entry_costo.place(x=180, y=170, width=250, height=30)
        entry_costo.insert(0, costo)
        
        # Campo para el estado
        tk.Label(top, text="Estado:", font="arial 12 bold", bg="#66bb6a").place(x=20, y=220, width=150, height=25)
        combobox_estado = ttk.Combobox(top, font="arial 12 bold", values=["Activo", "Inactivo"], state="readonly")
        combobox_estado.place(x=180, y=220, width=250, height=30)
        combobox_estado.set(estado)
        
        
        # Selecciona la opción correspondiente en el combobox de estado
        if estado and estado.lower() == "activo":
            combobox_estado.current(0)
        elif estado and estado.lower() == "inactivo":
            combobox_estado.current(1)
        else:
            combobox_estado.set("")
        
        # Frame para la imagen
        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)
        
        if image_path and os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.LANCZOS)
            self.product_image = ImageTk.PhotoImage(image)
            self.image_path = image_path
            image_label = tk.Label(self.frameimg, image=self.product_image)
            image_label.pack(expand=True, fill="both")
        
        def guardar():
            categoria = combobox_categoria.get()
            nuevo_articulo = entry_articulo.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            estado = combobox_estado.get()
            
            
            if not categoria or not nuevo_articulo or not precio or not costo or not estado:
                messagebox.showerror("Error", "Llene todos los campos")
                return
            
            try:
                precio = float(precio)
                costo = float(costo)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Precio, costo y stock deben ser números válidos")
                return
            
            if hasattr(self, "image_path"):
                image_path = self.image_path 
            else:
                image_path = (r"fotos/default.png")
            
            try:
                self.cur.execute("UPDATE articulos SET categoria=?, articulo=?, precio=?, costo=?, estado=?, image_path=? WHERE articulo=?", 
                                (categoria, nuevo_articulo, precio, costo, estado, image_path, selected_item))
                self.con.commit()
                
                self.cur.execute(
                    "UPDATE categorias SET stock = (SELECT SUM(stock) FROM articulos WHERE categoria = ?) WHERE categoria = ?",
                    (categoria, categoria)
                )
                self.con.commit()
                self.articulos_combobox()
                
                self.after(0, lambda: self.cargar_articulos(filtro=nuevo_articulo))
                
                top.destroy()
                messagebox.showinfo("Éxito", "Artículo editado correctamente")
            except sqlite3.Error as e:
                print(f"Error al actualizar el artículo: {e}")
                messagebox.showerror("Error", "No se pudo actualizar el artículo.")
                
        btnimage = tk.Button(top, text="Cargar imagen", font="arial 12 bold", command=self.load_image)
        btnimage.place(x=470, y=240, width=150, height=40)
        
        btnguardar = tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar)
        btnguardar.place(x=470, y=290, width=150, height=40)
        
        btnsalir = tk.Button(top, text="Salir", font="arial 12 bold", command=top.destroy)
        btnsalir.place(x=470, y=350, width=150, height=40)
            
    def eliminar_articulo(self):
        articulo_seleccionado = self.comboboxbuscar.get()
        
        if not articulo_seleccionado:
            messagebox.showerror("Error", "Por favor selecciona un artículo para eliminar")
            return

        if articulo_seleccionado not in self.articulos:
            messagebox.showerror("Error", "El artículo seleccionado no se encuentra en la lista actual")
            return

        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el artículo '{articulo_seleccionado}'?")
        
        if confirmar:
            try:
                self.cur.execute("SELECT categoria FROM articulos WHERE articulo = ?", (articulo_seleccionado,))
                categoria_resultado = self.cur.fetchone()
                
                if not categoria_resultado:
                    messagebox.showerror("Error", "No se encontró la categoría del artículo seleccionado.")
                    return

                categoria = categoria_resultado[0] 

                # Eliminar el artículo
                self.cur.execute("DELETE FROM articulos WHERE articulo = ?", (articulo_seleccionado,))
                self.con.commit()

                
                self.cur.execute(
                    "UPDATE categorias SET stock = (SELECT SUM(stock) FROM articulos WHERE categoria = ?) WHERE categoria = ?",
                    (categoria, categoria)
                )
                self.con.commit()

                self.cur.execute(
                    "UPDATE categorias SET stock = 0 WHERE categoria = ? AND NOT EXISTS (SELECT 1 FROM articulos WHERE categoria = ?)",
                    (categoria, categoria)
                )
                self.con.commit()

                if articulo_seleccionado in self.articulos:
                    self.articulos.remove(articulo_seleccionado)
                self.comboboxbuscar['values'] = self.articulos
                self.cargar_articulos()
                self.actualizar_label()
                messagebox.showinfo("Éxito", f"El artículo '{articulo_seleccionado}' fue eliminado exitosamente")
            
            except sqlite3.Error as e:
                print(f"Error al eliminar el artículo: {e}")
                messagebox.showerror("Error", "No se pudo eliminar el artículo. Por favor, intenta nuevamente")
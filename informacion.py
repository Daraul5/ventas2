from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
from tkinter import simpledialog, messagebox, filedialog
import pandas as pd
import os
import datetime

class Informacion(tk.Frame):
    db_name = "database.db"

    def __init__(self, padre):
        super().__init__(padre)
        self.logged_user_label = None
        self.empresa_label = None
        self.factura_label = None 
        self.total_ventas_label = None 
        self.widgets()
        self.cargar_info_empresa()
        self.cargar_datos_facturacion()

    def widgets(self):
        frame = tk.Frame(self, bg="#ffb74d")
        frame.place(x=0, y=0, width=1100, height=650)

        labelinfo = tk.LabelFrame(frame, text="Usuario", bg="#ffb74d", font="arial 14 bold")
        labelinfo.place(x=50, y=50, width=500, height=225)

        labelinfo2 = tk.LabelFrame(frame, text="Informacion", bg="#ffb74d", font="arial 14 bold")
        labelinfo2.place(x=550, y=50, width=500, height=225)

        labelinfo3 = tk.LabelFrame(frame, text="Exportar", bg="#ffb74d", font="arial 14 bold")
        labelinfo3.place(x=50, y=300, width=1000, height=225)

        empresa_label_text = tk.Label(labelinfo, text="Nombre de la empresa: ", bg="#ffb74d", font="arial 12 bold")
        empresa_label_text.place(x=10, y=20)
        self.empresa_label = tk.Label(labelinfo, text="", bg="#ffb74d", font="arial 12 bold")
        self.empresa_label.place(x=200, y=20)

        usuario_label_text = tk.Label(labelinfo, text="Nombre de usuario: ", bg="#ffb74d", font="arial 12 bold")
        usuario_label_text.place(x=10, y=60)
        self.logged_user_label = tk.Label(labelinfo, text="", bg="#ffb74d", font="arial 12 bold")
        self.logged_user_label.place(x=180, y=60)

        facturas_label_text = tk.Label(labelinfo, text="Última Factura: ", bg="#ffb74d", font="arial 12 bold")
        facturas_label_text.place(x=10, y=100)
        self.factura_label = tk.Label(labelinfo, text="", bg="#ffb74d", font="arial 12 bold")
        self.factura_label.place(x=150, y=100)

        total_label_text = tk.Label(labelinfo, text="Total Ventas: $", bg="#ffb74d", font="arial 12 bold")
        total_label_text.place(x=10, y=140)
        self.total_ventas_label = tk.Label(labelinfo, text="0.00", bg="#ffb74d", font="arial 12 bold")
        self.total_ventas_label.place(x=150, y=140)

        info_label = tk.Label(labelinfo2, text="Información de la empresa: ", bg="#ffb74d", font="arial 12 bold")
        info_label.place(x=10, y=20)
        btninfo = tk.Button(labelinfo2, text="Ver información", bg="white", font="arial 12 bold", command=self.mostrar_info_empresa)
        btninfo.place(x=10, y=60, width=200, height=40)
        edit_label = tk.Label(labelinfo2, text="Editar información: ", bg="#ffb74d", font="arial 12 bold")
        edit_label.place(x=250, y=20)
        btnedit = tk.Button(labelinfo2, text="Editar", bg="white", font="arial 12 bold", command=self.editar_info_empresa)
        btnedit.place(x=250, y=60, width=200, height=40)

        ventas_label = tk.Label(labelinfo3, text="Ventas", bg="#ffb74d", font="arial 12 bold")
        ventas_label.place(x=190, y=130)
        adminventas = tk.Button(labelinfo3, text="Administrar ventas", bg="white", font="arial 12 bold", wraplength=90, command=self.administrar_ventas)
        adminventas.place(x=165, y=20, width=110, height=110)
        inventario_label = tk.Label(labelinfo3, text="Inventario", bg="#ffb74d", font="arial 12 bold")
        inventario_label.place(x=490, y=130)
        admininventario = tk.Button(labelinfo3, text="Administrar inventario", bg="white", font="arial 12 bold", wraplength=90, command=self.administrar_inventario)
        admininventario.place(x=465, y=20, width=110, height=110)
        categorias_label = tk.Label(labelinfo3, text="Categorias", bg="#ffb74d", font="arial 12 bold")
        categorias_label.place(x=790, y=130)
        admincategorias = tk.Button(labelinfo3, text="Administrar categorias", bg="white", font="arial 12 bold", wraplength=90, command=self.administrar_categorias)
        admincategorias.place(x=765, y=20, width=110, height=110)

    def cargar_usuario(self, username):
        """Este método actualiza el label con el nombre del usuario."""
        if self.logged_user_label:
            self.logged_user_label.config(text=username)

    def cargar_info_empresa(self):
        """Carga el nombre de la empresa desde la base de datos y lo muestra."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nombre FROM empresa LIMIT 1")
                empresa_data = cursor.fetchone()
                if empresa_data:
                    self.empresa_label.config(text=empresa_data[0])
                else:
                    self.empresa_label.config(text="No configurado")
        except sqlite3.Error as e:
            print(f"Error al cargar información de la empresa: {e}")
            self.empresa_label.config(text="Error al cargar")

    def cargar_datos_facturacion(self):
        """Carga el número de la última factura y el total de ventas."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                # Obtener el número de la última factura
                cursor.execute("SELECT MAX(factura) FROM ventas")
                ultima_factura = cursor.fetchone()[0]
                self.factura_label.config(text=ultima_factura if ultima_factura is not None else "Ninguna")

                # Obtener el total de todas las ventas
                cursor.execute("SELECT SUM(total) FROM ventas")
                total_ventas = cursor.fetchone()[0]
                self.total_ventas_label.config(text=f"{total_ventas:.2f}" if total_ventas is not None else "0.00")
        except sqlite3.Error as e:
            print(f"Error al cargar datos de facturación: {e}")
            self.factura_label.config(text="Error")
            self.total_ventas_label.config(text="Error")

    def editar_info_empresa(self):

        ventana_editar = tk.Toplevel(self)
        ventana_editar.title("Editar Información de la Empresa")
        ventana_editar.geometry("400x400")
        ventana_editar.resizable(False, False)
        ventana_editar.config(bg="#ffb74d")

        ventana_editar.transient(self.master)
        ventana_editar.grab_set()
        ventana_editar.focus_set()
        ventana_editar.lift()
        tk.Label(ventana_editar, text="Editar Información de la Empresa", font="arial 14 bold", bg="#ffb74d").place(x=50, y=20)
        tk.Label(ventana_editar, text="Nombre:", font="arial 12", bg="#ffb74d").place(x=20, y=80)
        entry_nombre = tk.Entry(ventana_editar, font="arial 12")
        entry_nombre.place(x=150, y=80, width=200)
        tk.Label(ventana_editar, text="Dirección:", font="arial 12", bg="#ffb74d").place(x=20, y=120)
        entry_direccion = tk.Entry(ventana_editar, font="arial 12")
        entry_direccion.place(x=150, y=120, width=200)
        tk.Label(ventana_editar, text="Teléfono:", font="arial 12", bg="#ffb74d").place(x=20, y=160)
        entry_telefono = tk.Entry(ventana_editar, font="arial 12")
        entry_telefono.place(x=150, y=160, width=200)
        tk.Label(ventana_editar, text="Email:", font="arial 12", bg="#ffb74d").place(x=20, y=200)
        entry_email = tk.Entry(ventana_editar, font="arial 12")
        entry_email.place(x=150, y=200, width=200)
        tk.Label(ventana_editar, text="Web:", font="arial 12", bg="#ffb74d").place(x=20, y=240)
        entry_web = tk.Entry(ventana_editar, font="arial 12")
        entry_web.place(x=150, y=240, width=200)

        def guardar_cambios():
            nuevo_nombre = entry_nombre.get()
            nueva_direccion = entry_direccion.get()
            nuevo_telefono = entry_telefono.get()
            nuevo_email = entry_email.get()
            nueva_web = entry_web.get()

            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM empresa") # Eliminar la entrada anterior
                    cursor.execute("INSERT INTO empresa (nombre, direccion, telefono, email, web) VALUES (?, ?, ?, ?, ?)",
                                   (nuevo_nombre, nueva_direccion, nuevo_telefono, nuevo_email, nueva_web))
                    conn.commit()
                    self.cargar_info_empresa() # Recargar el nombre en el label
                    messagebox.showinfo("Éxito", "Información de la empresa actualizada.")
                    ventana_editar.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al guardar la información de la empresa: {e}")

        btn_guardar = tk.Button(ventana_editar, text="Guardar", font="arial 12", command=guardar_cambios)
        btn_guardar.place(x=150, y=300, width=100, height=40)
        btn_cancelar = tk.Button(ventana_editar, text="Cancelar", font="arial 12", command=ventana_editar.destroy)
        btn_cancelar.place(x=260, y=300, width=100, height=40)
        # Cargar los datos actuales para prellenar los campos
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nombre, direccion, telefono, email, web FROM empresa LIMIT 1")
                empresa_actual = cursor.fetchone()
                if empresa_actual:
                    entry_nombre.insert(0, empresa_actual[0])
                    entry_direccion.insert(0, empresa_actual[1] or "")
                    entry_telefono.insert(0, empresa_actual[2] or "")
                    entry_email.insert(0, empresa_actual[3] or "")
                    entry_web.insert(0, empresa_actual[4] or "")
        except sqlite3.Error as e:
            print(f"Error al cargar datos para editar: {e}")


    def mostrar_info_empresa(self):
        """Muestra toda la información de la empresa."""
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT nombre, direccion, telefono, email, web FROM empresa LIMIT 1")
                empresa_info = cursor.fetchone()
                if empresa_info:
                    info_text = f"Nombre: {empresa_info[0]}\nDirección: {empresa_info[1]}\nTeléfono: {empresa_info[2]}\nEmail: {empresa_info[3]}\nWeb: {empresa_info[4]}"
                    messagebox.showinfo("Información de la Empresa", info_text)
                else:
                    messagebox.showinfo("Información de la Empresa", "No hay información de la empresa configurada.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al leer la información de la empresa: {e}")

    def administrar_ventas(self):
        print("Función administrar_ventas llamada")
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT v.factura, a.categoria, v.articulo, v.precio, v.cantidad, v.total, v.fecha, v.hora FROM ventas v INNER JOIN articulos a ON v.articulo = a.articulo")
            ventas = c.fetchall()

            if not ventas:
                messagebox.showinfo("Ventas", "No hay ventas registradas.")
                return

            ventana_ventas = tk.Toplevel(self)
            ventana_ventas.title("Ventas Realizadas")
            ventana_ventas.geometry("1100x650+120+20")
            ventana_ventas.config(bg="#ffb74d")
            ventana_ventas.resizable(False, False)
            ventana_ventas.transient(self.master)
            ventana_ventas.grab_set()
            ventana_ventas.focus_set()
            ventana_ventas.lift()

            label_ventas_realizadas = tk.Label(ventana_ventas, text="Ventas Realizadas", font="sans 26 bold", bg="#ffb74d")
            label_ventas_realizadas.place(x=350, y=20)

            exportbtn = tk.Button(ventana_ventas, text="Exportar a Excel", bg="white", font="arial 12 bold", command=self.exportar_ventas)
            exportbtn.place(x=20, y=80, width=150, height=40)
            btn_cerrar = tk.Button(ventana_ventas, text="Cerrar", bg="white", font="arial 12 bold", command=ventana_ventas.destroy)
            btn_cerrar.place(x=200, y=80, width=150, height=40)

            tree_frame = tk.Frame(ventana_ventas, bg="white")
            tree_frame.place(x=20, y=120, width=1060, height=500)

            scrol_y = ttk.Scrollbar(tree_frame)
            scrol_y.pack(side=RIGHT, fill=Y)

            scrol_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
            scrol_x.pack(side=BOTTOM, fill=X)

            tree = ttk.Treeview(tree_frame, columns=("Factura", "Categoría", "Producto", "Precio", "Cantidad","Total", "Fecha", "Hora"), show="headings")
            tree.pack(expand=True, fill=BOTH)

            scrol_y.config(command=tree.yview)
            scrol_x.config(command=tree.xview)

            tree.heading("Factura", text="Factura")
            tree.heading("Categoría", text="Categoría")
            tree.heading("Producto", text="Producto")
            tree.heading("Precio", text="Precio")
            tree.heading("Cantidad", text="Cantidad")
            tree.heading("Total", text="Total")
            tree.heading("Fecha", text="Fecha")
            tree.heading("Hora", text="Hora")

            tree.column("Factura", width=60, anchor="center")
            tree.column("Categoría", width=120, anchor="center")
            tree.column("Producto", width=120, anchor="center")
            tree.column("Precio", width=80, anchor="center")
            tree.column("Cantidad", width=80, anchor="center")
            tree.column("Total", width=80, anchor="center")
            tree.column("Fecha", width=80, anchor="center")
            tree.column("Hora", width=80, anchor="center")

            for venta in ventas:
                venta = list(venta)
                venta[3] = "{:,.0f}".format(venta[3])
                venta[5] = "{:,.0f}".format(venta[5])
                venta[6] = datetime.datetime.strptime(str(venta[6]), "%Y-%m-%d").strftime("%d-%m-%Y")
                tree.insert("", "end", values=venta)

        except sqlite3.Error as e:
            print("Error al cargar las ventas:", e)
            messagebox.showerror("Error", f"Error al cargar las ventas: {e}")
        finally:
            if conn:
                conn.close()

    def exportar_ventas(self):
        try:
            ruta_destino = r"excel"
            nombre_base = "ventas"
            fecha_hora_actual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"{nombre_base}_{fecha_hora_actual}.csv"
            ruta_completa = os.path.join(ruta_destino, nombre_archivo)

            conn = sqlite3.connect(self.db_name)
            query = "SELECT v.factura, a.categoria, v.articulo, v.precio, v.cantidad, v.total, v.fecha, v.hora FROM ventas v INNER JOIN articulos a ON v.articulo = a.articulo"
            df = pd.read_sql_query(query, conn)
            conn.close()

            df.to_csv(ruta_completa, index=False, encoding='utf-8')
            messagebox.showinfo("Exportar Ventas", f"Ventas exportadas automáticamente a: {ruta_completa}")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al leer los datos de la base de datos: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al exportar a CSV: {e}")
            print(f"Error: {e}")
            
    def administrar_inventario(self):
        print("Función administrar_inventario llamada")
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM articulos")
            articulos = c.fetchall()

            if not articulos:
                messagebox.showinfo("Inventario", "No hay artículos registrados.")
                return

            ventana_inventario = tk.Toplevel(self)
            ventana_inventario.title("Inventario")
            ventana_inventario.geometry("1100x650+120+20")
            ventana_inventario.config(bg="#ffb74d")
            ventana_inventario.resizable(False, False)
            ventana_inventario.transient(self.master)
            ventana_inventario.grab_set()
            ventana_inventario.focus_set()
            ventana_inventario.lift()

            label_inventario = tk.Label(ventana_inventario, text="Inventario", font="sans 26 bold", bg="#ffb74d")
            label_inventario.place(x=350, y=20)

            btnexportar = tk.Button(ventana_inventario, text="Exportar a Excel", bg="white", font="arial 12 bold", command=self.exportar_inventario)
            btnexportar.place(x=20, y=80, width=150, height=40)
            
            btn_cerrar = tk.Button(ventana_inventario, text="Cerrar", bg="white", font="arial 12 bold", command=ventana_inventario.destroy)
            btn_cerrar.place(x=200, y=80, width=150, height=40)
            
            tree_frame = tk.Frame(ventana_inventario, bg="white")
            tree_frame.place(x=20, y=120, width=1060, height=500)
            scrol_y = ttk.Scrollbar(tree_frame)
            scrol_y.pack(side=RIGHT, fill=Y)
            scrol_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
            scrol_x.pack(side=BOTTOM, fill=X)
            tree = ttk.Treeview(tree_frame, columns=("ID", "Categoría", "Artículo", "Precio", "Costo", "Stock", "Estado"), show="headings")
            tree.pack(expand=True, fill=BOTH)
            scrol_y.config(command=tree.yview)
            scrol_x.config(command=tree.xview)
            tree.heading("ID", text="ID")
            tree.heading("Categoría", text="Categoría")
            tree.heading("Artículo", text="Artículo")
            tree.heading("Precio", text="Precio")
            tree.heading("Costo", text="Costo")
            tree.heading("Stock", text="Stock")
            tree.heading("Estado", text="Estado")
            tree.column("ID", width=60, anchor="center")
            tree.column("Categoría", width=120, anchor="center")
            tree.column("Artículo", width=120, anchor="center")
            tree.column("Precio", width=80, anchor="center")
            tree.column("Costo", width=80, anchor="center")
            tree.column("Stock", width=80, anchor="center")
            tree.column("Estado", width=80, anchor="center")
            
            for articulo in articulos:
                articulo = list(articulo)
                articulo[3] = "{:,.0f}".format(articulo[3])
                articulo[4] = "{:,.0f}".format(articulo[4])
                tree.insert("", "end", values=articulo)
        except sqlite3.Error as e:
            print("Error al cargar el inventario:", e)
            messagebox.showerror("Error", f"Error al cargar el inventario: {e}")
        finally:
            if conn:
                conn.close()
                
    def exportar_inventario(self):
        try:
            ruta_destino = r"inve"
            nombre_base = "inventario"
            fecha_hora_actual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"{nombre_base}_{fecha_hora_actual}.csv"
            ruta_completa = os.path.join(ruta_destino, nombre_archivo)

            conn = sqlite3.connect(self.db_name)
            query = "SELECT * FROM articulos"
            df = pd.read_sql_query(query, conn)
            conn.close()

            df.to_csv(ruta_completa, index=False, encoding='utf-8')
            messagebox.showinfo("Exportar Inventario", f"Inventario exportado automáticamente a: {ruta_completa}")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al leer los datos de la base de datos: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al exportar a CSV: {e}")
            print(f"Error: {e}")

    def administrar_categorias(self):
        print("Función administrar_categorias llamada")
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM categorias")
            categorias = c.fetchall()

            if not categorias:
                messagebox.showinfo("Categorías", "No hay categorías registradas.")
                return

            ventana_categorias = tk.Toplevel(self)
            ventana_categorias.title("Categorías")
            ventana_categorias.geometry("1100x650+120+20")
            ventana_categorias.config(bg="#ffb74d")
            ventana_categorias.resizable(False, False)
            ventana_categorias.transient(self.master)
            ventana_categorias.grab_set()
            ventana_categorias.focus_set()
            ventana_categorias.lift()

            label_categorias = tk.Label(ventana_categorias, text="Categorías", font="sans 26 bold", bg="#ffb74d")
            label_categorias.place(x=350, y=20)

            btnexportar = tk.Button(ventana_categorias, text="Exportar a Excel", bg="white", font="arial 12 bold", command=self.exportar_categorias)
            btnexportar.place(x=20, y=80, width=150, height=40)
            
            btn_cerrar = tk.Button(ventana_categorias, text="Cerrar", bg="white", font="arial 12 bold", command=ventana_categorias.destroy)
            btn_cerrar.place(x=200, y=80, width=150, height=40)

            tree_frame = tk.Frame(ventana_categorias, bg="white")
            tree_frame.place(x=20, y=120, width=1060, height=500)
            scrol_y = ttk.Scrollbar(tree_frame)
            scrol_y.pack(side=RIGHT, fill=Y)
            scrol_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
            scrol_x.pack(side=BOTTOM, fill=X)
            tree = ttk.Treeview(tree_frame, columns=("ID", "Categoría","Stock", "Descripcion"), show="headings")
            tree.pack(expand=True, fill=BOTH)
            scrol_y.config(command=tree.yview)
            scrol_x.config(command=tree.xview)
            tree.heading("ID", text="ID")
            tree.heading("Categoría", text="Categoría")
            tree.heading("Stock", text="Stock")
            tree.heading("Descripcion", text="Descripcion")
            tree.column("ID", width=60, anchor="center")
            tree.column("Categoría", width=120, anchor="center")
            tree.column("Stock", width=80, anchor="center")
            tree.column("Descripcion", width=120, anchor="center")
            for categoria in categorias:
                categoria = list(categoria)
                tree.insert("", "end", values=categoria)
        except sqlite3.Error as e:
            print("Error al cargar las categorías:", e)
            messagebox.showerror("Error", f"Error al cargar las categorías: {e}")
        finally:
            if conn:
                conn.close()
    def exportar_categorias(self):
        try:
            ruta_destino = r"cate"
            nombre_base = "categorias"
            fecha_hora_actual = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"{nombre_base}_{fecha_hora_actual}.csv"
            ruta_completa = os.path.join(ruta_destino, nombre_archivo)

            conn = sqlite3.connect(self.db_name)
            query = "SELECT * FROM categorias"
            df = pd.read_sql_query(query, conn)
            conn.close()

            df.to_csv(ruta_completa, index=False, encoding='utf-8')
            messagebox.showinfo("Exportar Categorías", f"Categorías exportadas automáticamente a: {ruta_completa}")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al leer los datos de la base de datos: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al exportar a CSV: {e}")
            print(f"Error: {e}")        
from tkinter import *
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import threading
from tkinter import simpledialog  
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from abstracs import Modulos
import sys
import os

class Ventas(tk.Frame, Modulos):
    db_name = "database.db"

    def __init__(self, padre):
        super().__init__(padre)
        self.numero_factura = self.obtener_numero_factura_actual()
        self.lista_ventas = []  # Lista de productos escaneados
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()
        self.productos_seleccionados = []
        # Inicializar interfaz antes de cargar datos
        self.widgets()
        
    def widgets(self):
        
        frame = tk.Frame(self, bg="#29b6f6")
        frame.place(x=0, y=0, width=1100, height=650)
        
        
        labelframe = tk.LabelFrame(frame, font="sans 16 bold", bg="#29b6f6", text="Ventas", fg="white")
        labelframe.place(x=25, y=30, width=1045, height=180)

        # Campo para escaneo de código de barras
        label_codigo = tk.Label(labelframe, text="Código de Barras", font="sans 14 bold", bg="#29b6f6")
        label_codigo.place(x=90, y=11)

        self.entry_codigo_venta = ttk.Entry(labelframe, font="sans 14 bold")
        self.entry_codigo_venta.place(x=90, y=56, width=260, height=40)

        # Vincular escaneo con la función de agregar productos
        self.entry_codigo_venta.bind("<Return>", self.agregar_articulo)

        # Label de factura
        label_factura = tk.Label(labelframe, text="Factura", font="sans 14 bold", bg="#29b6f6")
        label_factura.place(x=690, y=11)

        self.label_numero_factura = tk.Label(labelframe, text=f"{self.numero_factura}", font="sans 14 bold", bg="#29b6f6")
        self.label_numero_factura.place(x=660, y=11)

        # Botones de gestión de ventas
        boton_agregar = tk.Button(labelframe, text="Agregar producto", font="sans 12 bold", bg="white", command=self.agregar_articulo)
        boton_agregar.place(x=130,y=110, width=200, height=40)

        boton_eliminar = tk.Button(labelframe, text="Eliminar producto", font="sans 12 bold", bg="white", command=self.eliminar_articulo)
        boton_eliminar.place(x=430, y=110, width=200, height=40)

        boton_limpiar = tk.Button(labelframe, text="Cancelar Venta", font="sans 12 bold", bg="white", command=self.cancelar_venta)
        boton_limpiar.place(x=750, y=110, width=200, height=40)

        # Frame para mostrar productos en venta
        treFrame = tk.Frame(self, bg="#b3e5fc")
        treFrame.place(x=70, y=220, width=980, height=300)

        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, 
                                columns=("Factura", "Categoría", "Producto", "Precio", "Cantidad", "Total"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        self.tre.heading("Factura", text="Factura")
        self.tre.heading("Categoría", text="Categoría")
        self.tre.heading("Producto", text="Producto")
        self.tre.heading("Precio", text="Precio")
        self.tre.heading("Cantidad", text="Cantidad")
        self.tre.heading("Total", text="Total")

        self.tre.column("Factura", width=70, anchor="center")
        self.tre.column("Categoría", width=250, anchor="center")
        self.tre.column("Producto", width=250, anchor="center")
        self.tre.column("Precio", width=120, anchor="center")
        self.tre.column("Cantidad", width=120, anchor="center")
        self.tre.column("Total", width=150, anchor="center")

        # Total de la venta
        self.label_precio_total = tk.Label(self, text="Total a pagar: $0.00", font="sans 18 bold", bg="#29b6f6")
        self.label_precio_total.place(x=680, y=550)

        # Botón de pago
        boton_pagar = tk.Button(self, text="Pagar", font="sans 14 bold", bg="white", command=self.realizar_pago)
        boton_pagar.place(x=70, y=550, width=180, height=40)

        boton_ver_ventas = tk.Button(self, text="Ventas realizadas", font="sans 14 bold", bg="white", command=self.ver_ventas_realizadas)
        boton_ver_ventas.place(x=290, y=550, width=250, height=40)
        
    def obtener_numero_factura_actual(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT MAX(factura) FROM ventas")
            last_invoice_number = c.fetchone()[0]
            conn.close()
            return last_invoice_number + 1 if last_invoice_number is not None else 1
        except sqlite3.Error as e:
            print("Error obteniendo el número de factura actual:", e)
            return 1
    def cargar_producto(self):
        try:
            conn =sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT articulo FROM articulos")
            self.products= [product[0]for product in c.fetchall()]
            self.entry_producto["values"]= self.products
            conn.close()
        except sqlite3.Error as e:
            print("Error cargando productos",e)
    
    def cargar_categorias(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT categoria FROM categorias")  # Consulta para obtener las categorías
            self.categories = [row[0] for row in c.fetchall()]  # Crear lista de categorías
            self.entry_categoria["values"] = self.categories  # Asignar categorías al Combobox
            conn.close()
        except sqlite3.Error as e:
            print("Error cargando categorías:", e)

    
    def actualizar_lista_ventas(self):
        # Limpiar lista antes de actualizar
        for widget in self.tre.get_children():
            self.tre.delete(widget)

        total = 0

        # Mostrar productos en la tabla de ventas
        for producto in self.lista_ventas:
            self.tre.insert("", "end", values=(
                producto["factura"], producto["categoria"], producto["articulo"],
                f"${producto['precio']:.2f}", producto["cantidad"],
                f"${producto['precio'] * producto['cantidad']:.2f}"
            ))
            total += producto["precio"] * producto["cantidad"]

        # Mostrar total en la interfaz
        self.label_precio_total.config(text=f"Total a pagar: ${total:.2f}")
    def agregar_articulo(self):
        codigo_barras = self.entry_codigo_venta.get().strip()

        if not codigo_barras:
            messagebox.showerror("Error", "Escanea un código válido.")
            return

        try:
            self.cur.execute("""
                SELECT id, articulo, precio, stock, categoria
                FROM articulos
                WHERE id IN (SELECT producto_id FROM inventario WHERE codigo_barras = ?) AND stock > 0
                LIMIT 1
            """, (codigo_barras,))

            resultado = self.cur.fetchone()

            if not resultado:
                messagebox.showerror("Error", f"No hay unidades disponibles para el código '{codigo_barras}'.")
                self.entry_codigo_venta.delete(0, tk.END)
                self.entry_codigo_venta.focus()
                return

            articulo_id, articulo_nombre, precio, stock, categoria = resultado

            # Agregar producto con su ID único a la lista de ventas
            self.lista_ventas.append({
                "factura": self.numero_factura,
                "categoria": categoria,
                "articulo": articulo_nombre,
                "precio": precio,
                "cantidad": 1,
                "codigo_barras": codigo_barras,
                "articulo_id": articulo_id  # Asegúrate de tener esto
            })

            # Reducir stock del artículo específico en la base de datos
            self.cur.execute("UPDATE articulos SET stock = stock - 1 WHERE id = ?", (articulo_id,))
            self.con.commit()

            # Limpiar Entry después de agregar el producto
            self.entry_codigo_venta.delete(0, tk.END)
            self.entry_codigo_venta.focus()

            # Actualizar la lista de ventas en la interfaz
            self.actualizar_lista_ventas()

        except sqlite3.Error as e:
            print(f"Error en venta: {e}")
            messagebox.showerror("Error", "Hubo un problema al procesar la venta.")
            self.con.rollback()
    def calcular_precio_total(self):
        total_pagar = 0.0
        for item in self.tre.get_children():
            try:
                valor_total_str = self.tre.item(item)["values"][-1]
                # Eliminar el símbolo '$' y la coma, luego intentar convertir a float
                valor_total_limpio = valor_total_str.replace("$", "").replace(",", "").replace(" ", "")
                total_pagar += float(valor_total_limpio)
            except ValueError as e:
                print(f"Error al convertir el valor total: {e}, valor original: {self.tre.item(item)['values'][-1]}")
                # Aquí podrías decidir cómo manejar el error, por ejemplo, omitir este ítem o mostrar un mensaje.

        total_pagar_cop = "{:,.2f}".format(total_pagar)  # Formatear con dos decimales
        self.label_precio_total.config(text=f"Total a pagar: ${total_pagar_cop}")
    def actualizar_stock(self, event=None):
        producto_seleccionado=self.entry_producto.get()
        
        try:
            conn=sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT stock FROM articulos WHERE articulo=?", (producto_seleccionado,))
            stock= c.fetchone()[0]
            conn.close()

            self.label_stock.config(text=f"Stock: {stock}")

        except sqlite3.Error as e:
            print("Error al obtener el stock del producto: ", e)
        
    def realizar_pago(self):
        if not self.lista_ventas:
            messagebox.showerror("Error", "No hay productos seleccionados para realizar el pago.")
            return

        # Recalcular el total de la venta justo antes de abrir la ventana de pago
        total_venta = sum(producto["precio"] * producto["cantidad"] for producto in self.lista_ventas)
        total_formateado = "{:,.0f}".format(total_venta)

        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Realizar Pago")
        ventana_pago.geometry("400x400+450+80")
        ventana_pago.config(bg="#29b6f6")
        ventana_pago.resizable(False, False)

        tk.Label(ventana_pago, text="Realizar Pago", font="sans 30 bold", bg="#29b6f6").place(x=70, y=10)
        tk.Label(ventana_pago, text=f"Total a pagar: ${total_formateado}", font="sans 14 bold", bg="#29b6f6").place(x=80, y=100)

        entry_monto = ttk.Entry(ventana_pago, font="sans 14 bold")
        entry_monto.place(x=80, y=210, width=240, height=40)

        tk.Button(ventana_pago, text="Confirmar Pago", font="sans 14 bold",
                  command=lambda: self.procesar_pago(entry_monto.get(), ventana_pago, total_venta)).place(x=80, y=270, width=240, height=40)
        
    def procesar_pago(self, cantidad_pagada, ventana_pago, total_venta):
        try:
            cantidad_pagada = float(cantidad_pagada)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un monto válido.")
            return

        if cantidad_pagada < total_venta:
            messagebox.showerror("Error", "La cantidad pagada es insuficiente.")
            return

        cambio = cantidad_pagada - total_venta
        messagebox.showinfo("Pago realizado", f"Total: ${total_venta:,.2f}\nCambio: ${cambio:,.2f}")

        try:
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

            self.con.execute("BEGIN TRANSACTION")

            for producto in self.lista_ventas:
                self.cur.execute(
                    "INSERT INTO ventas (factura, articulo, precio, cantidad, total, fecha, hora) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (self.numero_factura, producto["articulo"], producto["precio"], producto["cantidad"],
                     producto["precio"] * producto["cantidad"], fecha_actual, hora_actual)
                )

            self.con.commit()
            self.generar_factura_pdf(total_venta)

            self.numero_factura += 1

            self.lista_ventas.clear()
            self.tre.delete(*self.tre.get_children())
            self.label_precio_total.config(text="Total a pagar: $0.00")
            ventana_pago.destroy()

        except sqlite3.Error as e:
            self.con.rollback()
            messagebox.showerror("Error", f"Error al registrar la venta: {e}")
    def limpiar_campos(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
        self.label_precio_total.config(text="Precio a pagar: $ 0.00")

        self.entry_producto.set('')
        self.entry_cantidad.delete(0,'end')

    def limpiar_lista(self):
        self.tre.delete(*self.tre.get_children())  # Corregido: se llama correctamente a get_children()
        self.productos_seleccionados.clear()
        self.calcular_precio_total()
    
    def eliminar_articulo(self):
        item_seleccionado = self.tre.selection()
        if not item_seleccionado:
            messagebox.showerror("Error", "No hay ningún artículo seleccionado.")
            return

        item_id_treeview = item_seleccionado[0]
        valores_item = self.tre.item(item_id_treeview)["values"]
        articulo_nombre = valores_item[2]
        cantidad_eliminada = valores_item[4]

        # Encuentra el primer artículo en self.lista_ventas con el mismo nombre
        for index, item in enumerate(self.lista_ventas):
            if item["articulo"] == articulo_nombre:
                articulo_id_db = item.get("articulo_id")
                codigo_barras = item.get("codigo_barras")

                try:
                    conn = sqlite3.connect(self.db_name)
                    cur = conn.cursor()
                    cur.execute("UPDATE articulos SET stock = stock + ? WHERE id = ?", (cantidad_eliminada, articulo_id_db))
                    conn.commit()
                    conn.close()

                    # Eliminar SOLO este artículo de self.lista_ventas
                    del self.lista_ventas[index]
                    self.tre.delete(item_id_treeview)
                    self.actualizar_lista_ventas()
                    return  # Importante: salir después de eliminar el primer coincidente

                except sqlite3.Error as e:
                    print(f"Error al revertir el stock: {e}")
                    messagebox.showerror("Error", "Hubo un problema al revertir el stock.")
                    conn.rollback()
                break  # Salir del bucle después de intentar eliminar

        messagebox.showerror("Error", "No se encontró el artículo en la lista de ventas para eliminar.")
        
    def cancelar_venta(self):
        print("Cancelando venta...")
        if not self.lista_ventas:
            messagebox.showinfo("Cancelación", "No hay productos en la lista de ventas.")
            return
        
        self.lista_ventas.clear()
        self.actualizar_lista_ventas()

        messagebox.showinfo("Venta cancelada", "Todos los productos han sido eliminados.")

    def ver_ventas_realizadas(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT v.factura, a.categoria, v.articulo, v.precio, v.cantidad, v.total, v.fecha, v.hora FROM ventas v INNER JOIN articulos a ON v.articulo = a.articulo")
            ventas = c.fetchall()
            
            
            c.execute("SELECT categoria FROM categorias")
            categorias = sorted([row[0] for row in c.fetchall()])
            
            
            if not ventas:
                messagebox.showinfo("Ventas", "No hay ventas registradas.")
                return

            ventana_ventas = tk.Toplevel(self)
            ventana_ventas.title("Ventas Realizadas")
            ventana_ventas.geometry("1100x650+120+20")
            ventana_ventas.config(bg="#29b6f6")
            ventana_ventas.resizable(False, False)
            ventana_ventas.transient(self.master)
            ventana_ventas.grab_set()
            ventana_ventas.focus_set()
            ventana_ventas.lift()
            
            def filtrar_ventas():
                factura_a_buscar = entry_factura.get()
                categoria_a_buscar = entry_categoria.get()
                for item in tree.get_children():
                    tree.delete(item)
                ventas_filtradas = [
                    venta for venta in ventas
                    if (str(venta[0]) == factura_a_buscar or not factura_a_buscar) and
                    (venta[1].lower() == categoria_a_buscar.lower() or not categoria_a_buscar)
                ]    
                for venta in ventas_filtradas:
                    venta = list(venta)
                    venta[3] = "{:,.0f}".format(venta[3])
                    venta[5] = "{:,.0f}".format(venta[5])
                    venta[6] = datetime.datetime.strptime(str(venta[6]), "%Y-%m-%d").strftime("%d-%m-%Y")
                    tree.insert("", "end", values=venta)
                    
            label_ventas_realizadas = tk.Label(ventana_ventas, text="Ventas Realizadas", font="sans 26 bold", bg="#29b6f6")
            label_ventas_realizadas.place(x=350, y=20)
            
            filtro_frame = tk.Frame(ventana_ventas, bg="#29b6f6")
            filtro_frame.place(x=20, y=60, width=1060, height=60)  
            
            label_factura = tk.Label(filtro_frame, text="Factura:", font="sans 14 bold", bg="#29b6f6")
            label_factura.place(x=10, y=15)
            
            entry_factura = ttk.Entry(filtro_frame, font="sans 14 bold")
            entry_factura.place(x=200, y=10, width=200, height=40)
            
            label_categoria = tk.Label(filtro_frame, text="Categoría:", font="sans 14 bold", bg="#29b6f6")
            label_categoria.place(x=420, y=15)
            
            entry_categoria = ttk.Combobox(filtro_frame, font="sans 14 bold", values=categorias)
            entry_categoria.place(x=620, y=10, width=200, height=40)
            
            btn_filtrar = tk.Button(filtro_frame, text="Filtrar", font="sans 14 bold", bg="white", command=filtrar_ventas)  
            btn_filtrar.place(x=840, y=10, width=200, height=40)   
            
            tree_frame = tk.Frame(ventana_ventas, bg="white")
            tree_frame.place(x=20, y=130, width=1060, height=500)
            
            scrol_y = ttk.Scrollbar(tree_frame)
            scrol_y.pack(side=RIGHT, fill=Y)
            
            scrol_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
            scrol_x.pack(side=BOTTOM, fill=X)
            
            tree = ttk.Treeview(tree_frame, columns=("Factura", "Categoría", "Producto", "Precio", "Cantidad", "Total", "Fecha", "Hora"), show="headings")
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
                
    def generar_factura_pdf(self, total_venta):
        try:
            factura_path = f"facturas/Factura_{self.numero_factura}.pdf"
            c = canvas.Canvas(factura_path, pagesize=letter)

            # Obtener la información de la empresa desde la base de datos
            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT nombre, direccion, telefono, email, web FROM empresa LIMIT 1")
                    empresa_data = cursor.fetchone()
                    empresa_nombre = empresa_data[0] if empresa_data and len(empresa_data) > 0 else "Nombre de la Empresa"
                    empresa_direccion = empresa_data[1] if empresa_data and len(empresa_data) > 1 else "Dirección no configurada"
                    empresa_telefono = empresa_data[2] if empresa_data and len(empresa_data) > 2 else "Teléfono no configurado"
                    empresa_email = empresa_data[3] if empresa_data and len(empresa_data) > 3 else "Email no configurado"
                    empresa_web = empresa_data[4] if empresa_data and len(empresa_data) > 4 else "Web no configurada"
            except sqlite3.Error as e:
                empresa_nombre = "Error al cargar el nombre"
                empresa_direccion = "Error al cargar la dirección"
                empresa_telefono = "Error al cargar el teléfono"
                empresa_email = "Error al cargar el email"
                empresa_web = "Error al cargar la web"
                print(f"Error al obtener información de la empresa para la factura: {e}")

            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(colors.black)
            c.drawCentredString(300, 750, "FACTURA")

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 710, empresa_nombre)

            c.setFont("Helvetica", 12)
            c.drawString(50, 690, f"Dirección: {empresa_direccion}")
            c.drawString(50, 670, f"Teléfono: {empresa_telefono}")
            c.drawString(50, 650, f"Email: {empresa_email}")
            c.drawString(50, 630, f"Web: {empresa_web}")

            c.line(50, 620, 550, 620)

            c.setFont("Helvetica", 12)
            c.drawString(50, 600, f"Factura: {self.numero_factura}")
            c.drawString(50, 580, f"Fecha: {datetime.datetime.now().strftime('%d-%m-%Y, %H:%M:%S')}")

            c.line(50, 560, 550, 560)
            c.drawString(50, 520, "Descripción:")

            y_offset = 500
            c.setFont("Helvetica", 12)
            c.drawString(70, y_offset, "Producto")
            c.drawString(270, y_offset, "Cantidad")
            c.drawString(370, y_offset, "Precio")
            c.drawString(470, y_offset, "Total")

            c.line(50, y_offset - 10, 550, y_offset - 10)
            y_offset -= 20
            c.setFont("Helvetica", 12)

            for item in self.lista_ventas:
                producto = item["articulo"]
                cantidad = item["cantidad"]
                precio = item["precio"]
                total = item["precio"] * item["cantidad"]

                c.drawString(70, y_offset, producto)
                c.drawString(270, y_offset, str(cantidad))
                c.drawString(370, y_offset, f"${precio:,.2f}")
                c.drawString(470, y_offset, f"${total:,.2f}")
                y_offset -= 20

            c.line(50, y_offset, 550, y_offset)
            y_offset -= 20

            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.black)

            total_venta = float(total_venta)
            c.drawString(50, y_offset, f"Total: ${total_venta:,.2f}")

            y_offset -= 20
            c.line(50, y_offset, 550, y_offset)

            c.setFont("Helvetica", 16)
            c.drawString(150, y_offset - 60, "Gracias por su compra")

            y_offset -= 100
            c.setFont("Helvetica", 12)
            c.drawString(50, y_offset, "Términos y condiciones:")
            c.drawString(50, y_offset - 20, "1. No se aceptan devoluciones.")
            c.drawString(50, y_offset - 40, "2. No se aceptan cambios.")
            c.drawString(50, y_offset - 60, "3. No se aceptan reembolsos.")

            c.save()
            messagebox.showinfo("Factura generada", f"Factura guardada en: {factura_path}")
            os.startfile(os.path.abspath(factura_path))

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar la factura: {e}")
import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

class Proveedor(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.lista_proveedores = []
        self.con = sqlite3.connect("database.db")
        self.cur = self.con.cursor()
        self.gmail_servidor = "smtp.gmail.com"
        self.gmail_puerto = 465
        self.gmail_usuario = "darau2746@gmail.com"  
        self.gmail_contrasena = "urzm djun suek htmz" 
        self.widgets()
        self.cargar_proveedores()

    def widgets(self):
        
        frame = tk.Frame(self, bg="#ba68c8")
        frame.place(x=0, y=0, width=1100, height=650)
        
        labelframetree = tk.LabelFrame(self, text="Proveedores", font="Arial 14 bold", bg="#ba68c8")
        labelframetree.place(x=300, y=10, width=780, height=580)

        scroly= ttk.Scrollbar(labelframetree)
        scroly.pack(side=RIGHT, fill=Y)

        scrolx = ttk.Scrollbar(labelframetree, orient=HORIZONTAL)
        scrolx.pack(side=BOTTOM, fill=X)

        self.treeproveedores = ttk.Treeview(labelframetree, yscrollcommand=scroly.set, xscrollcommand=scrolx.set, height=40,
                                            columns=("ID", "Nombre", "Telefono", "Email", "Fecha"), show="headings")
        self.treeproveedores.pack(expand=True, fill=BOTH)

        scrolx.config(command=self.treeproveedores.xview)
        scroly.config(command=self.treeproveedores.yview)

        self.treeproveedores.heading("ID", text="ID")
        self.treeproveedores.heading("Nombre", text="Nombre")
        self.treeproveedores.heading("Telefono", text="Telefono")
        self.treeproveedores.heading("Email", text="Email")
        self.treeproveedores.heading("Fecha", text="Fecha")

        self.treeproveedores.column("ID", width=50, anchor="center")
        self.treeproveedores.column("Nombre", width=200, anchor="center")
        self.treeproveedores.column("Telefono", width=100, anchor="center")
        self.treeproveedores.column("Email", width=200, anchor="center")
        self.treeproveedores.column("Fecha", width=100, anchor="center")

        lableframellenar = tk.LabelFrame(self, text="Llenar Datos", font="Arial 14 bold", bg="#ba68c8")
        lableframellenar.place(x=10, y=10, width=280, height=580)

        tk.Label(lableframellenar, text="Nombre", font="arial 12 bold", bg="#ba68c8").place(x=10, y=10)
        self.entry_nombre = ttk.Entry(lableframellenar, font="arial 12 bold")
        self.entry_nombre.place(x=10, y=40, width=250, height=40)

        tk.Label(lableframellenar, text="Numero", font="arial 12 bold", bg="#ba68c8").place(x=10, y=80)
        self.entry_numero = ttk.Entry(lableframellenar, font="arial 12 bold")
        self.entry_numero.place(x=10, y=110, width=250, height=40)

        tk.Label(lableframellenar, text="Email", font="arial 12 bold", bg="#ba68c8").place(x=10, y=150)
        self.entry_email = ttk.Entry(lableframellenar, font="arial 12 bold")
        self.entry_email.place(x=10, y=180, width=250, height=40)

        tk.Label(lableframellenar, text="Fecha", font="arial 12 bold", bg="#ba68c8").place(x=10, y=220)
        self.entry_fecha = ttk.Entry(lableframellenar, font="arial 12 bold")
        self.entry_fecha.place(x=10, y=250, width=250, height=40)
        self.entry_fecha.insert(0, "dd/mm/aaaa")
        self.entry_fecha.bind("<FocusIn>", lambda e: self.entry_fecha.delete(0, tk.END))
        self.entry_fecha.bind("<FocusOut>", lambda e: self.entry_fecha.insert(0, "dd/mm/aaaa") if self.entry_fecha.get() == "" else None)

        btn_agregar = tk.Button(lableframellenar, text="Agregar", font="arial 12 bold", bg="white", command=self.agregar_proveedor)
        btn_agregar.place(x=10, y=350, width=250, height=40)

        btn_editar = tk.Button(lableframellenar, text="Editar", font="arial 12 bold", bg="white", command=self.editar_proveedor)
        btn_editar.place(x=10, y=400, width=250, height=40)

        btn_eliminar = tk.Button(lableframellenar, text="Eliminar", font="arial 12 bold", bg="white", command=self.eliminar_proveedor)
        btn_eliminar.place(x=10, y=450, width=250, height=40)

        btn_notificar = tk.Button(lableframellenar, text="Notificar", font="arial 12 bold", bg="white", command=self.notificar_proveedor)
        btn_notificar.place(x=10, y=500, width=250, height=40)

    def cargar_proveedores(self):
        try:
            self.cur.execute("SELECT id, nombre, telefono, email, fecha FROM proveedores")
            proveedores = self.cur.fetchall()
            self.actualizar_lista_proveedores_desde_db(proveedores)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar proveedores: {e}")

    def actualizar_lista_proveedores_desde_db(self, proveedores):
        for widget in self.treeproveedores.get_children():
            self.treeproveedores.delete(widget)

        for proveedor in proveedores:
            self.treeproveedores.insert("", "end", values=(proveedor[0], proveedor[1], proveedor[2], proveedor[3], proveedor[4]))

    def agregar_proveedor(self):
        nombre = self.entry_nombre.get()
        numero = self.entry_numero.get()
        email = self.entry_email.get()
        fecha = self.entry_fecha.get()

        if not nombre or not numero or not email or not fecha:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            self.cur.execute("INSERT INTO proveedores (nombre, telefono, email, fecha) VALUES (?, ?, ?, ?)", (nombre, numero, email, fecha))
            self.con.commit()
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente")
            self.cargar_proveedores()
            self.entry_nombre.delete(0, tk.END)
            self.entry_numero.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, "dd/mm/aaaa") 
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al agregar proveedor: {e}")

    def editar_proveedor(self):
        selected_item = self.treeproveedores.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un proveedor para editar")
            return

        item_values = self.treeproveedores.item(selected_item, "values")
        id_proveedor = item_values[0]

        nombre = self.entry_nombre.get()
        numero = self.entry_numero.get()
        email = self.entry_email.get()
        fecha = self.entry_fecha.get()

        if not nombre or not numero or not email or not fecha:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        try:
            self.cur.execute("UPDATE proveedores SET nombre=?, telefono=?, email=?, fecha=? WHERE id=?", (nombre, numero, email, fecha, id_proveedor))
            self.con.commit()
            messagebox.showinfo("Éxito", "Proveedor editado correctamente")
            self.cargar_proveedores()
            self.entry_nombre.delete(0, tk.END)
            self.entry_numero.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            self.entry_fecha.delete(0, tk.END)
            self.entry_fecha.insert(0, "dd/mm/aaaa")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al editar proveedor: {e}")
            
    def eliminar_proveedor(self):
        selected_item = self.treeproveedores.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un proveedor para eliminar")
            return

        item_values = self.treeproveedores.item(selected_item, "values")
        id_proveedor = item_values[0]

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este proveedor?"):
            try:
                self.cur.execute("DELETE FROM proveedores WHERE id=?", (id_proveedor,))
                self.con.commit()
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
                self.cargar_proveedores()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al eliminar proveedor: {e}")

    def notificar_proveedor(self):
        selected_item = self.treeproveedores.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un proveedor para notificar")
            return

        item_values = self.treeproveedores.item(selected_item, "values")
        id_proveedor = item_values[0]

        try:
            self.cur.execute("SELECT nombre, email FROM proveedores WHERE id=?", (id_proveedor,))
            proveedor_info = self.cur.fetchone()
            if proveedor_info:
                nombre_proveedor = proveedor_info[0]
                email_proveedor = proveedor_info[1]
                self.abrir_ventana_mensaje(nombre_proveedor, email_proveedor)
            else:
                messagebox.showerror("Error", "No se encontró información del proveedor")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener información del proveedor: {e}")
        finally:
            if hasattr(self, 'con') and self.con:
                pass

    def abrir_ventana_mensaje(self, nombre_proveedor, email_proveedor):
        top = Toplevel(self.master)
        top.title(f"Enviar Notificación a {nombre_proveedor}")
        top.geometry("700x400+200+50") 
        top.config(bg="#ba68c8")
        top.resizable(False, False)

        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        label_mensaje = tk.Label(top, text="Escriba su mensaje:", bg="#ba68c8", font="Arial 12 bold")
        label_mensaje.pack(pady=5)

        text_mensaje = Text(top, height=15, width=70)
        text_mensaje.insert(END, f"Hola {nombre_proveedor}, nos gustaria hacer un pedido de mercancia para la proxima vez que nos visite.\n\n")
        text_mensaje.pack(padx=10, pady=5)

        self.archivos_adjuntos = [] 

        def seleccionar_archivo():
            from tkinter import filedialog
            ruta_archivo = filedialog.askopenfilename(
                title="Seleccionar archivo a adjuntar",
                filetypes=(("Todos los archivos", "*.*"),)
            )
            if ruta_archivo:
                self.archivos_adjuntos.append(ruta_archivo)
                print(f"Archivo adjuntado: {ruta_archivo}") 

        

        def enviar_correo():
            cuerpo = text_mensaje.get("1.0", END).strip()
            if not cuerpo and not self.archivos_adjuntos:
                messagebox.showerror("Error", "El mensaje no puede estar vacío si no hay archivos adjuntos.") # Mejorar mensaje
                return

            remitente = self.gmail_usuario
            destinatario = email_proveedor
            asunto = "Notificación Importante"

            msg = MIMEMultipart() 
            msg['Subject'] = asunto
            msg['From'] = remitente
            msg['To'] = destinatario
            msg.attach(MIMEText(cuerpo)) 

            for ruta_archivo in self.archivos_adjuntos:
                try:
                    with open(ruta_archivo, "rb") as archivo:
                        parte = MIMEBase("application", "octet-stream")
                        parte.set_payload(archivo.read())
                    encoders.encode_base64(parte)
                    parte.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(ruta_archivo)}"')
                    msg.attach(parte)
                except FileNotFoundError:
                    messagebox.showerror("Error", f"No se pudo encontrar el archivo: {ruta_archivo}")
                    return
                except Exception as e:
                    messagebox.showerror("Error", f"Error al adjuntar el archivo {os.path.basename(ruta_archivo)}: {e}")
                    return

            try:
                with smtplib.SMTP_SSL(self.gmail_servidor, self.gmail_puerto) as server:
                    server.login(self.gmail_usuario, self.gmail_contrasena)
                    server.sendmail(remitente, [destinatario], msg.as_string())
                messagebox.showinfo("Notificación", f"Correo electrónico enviado a {nombre_proveedor} con {len(self.archivos_adjuntos)} archivo(s) adjunto(s) a través de Gmail")
                top.destroy()
            except smtplib.SMTPAuthenticationError as e:
                messagebox.showerror("Error al enviar correo electrónico", f"Error de autenticación (Gmail): {e}")
            except smtplib.SMTPConnectError as e:
                messagebox.showerror("Error al enviar correo electrónico", f"Error al conectar a Gmail: {e}")
            except Exception as e:
                messagebox.showerror("Error al enviar correo electrónico", f"Otro error: {e}")

        boton_enviar = Button(top, text="Enviar", font="arial 12 bold", command=enviar_correo)
        boton_enviar.place(x=90, y=290, width=150, height=40) 
        boton_adjuntar = Button(top, text="Adjuntar", font="arial 12 bold", command=seleccionar_archivo)
        boton_adjuntar.place(x=260, y=290, width=150, height=40)
        boton_cerrar = Button(top, text="Cerrar",font="arial 12 bold", command=top.destroy)
        boton_cerrar.place(x=430, y=290, width=150, height=40) 
        top.transient(self.master)
        top.grab_set()
        self.master.wait_window(top)
        
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Gestión de Proveedores")
    root.geometry("1100x600+100+50")
    root.config(bg="#f0f0f0")
    app = Proveedor(root)
    app.pack(expand=True, fill=BOTH)
    root.mainloop()
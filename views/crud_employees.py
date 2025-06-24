import customtkinter as ctk
from tkinter import messagebox
from controllers import employee_controller
from models.employee import Empleado

class CrudEmpleados(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.controller = employee_controller
        self.title("CRUD Empleados")
        self.geometry("600x700")
        

        ctk.CTkLabel(self, text="Gestión de Empleados", font=("Arial", 18)).pack(pady=20)
        ctk.CTkButton(self, text="Volver al menú principal", command=lambda: self.volver_menu(username, rol)).pack(pady=10)

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=580, height=500)
        self.scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        campos = [
            ("nombre", "Nombre"),
            ("apellido", "Apellido"),
            ("tipo_doc.", "Tipo Doc."),
            ("n°_doc.", "N° Doc."),
            ("expedición", "Expedición"),
            ("nacimiento", "Nacimiento"),
            ("teléfono", "Teléfono"),
            ("dirección", "Dirección"),
            ("rut", "RUT"),
            ("email", "Email"),
            ("cargo", "Cargo")
        ]
        self.entries = {}
        for key, label in campos:
            ctk.CTkLabel(self.scroll_frame, text=label).pack(pady=2)
            entry = ctk.CTkEntry(self.scroll_frame, width=400)
            entry.pack(pady=3)
            self.entries[key] = entry

        ctk.CTkButton(self.scroll_frame, text="Guardar", command=self.guardar).pack(pady=5)
        ctk.CTkButton(self.scroll_frame, text="Actualizar", command=self.actualizar).pack(pady=5)
        ctk.CTkButton(self.scroll_frame, text="Eliminar", command=self.eliminar).pack(pady=5)
        ctk.CTkButton(self.scroll_frame, text="Limpiar", command=self.limpiar).pack(pady=5)

        self.lista = ctk.CTkOptionMenu(self.scroll_frame, values=[], command=self.cargar_empleado)
        self.lista.pack(pady=10)

        self.selected_id = None
        self.cargar_lista()

    def cargar_lista(self):
        empleados = self.controller.listar_empleados()
        self.empleados = {f"{e.name} {e.last_name} ({e.document_number})": e.id for e in empleados}
        if self.empleados:
            self.lista.configure(values=list(self.empleados.keys()))
            self.lista.set(list(self.empleados.keys())[0])
            self.cargar_empleado(list(self.empleados.keys())[0])
        else:
            self.lista.configure(values=["(sin empleados)"])
            self.lista.set("(sin empleados)")

    def cargar_empleado(self, seleccion):
        emp_id = self.empleados.get(seleccion)
        if not emp_id:
            return
        datos = self.controller.consultar_empleado(emp_id)
        if not datos:
            return

        self.entries["nombre"].delete(0, 'end')
        self.entries["nombre"].insert(0, datos.name)
        self.entries["apellido"].delete(0, 'end')
        self.entries["apellido"].insert(0, datos.last_name)
        self.entries["tipo_doc."].delete(0, 'end')
        self.entries["tipo_doc."].insert(0, datos.document_type)
        self.entries["n°_doc."].delete(0, 'end')
        self.entries["n°_doc."].insert(0, datos.document_number)
        self.entries["expedición"].delete(0, 'end')
        self.entries["expedición"].insert(0, datos.document_issuance)
        self.entries["nacimiento"].delete(0, 'end')
        self.entries["nacimiento"].insert(0, datos.birthdate)
        self.entries["teléfono"].delete(0, 'end')
        self.entries["teléfono"].insert(0, datos.phone_number)
        self.entries["dirección"].delete(0, 'end')
        self.entries["dirección"].insert(0, datos.residence_address)
        self.entries["rut"].delete(0, 'end')
        self.entries["rut"].insert(0, datos.RUT)
        self.entries["email"].delete(0, 'end')
        self.entries["email"].insert(0, datos.email)
        self.entries["cargo"].delete(0, 'end')
        self.entries["cargo"].insert(0, datos.position)

        self.selected_id = emp_id

    def guardar(self):
        datos = Empleado(
            name=self.entries["nombre"].get(),
            last_name=self.entries["apellido"].get(),
            document_type=self.entries["tipo_doc."].get(),
            document_number=self.entries["n°_doc."].get(),
            document_issuance=self.entries["expedición"].get(),
            birthdate=self.entries["nacimiento"].get(),
            phone_number=self.entries["teléfono"].get(),
            residence_address=self.entries["dirección"].get(),
            RUT=self.entries["rut"].get(),
            email=self.entries["email"].get(),
            position=self.entries["cargo"].get()
        )
        try:
            self.controller.registrar_empleado(datos)
            messagebox.showinfo("Éxito", "Empleado registrado.")
            self.limpiar()
            self.cargar_lista()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        if not self.selected_id:
            messagebox.showwarning("Selecciona", "Selecciona un empleado primero.")
            return
        datos = Empleado(
            name=self.entries["nombre"].get(),
            last_name=self.entries["apellido"].get(),
            document_type=self.entries["tipo_doc."].get(),
            document_number=self.entries["n°_doc."].get(),
            document_issuance=self.entries["expedición"].get(),
            birthdate=self.entries["nacimiento"].get(),
            phone_number=self.entries["teléfono"].get(),
            residence_address=self.entries["dirección"].get(),
            RUT=self.entries["rut"].get(),
            email=self.entries["email"].get(),
            position=self.entries["cargo"].get()
        )
        self.controller.actualizar_empleado(self.selected_id, datos)
        messagebox.showinfo("Actualizado", "Datos actualizados.")
        self.cargar_lista()

    def eliminar(self):
        if not self.selected_id:
            messagebox.showwarning("Selecciona", "Selecciona un empleado primero.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este empleado?"):
            self.controller.eliminar_empleado(self.selected_id)
            messagebox.showinfo("Eliminado", "Empleado eliminado.")
            self.limpiar()
            self.cargar_lista()

    def limpiar(self):
        for campo in self.entries.values():
            campo.delete(0, 'end')
        self.selected_id = None

    def volver_menu(self, username, rol):
        self.destroy()
        from views.main_menu import MainMenu
        MainMenu(username, rol).deiconify()
import customtkinter as ctk
from tkinter import messagebox
from bd.employees import crear_empleado, obtener_empleados, obtener_empleado_por_id, actualizar_empleado, eliminar_empleado

class CrudEmpleados(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CRUD Empleados")
        self.geometry("600x600")
        self.selected_id = None

        # Contenedor scrollable
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=580, height=550)
        self.scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Entradas de texto
        campos = [
            "Nombre", "Apellido", "Tipo Doc.", "N° Doc.", "Expedición", "Nacimiento",
            "Teléfono", "Dirección", "RUT", "Email", "Cargo"
        ]
        self.entries = {}
        for campo in campos:
            label = ctk.CTkLabel(self.scroll_frame, text=campo)
            label.pack(pady=2)
            entry = ctk.CTkEntry(self.scroll_frame, width=400)
            entry.pack(pady=3)
            self.entries[campo.lower().replace(" ", "_")] = entry

        # Botones
        ctk.CTkButton(self.scroll_frame, text="Guardar", command=self.guardar).pack(pady=5)
        ctk.CTkButton(self.scroll_frame, text="Actualizar", command=self.actualizar).pack(pady=5)
        ctk.CTkButton(self.scroll_frame, text="Eliminar", command=self.eliminar).pack(pady=5)
        ctk.CTkButton(self.scroll_frame, text="Limpiar", command=self.limpiar).pack(pady=5)

        # Lista de empleados
        self.lista = ctk.CTkOptionMenu(self.scroll_frame, values=[], command=self.cargar_empleado)
        self.lista.pack(pady=10)
        self.cargar_lista()

    def cargar_lista(self):
        empleados = obtener_empleados()
        self.empleados = {f"{e[1]} {e[2]} ({e[3]})": e[0] for e in empleados}
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
        datos = obtener_empleado_por_id(emp_id)
        campos = list(self.entries.keys())
        for i, campo in enumerate(campos):
            self.entries[campo].delete(0, 'end')
            self.entries[campo].insert(0, str(datos[i + 1]))  # +1 porque el índice 0 es el ID
        self.selected_id = emp_id

    def guardar(self):
        datos = tuple(self.entries[c].get() for c in self.entries)
        try:
            crear_empleado(datos)
            messagebox.showinfo("Éxito", "Empleado registrado.")
            self.limpiar()
            self.cargar_lista()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        if not self.selected_id:
            messagebox.showwarning("Selecciona", "Selecciona un empleado primero.")
            return
        datos = tuple(self.entries[c].get() for c in self.entries)
        actualizar_empleado(self.selected_id, datos)
        messagebox.showinfo("Actualizado", "Datos actualizados.")
        self.cargar_lista()

    def eliminar(self):
        if not self.selected_id:
            messagebox.showwarning("Selecciona", "Selecciona un empleado primero.")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este empleado?"):
            eliminar_empleado(self.selected_id)
            messagebox.showinfo("Eliminado", "Empleado eliminado.")
            self.limpiar()
            self.cargar_lista()

    def limpiar(self):
        for campo in self.entries.values():
            campo.delete(0, 'end')
        self.selected_id = None

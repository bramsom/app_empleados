import customtkinter as ctk
from tkinter import messagebox
from controllers.affiliation_controller import (
    registrar_afiliacion,
    listar_afiliaciones,
    consultar_afiliacion,
    modificar_afiliacion,
    borrar_afiliacion
)
from controllers.employee_controller import listar_empleados

class CrudAfiliaciones(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.title("CRUD Afiliaciones")
        self.geometry("700x650")
        self.selected_id = None

        ctk.CTkButton(self, text="Volver al menú principal", command=lambda: self.volver_menu(username, rol)).pack(pady=20)

        self.scroll = ctk.CTkScrollableFrame(self, width=680, height=600)
        self.scroll.pack(padx=10, pady=10, fill="both", expand=True)

        self.empleado_map = {f"{e.name} {e.last_name} ({e.document_number})": e.id for e in listar_empleados()}
        self.option_empleado = ctk.CTkOptionMenu(self.scroll, values=list(self.empleado_map.keys()))
        self.option_empleado.pack(pady=5)

        self.tipo_afiliacion = ctk.CTkOptionMenu(self.scroll, values=["EPS", "ARL", "AFP", "BANCO"])
        self.tipo_afiliacion.pack(pady=5)

        campos = ["Nombre", "Banco", "Número de cuenta", "Tipo de cuenta"]
        self.entries = {}
        for campo in campos:
            lbl = ctk.CTkLabel(self.scroll, text=campo)
            lbl.pack(pady=2)
            entry = ctk.CTkEntry(self.scroll)
            entry.pack(pady=2)
            self.entries[campo.lower().replace(" ", "_")] = entry

        ctk.CTkButton(self.scroll, text="Guardar", command=self.guardar).pack(pady=5)
        ctk.CTkButton(self.scroll, text="Actualizar", command=self.actualizar).pack(pady=5)
        ctk.CTkButton(self.scroll, text="Eliminar", command=self.eliminar).pack(pady=5)
        ctk.CTkButton(self.scroll, text="Limpiar", command=self.limpiar).pack(pady=5)

        # Marco para mostrar afiliaciones
        self.frame_lista = ctk.CTkScrollableFrame(self.scroll, width=640, height=200)
        self.frame_lista.pack(pady=10)

        self.afiliaciones = {}
        self.cargar_lista()

    def cargar_lista(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        resultados = listar_afiliaciones()
        self.afiliaciones = {}
        for r in resultados:
            clave = f"{r.employee_id} - {r.affiliation_type} ({r.name})"
            self.afiliaciones[clave] = r.id
            boton = ctk.CTkButton(self.frame_lista, text=clave, command=lambda k=clave: self.cargar(k))
            boton.pack(fill="x", padx=5, pady=2)

    def cargar(self, clave):
        af_id = self.afiliaciones.get(clave)
        datos = consultar_afiliacion(af_id)
        if not datos:
            return
        self.selected_id = af_id
        self.option_empleado.set(self._get_empleado_display(datos.employee_id))
        self.tipo_afiliacion.set(datos.affiliation_type)

        for key in self.entries:
            self.entries[key].delete(0, 'end')

        self.entries["nombre"].insert(0, datos.name or "")
        self.entries["banco"].insert(0, datos.bank or "")
        self.entries["número_de_cuenta"].insert(0, datos.account_number or "")
        self.entries["tipo_de_cuenta"].insert(0, datos.account_type or "")

    def guardar(self):
        try:
            tipo = self.tipo_afiliacion.get().strip().upper()
            if tipo not in ["EPS", "ARL", "AFP", "BANCO"]:
                messagebox.showerror("Error", "Tipo de afiliación no válido.")
                return

            datos = (
                self.empleado_map[self.option_empleado.get()],
                tipo,
                self.entries["nombre"].get().strip(),
                self.entries["banco"].get().strip(),
                self.entries["número_de_cuenta"].get().strip(),
                self.entries["tipo_de_cuenta"].get().strip()
            )
            registrar_afiliacion(datos)
            messagebox.showinfo("Éxito", "Afiliación registrada.")
            self.cargar_lista()
            self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        if not self.selected_id:
            return
        tipo = self.tipo_afiliacion.get().strip().upper()
        if tipo not in ["EPS", "ARL", "AFP", "BANCO"]:
            messagebox.showerror("Error", "Tipo de afiliación no válido.")
            return

        datos = (
            self.empleado_map[self.option_empleado.get()],
            tipo,
            self.entries["nombre"].get().strip(),
            self.entries["banco"].get().strip(),
            self.entries["número_de_cuenta"].get().strip(),
            self.entries["tipo_de_cuenta"].get().strip()
        )
        modificar_afiliacion(self.selected_id, datos)
        messagebox.showinfo("Actualizado", "Afiliación actualizada.")
        self.cargar_lista()

    def eliminar(self):
        if not self.selected_id:
            return
        if messagebox.askyesno("¿Confirmar?", "¿Eliminar esta afiliación?"):
            borrar_afiliacion(self.selected_id)
            messagebox.showinfo("Eliminado", "Afiliación eliminada.")
            self.cargar_lista()
            self.limpiar()

    def limpiar(self):
        for e in self.entries.values():
            e.delete(0, 'end')
        self.selected_id = None
        if self.empleado_map:
            self.option_empleado.set(list(self.empleado_map.keys())[0])
        self.tipo_afiliacion.set("EPS")

    def _get_empleado_display(self, emp_id):
        for k, v in self.empleado_map.items():
            if v == emp_id:
                return k
        return ""

    def volver_menu(self, username, rol):
        self.destroy()
        from views.main_menu import MainMenu
        main_menu = MainMenu(username, rol)
        main_menu.mainloop()

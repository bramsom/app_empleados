import customtkinter as ctk
from tkinter import messagebox
from controllers.affiliation_controller import (registrar_afiliacion,
    listar_afiliaciones,
    consultar_afiliacion,
    modificar_afiliacion,
    borrar_afiliacion)
from controllers.employee_controller import listar_empleados  # para seleccionar empleados

class CrudAfiliaciones(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.title("CRUD Afiliaciones")
        self.geometry("700x620")
        self.selected_id = None

        ctk.CTkButton(self, text="Volver al menú principal", command=lambda: self.volver_menu(username, rol)).pack(pady=20)

        self.scroll = ctk.CTkScrollableFrame(self, width=680, height=600)
        self.scroll.pack(padx=10, pady=10, fill="both", expand=True)

        # Empleado
        self.empleado_map = {f"{e[1]} {e[2]} ({e[4]})": e[0] for e in listar_empleados()}
        self.option_empleado = ctk.CTkOptionMenu(self.scroll, values=list(self.empleado_map.keys()))
        self.option_empleado.pack(pady=5)

        # Tipo de afiliación
        self.tipo_afiliacion = ctk.CTkOptionMenu(self.scroll, values=["EPS", "ARL", "AFP", "BANCO"])
        self.tipo_afiliacion.pack(pady=5)

        # Campos texto
        campos = ["Nombre", "Banco", "Número de cuenta", "Tipo de cuenta"]
        self.entries = {}
        for campo in campos:
            lbl = ctk.CTkLabel(self.scroll, text=campo)
            lbl.pack(pady=2)
            entry = ctk.CTkEntry(self.scroll)
            entry.pack(pady=2)
            self.entries[campo.lower().replace(" ", "_")] = entry

        # Botones
        ctk.CTkButton(self.scroll, text="Guardar", command=self.guardar).pack(pady=5)
        ctk.CTkButton(self.scroll, text="Actualizar", command=self.actualizar).pack(pady=5)
        ctk.CTkButton(self.scroll, text="Eliminar", command=self.eliminar).pack(pady=5)
        ctk.CTkButton(self.scroll, text="Limpiar", command=self.limpiar).pack(pady=5)

        # Lista de afiliaciones
        self.lista = ctk.CTkOptionMenu(self.scroll, values=[], command=self.cargar)
        self.lista.pack(pady=10)
        self.cargar_lista()

    def cargar_lista(self):
        resultados = listar_afiliaciones()
        self.afiliaciones = {f"{r[1]} - {r[2]} ({r[3]})": r[0] for r in resultados}
        self.lista.configure(values=list(self.afiliaciones.keys()))
        if self.afiliaciones:
            primera = list(self.afiliaciones.keys())[0]
            self.lista.set(primera)
            self.cargar(primera)
        else:
            self.lista.set("")

    def cargar(self, clave):
        af_id = self.afiliaciones.get(clave)
        datos = consultar_afiliacion(af_id)
        if not datos:
            return
        self.selected_id = af_id
        self.option_empleado.set(self._get_empleado_display(datos[1]))
        self.tipo_afiliacion.set(datos[2])
        self.entries["nombre"].delete(0, 'end')
        self.entries["nombre"].insert(0, datos[3] or "")
        self.entries["banco"].delete(0, 'end')
        self.entries["banco"].insert(0, datos[4] or "")
        self.entries["número_de_cuenta"].delete(0, 'end')
        self.entries["número_de_cuenta"].insert(0, datos[5] or "")
        self.entries["tipo_de_cuenta"].delete(0, 'end')
        self.entries["tipo_de_cuenta"].insert(0, datos[6] or "")

    def guardar(self):
        try:
            datos = (
                self.empleado_map[self.option_empleado.get()],
                self.tipo_afiliacion.get(),
                self.entries["nombre"].get(),
                self.entries["banco"].get(),
                self.entries["número_de_cuenta"].get(),
                self.entries["tipo_de_cuenta"].get()
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
        datos = (
            self.empleado_map[self.option_empleado.get()],
            self.tipo_afiliacion.get(),
            self.entries["nombre"].get(),
            self.entries["banco"].get(),
            self.entries["número_de_cuenta"].get(),
            self.entries["tipo_de_cuenta"].get()
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
        self.destroy()  # Cierra esta ventana
        from views.main_menu import MainMenu
        main_menu = MainMenu(username, rol)
        main_menu.mainloop()
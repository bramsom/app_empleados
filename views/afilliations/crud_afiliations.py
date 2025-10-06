import customtkinter as ctk
from tkinter import messagebox
from controllers.affiliation_controller import (
    registrar_afiliacion,
    listar_afiliaciones,
    consultar_afiliacion,
    modificar_afiliacion,
    consultar_afiliaciones_por_empleado,
    borrar_afiliacion
)
from controllers.employee_controller import listar_empleados

class CrudAfiliaciones(ctk.CTkFrame):
    def __init__(self, parent, username, rol, action=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.action = action
        self.configure(fg_color="transparent")

        ctk.CTkButton(self, text="Volver al menú principal", command=lambda: self.volver_menu(username, rol)).pack(pady=20)

        self.scroll = ctk.CTkScrollableFrame(self, width=680, height=600)
        self.scroll.pack(padx=10, pady=10, fill="both", expand=True)

        # Mapa empleados
        self.empleado_map = {f"{e.name} {e.last_name} ({e.document_number})": e.id for e in listar_empleados()}
        

        campos = ["EPS", "ARL", "AFP", "Banco", "Número de cuenta", "Tipo de cuenta"]
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

        # Marco para mostrar afiliación
        self.frame_lista = ctk.CTkScrollableFrame(self.scroll, width=640, height=200)
        self.frame_lista.pack(pady=10)

        self.afiliaciones = {}
        self.afiliacion_actual = None

    def cargar_lista(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        resultados = listar_afiliaciones()
        self.afiliaciones = {}
    
        for r in resultados:
            empleado = consultar_afiliaciones_por_empleado(r.employee_id)
            clave = f"{empleado.name} {empleado.last_name} ({empleado.document_number})"
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

        # Limpiar campos
        for key in self.entries:
            self.entries[key].delete(0, 'end')

        # Insertar datos según los campos del nuevo modelo
        self.entries["eps"].insert(0, datos.eps or "")
        self.entries["arl"].insert(0, datos.arl or "")
        self.entries["afp"].insert(0, datos.afp or "")
        self.entries["banco"].insert(0, datos.bank or "")
        self.entries["número_de_cuenta"].insert(0, datos.account_number or "")
        self.entries["tipo_de_cuenta"].insert(0, datos.account_type or "")

    def guardar(self):
        try:
            employee_id = self.empleado_map.get(self.option_empleado.get())
            if not employee_id:
                messagebox.showerror("Error", "Debe seleccionar un empleado.")
                return

            datos = (
                employee_id,
                self.entries["eps"].get().strip(),
                self.entries["arl"].get().strip(),
                self.entries["afp"].get().strip(),
                self.entries["banco"].get().strip(),
                self.entries["número_de_cuenta"].get().strip(),
                self.entries["tipo_de_cuenta"].get().strip()
            )

            registrar_afiliacion(datos)
            messagebox.showinfo("Éxito", "Afiliación registrada correctamente.")
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

    def _get_empleado_display(self, emp_id):
        for k, v in self.empleado_map.items():
            if v == emp_id:
                return k
        return ""


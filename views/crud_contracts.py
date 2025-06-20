import customtkinter as ctk
from tkinter import messagebox
from bd.contracts import crear_contrato, obtener_contratos, obtener_contrato_por_id, actualizar_contrato, eliminar_contrato
from bd.employees import obtener_empleados  # para seleccionar empleados

class CrudContratos(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.title("CRUD Contratos")
        self.geometry("700x650")
        
        ctk.CTkButton(self, text="Volver al menú principal", command=lambda: self.volver_menu(username, rol)).pack(pady=20)
        # Frame desplazable
        self.scroll = ctk.CTkScrollableFrame(self, width=680, height=630)
        self.scroll.pack(padx=10, pady=10, fill="both", expand=True)

        # Empleados
        self.empleado_map = {f"{e[1]} {e[2]} ({e[4]})": e[0] for e in obtener_empleados()}
        self.option_empleado = ctk.CTkOptionMenu(self.scroll, values=list(self.empleado_map.keys()))
        self.option_empleado.pack(pady=5)

        # Tipo de contrato
        self.tipo_contrato = ctk.CTkOptionMenu(
            self.scroll, 
            values=[
                'contrato individual de trabajo termino fijo',
                'contrato individual de trabajo termino indefinido',
                'contrato servicio hora_catedra',
                'contrato aprendizaje sena',
                'orden prestacion de servicios'
            ]
        )
        self.tipo_contrato.pack(pady=5)

        # Campos de fechas y números
        campos = [
            "Fecha inicio", "Fecha fin", "Valor hora", "N° horas",
            "Pago mensual", "Transporte", "Contratista"
        ]
        self.entries = {}
        for campo in campos:
            lbl = ctk.CTkLabel(self.scroll, text=campo)
            lbl.pack(pady=2)
            entry = ctk.CTkEntry(self.scroll)
            entry.pack(pady=2)
            self.entries[campo.lower().replace(" ", "_")] = entry

        # Estado del contrato
        self.estado = ctk.CTkOptionMenu(self.scroll, values=["ACTIVO", "FINALIZADO", "RETIRADO"])
        self.estado.pack(pady=5)

        # Botones
        ctk.CTkButton(self.scroll, text="Guardar", command=self.guardar).pack(pady=5)
        ctk.CTkButton(self.scroll, text="Actualizar", command=self.actualizar).pack(pady=5)
        ctk.CTkButton(self.scroll, text="Eliminar", command=self.eliminar).pack(pady=5)
        ctk.CTkButton(self.scroll, text="Limpiar", command=self.limpiar).pack(pady=5)

        # Lista de contratos
        self.lista = ctk.CTkOptionMenu(self.scroll, values=[], command=self.cargar)
        self.lista.pack(pady=10)
        self.cargar_lista()

    def cargar_lista(self):
        contratos = obtener_contratos()
        self.contratos = {f"{c[1]} - {c[2]} ({c[5]})": c[0] for c in contratos}
        self.lista.configure(values=list(self.contratos.keys()))
        if self.contratos:
            self.lista.set(list(self.contratos.keys())[0])
            self.cargar(list(self.contratos.keys())[0])
        else:
            self.lista.set("")

    def cargar(self, clave):
        cid = self.contratos.get(clave)
        datos = obtener_contrato_por_id(cid)
        if not datos: return
        self.selected_id = cid
        self.option_empleado.set(self._get_empleado_display(datos[1]))
        self.tipo_contrato.set(datos[2])
        self.entries["fecha_inicio"].delete(0, 'end')
        self.entries["fecha_inicio"].insert(0, datos[3])
        self.entries["fecha_fin"].delete(0, 'end')
        self.entries["fecha_fin"].insert(0, datos[4])
        self.entries["valor_hora"].delete(0, 'end')
        self.entries["valor_hora"].insert(0, datos[5])
        self.entries["n°_horas"].delete(0, 'end')
        self.entries["n°_horas"].insert(0, datos[6])
        self.entries["pago_mensual"].delete(0, 'end')
        self.entries["pago_mensual"].insert(0, datos[7])
        self.entries["transporte"].delete(0, 'end')
        self.entries["transporte"].insert(0, datos[8])
        self.estado.set(datos[9])
        self.entries["contratista"].delete(0, 'end')
        self.entries["contratista"].insert(0, datos[10])

    def guardar(self):
        try:
            datos = (
                self.empleado_map[self.option_empleado.get()],
                self.tipo_contrato.get(),
                self.entries["fecha_inicio"].get(),
                self.entries["fecha_fin"].get(),
                float(self.entries["valor_hora"].get()),
                int(self.entries["n°_horas"].get()),
                float(self.entries["pago_mensual"].get()),
                float(self.entries["transporte"].get()),
                self.estado.get(),
                self.entries["contratista"].get()
            )
            crear_contrato(datos)
            messagebox.showinfo("Éxito", "Contrato creado.")
            self.cargar_lista()
            self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        if not self.selected_id:
            return
        datos = (
            self.empleado_map[self.option_empleado.get()],
            self.tipo_contrato.get(),
            self.entries["fecha_inicio"].get(),
            self.entries["fecha_fin"].get(),
            float(self.entries["valor_hora"].get()),
            int(self.entries["n°_horas"].get()),
            float(self.entries["pago_mensual"].get()),
            float(self.entries["transporte"].get()),
            self.estado.get(),
            self.entries["contratista"].get()
        )
        actualizar_contrato(self.selected_id, datos)
        messagebox.showinfo("Actualizado", "Contrato actualizado.")
        self.cargar_lista()

    def eliminar(self):
        if not self.selected_id:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este contrato?"):
            eliminar_contrato(self.selected_id)
            messagebox.showinfo("Eliminado", "Contrato eliminado.")
            self.cargar_lista()
            self.limpiar()

    def limpiar(self):
        for e in self.entries.values():
            e.delete(0, 'end')
        self.selected_id = None
        self.option_empleado.set(list(self.empleado_map.keys())[0])
        self.tipo_contrato.set("contrato individual de trabajo termino fijo")
        self.estado.set("ACTIVO")

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
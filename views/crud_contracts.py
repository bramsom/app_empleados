import customtkinter as ctk
from tkinter import messagebox
from controllers.contract_controller import ( registrar_contrato,
    listar_contratos,
    consultar_contrato,
    modificar_contrato,
    borrar_contrato
    )
from controllers.employee_controller import listar_empleados  # para seleccionar empleados
from models.contract import Contrato

class CrudContratos(ctk.CTkFrame):
    def __init__(self, parent, username, rol):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.configure(fg_color="transparent")

        #ctk.CTkButton(self, text="Volver al menú principal", command=lambda: self.volver_menu(username, rol)).pack(pady=20)
        self.scroll = ctk.CTkScrollableFrame(self, width=680, height=630)
        self.scroll.pack(padx=10, pady=10, fill="both", expand=True)

        self.empleado_map = { f"{e.name} {e.last_name} ({e.document_number})": e.id for e in listar_empleados()}
        self.option_empleado = ctk.CTkOptionMenu(self.scroll, values=list(self.empleado_map.keys()))
        self.option_empleado.pack(pady=5)

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

        campos = [
            "Fecha inicio", "Fecha fin", "Valor hora", "Numero horas",
            "Pago mensual", "Transporte", "Contratista"
        ]
        self.entries = {}
        for campo in campos:
            lbl = ctk.CTkLabel(self.scroll, text=campo)
            lbl.pack(pady=2)
            entry = ctk.CTkEntry(self.scroll)
            entry.pack(pady=2)
            self.entries[campo.lower().replace(" ", "_")] = entry

        self.estado = ctk.CTkOptionMenu(self.scroll, values=["ACTIVO", "FINALIZADO", "RETIRADO"])
        self.estado.pack(pady=5)

        ctk.CTkButton(self.scroll, text="Guardar", command=self.guardar).pack(pady=5)
        ctk.CTkButton(self.scroll, text="Actualizar", command=self.actualizar).pack(pady=5)
        ctk.CTkButton(self.scroll, text="Eliminar", command=self.eliminar).pack(pady=5)
        ctk.CTkButton(self.scroll, text="Limpiar", command=self.limpiar).pack(pady=5)

        self.lista = ctk.CTkOptionMenu(self.scroll, values=[], command=self.cargar)
        self.lista.pack(pady=10)
        self.cargar_lista()

    def cargar_lista(self):
        contratos = listar_contratos()
        self.contratos = {f"{c[1]} - {c[2]} ({c[5]})": c[0] for c in contratos}
        self.lista.configure(values=list(self.contratos.keys()))
        if self.contratos:
            self.lista.set(list(self.contratos.keys())[0])
            self.cargar(list(self.contratos.keys())[0])
        else:
            self.lista.set("")

    def cargar(self, clave):
        cid = self.contratos.get(clave)
        datos = consultar_contrato(cid)
        if not datos: return
        self.selected_id = cid
        self.option_empleado.set(self._get_empleado_display(datos.employee_id))
        self.tipo_contrato.set(datos.type_contract)
        self.entries["fecha_inicio"].delete(0, 'end')
        self.entries["fecha_inicio"].insert(0, datos.start_date)
        self.entries["fecha_fin"].delete(0, 'end')
        self.entries["fecha_fin"].insert(0, datos.end_date)
        self.entries["valor_hora"].delete(0, 'end')
        self.entries["valor_hora"].insert(0, datos.value_hour)
        self.entries["numero_horas"].delete(0, 'end')
        self.entries["numero_horas"].insert(0, datos.number_hour)
        self.entries["pago_mensual"].delete(0, 'end')
        self.entries["pago_mensual"].insert(0, datos.monthly_payment)
        self.entries["transporte"].delete(0, 'end')
        self.entries["transporte"].insert(0, datos.transport)
        self.estado.set(datos.state)
        self.entries["contratista"].delete(0, 'end')
        self.entries["contratista"].insert(0, datos.contractor)

    def _obtener_datos_contrato(self):
        try:
            datos = (
                self.empleado_map[self.option_empleado.get()],
                self.tipo_contrato.get(),
                self.entries["fecha_inicio"].get().strip(),
                self.entries["fecha_fin"].get().strip(),
                float(self.entries["valor_hora"].get()),
                int(float(self.entries["numero_horas"].get())),
                float(self.entries["pago_mensual"].get()),
                float(self.entries["transporte"].get()),
                self.estado.get(),
                self.entries["contratista"].get().strip()
            )
            return datos
        except ValueError as ve:
            messagebox.showerror("Error de validación", f"Verifica los datos numéricos: {ve}")
            return None
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return None

    def guardar(self):
        datos = self._obtener_datos_contrato()
        if not datos:
            return
        try:
            registrar_contrato(datos)
            messagebox.showinfo("Éxito", "Contrato creado.")
            self.cargar_lista()
            self.limpiar()
        except Exception as e:
            messagebox.showerror("Error al guardar", str(e))

    def actualizar(self):
        if not hasattr(self, 'selected_id') or not self.selected_id:
            messagebox.showwarning("Advertencia", "Selecciona un contrato primero.")
            return
        datos = self._obtener_datos_contrato()
        if not datos:
            return
        try:
            modificar_contrato(self.selected_id, datos)
            messagebox.showinfo("Actualizado", "Contrato actualizado.")
            self.cargar_lista()
        except Exception as e:
            messagebox.showerror("Error al actualizar", str(e))

    def eliminar(self):
        if not hasattr(self, 'selected_id') or not self.selected_id:
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar este contrato?"):
            borrar_contrato(self.selected_id)
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

    ##def volver_menu(self, username, rol):
       # self.destroy()
       # from views.main_menu import MainMenu
       # main_menu = MainMenu(username, rol)
       # main_menu.mainloop()

'''import customtkinter as ctk
from tkinter import ttk

class ContractManager:
    def __init__(self, root):
        self.root = root
        
        # Frame principal para el contenido (sobre el fondo)
        self.main_content_frame = ctk.CTkFrame(
            root, 
            fg_color="white",
            corner_radius=10,
            width=800,
            height=500
        )
        self.main_content_frame.place(x=50, y=100)  # Ajusta según tu layout
        
        # Frame para contratos (inicialmente oculto)
        self.contracts_frame = None
        
    def show_contracts_view(self):
        # Limpiar contenido actual
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()
            
        # Crear la vista de contratos
        self.create_contracts_table()
        
    def create_contracts_table(self):
        # Título
        title_label = ctk.CTkLabel(
            self.main_content_frame,
            text="CONTRATOS",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame para la tabla
        table_frame = ctk.CTkFrame(self.main_content_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear Treeview para la tabla
        columns = ('nombre', 'fecha_inicio', 'fecha_fin', 'tipo', 'modalidad', 
                  'transporte', 'valor', 'horas', 'estado', 'persona')
        
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar encabezados
        headers = {
            'nombre': 'Nombre o razón social',
            'fecha_inicio': 'Fecha inicio',
            'fecha_fin': 'Fecha fin',
            'tipo': 'Tipo de contrato',
            'modalidad': 'Modalidad',
            'transporte': 'Transporte',
            'valor': 'Valor hora',
            'horas': 'Horas',
            'estado': 'Estado',
            'persona': 'Persona que lo contrató'
        }
        
        for col in columns:
            tree.heading(col, text=headers[col])
            tree.column(col, width=100)
        
        # Datos de ejemplo
        contracts_data = [
            ('Huyen mental violin anterior', '03/04/2025', '03/10/2025', 'Contrato de aprendizaje', '$100000.00', '30', 'Activo', 'Edgar Alfonso Paez Flor'),
            ('Huyen mental violin anterior', '03/04/2025', '03/10/2025', 'Contrato de aprendizaje', '$100000.00', '30', 'Activo', 'Edgar Alfonso Paez Flor'),
            # ... más datos
        ]
        
        for contract in contracts_data:
            tree.insert('', 'end', values=contract)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones de acción
        button_frame = ctk.CTkFrame(self.main_content_frame)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        edit_btn = ctk.CTkButton(button_frame, text="Editar", width=100)
        edit_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(button_frame, text="Eliminar", width=100)
        delete_btn.pack(side="left", padx=5)'''
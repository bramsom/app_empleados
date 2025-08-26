# views/contracts/edit_contracts.py
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from datetime import datetime
from models.contract import Contrato
from services import contract_service, employee_service
from utils.canvas import agregar_fondo_decorativo
from utils.autocomplete import crear_autocompletado
from utils.contract_helpers import (
    fill_entry_field,
    format_date_for_entry,
    format_money_for_entry,
    parse_money_from_entry,
    abrir_calendario
)

class EditarContrato(ctk.CTkFrame):
    def __init__(self, parent, contract_id, username=None, rol=None, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.contrato_id = contract_id
        
        empleados = employee_service.obtener_empleados_para_combobox()
        self.empleados_dict = {f"{nombre}": id for id, nombre in empleados}
        
        agregar_fondo_decorativo(self)
        self.configure(fg_color="#F5F5F5")
        
        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))
        
        self.entry_style = {"border_width": 0, "fg_color": "#D9D9D9", "text_color": "#000000", "height": 40}
        self.label_style = {"font": ("Georgia", 12, "bold")}
        self.title_style = {"font": ("Georgia", 16), "text_color": "#06A051"}
        self.boton_style = {"font": ("Georgia", 14), "text_color": "black", "height": 50}
        
        self._setup_ui()
        self.cargar_datos()

    def _setup_ui(self):
        ctk.CTkButton(
            self, image=self.icon_back, text="", width=40, height=40,
            fg_color="#D2D2D2", corner_radius=0, hover_color="#E0E0E0", command=self.cancelar
        ).place(relx=0.98, rely=0.02, anchor="ne")

        ctk.CTkLabel(
            self, text="EDITAR CONTRATO", fg_color="transparent", **self.title_style
        ).pack(pady=(40, 0), padx=(250, 0), anchor="w")

        self.card = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card.place(relx=0.52, rely=0.52, anchor="center", relwidth=0.70, relheight=0.80)
        self.card.rowconfigure(0, weight=1)
        self.card.columnconfigure(0, weight=1)

        self.form_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.form_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        self.form_frame.columnconfigure((0, 1, 2, 3), weight=1)
        
        self._crear_widgets()

        botones_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        botones_frame.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="ew")
        botones_frame.columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            botones_frame, text="Guardar cambios", fg_color="#06A051", hover_color="#048B45",
            command=self.guardar_cambios, **self.boton_style, corner_radius=10
        ).grid(row=0, column=0, padx=30, pady=30, sticky="ew")
        ctk.CTkButton(
            botones_frame, text="Cancelar", fg_color="#D12B1B", hover_color="#B81D0F",
            command=self.cancelar, **self.boton_style, corner_radius=10
        ).grid(row=0, column=1, padx=30, pady=30, sticky="ew")

    def _crear_widgets(self):
        def create_field(text, row, col, colspan, attr_name, placeholder=""):
            ctk.CTkLabel(self.form_frame, text=text, **self.label_style).grid(
                row=row, column=col, columnspan=colspan, sticky="w", pady=(5, 0), padx=5
            )
            entry = ctk.CTkEntry(self.form_frame, placeholder_text=placeholder or text, **self.entry_style)
            entry.grid(row=row + 1, column=col, columnspan=colspan, padx=5, pady=(0, 10), sticky="ew")
            setattr(self, attr_name, entry)
            return entry

        self.entry_empleado = create_field("Nombre Empleado", 0, 0, 2, "entry_empleado")
        
        ctk.CTkLabel(self.form_frame, text="Tipo contrato", **self.label_style).grid(
            row=0, column=2, columnspan=2, sticky="w", pady=(5, 0), padx=5
        )
        opciones_tipo_contrato = [
            "CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO", "CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO",
            "CONTRATO SERVICIO HORA CATEDRA", "CONTRATO APRENDIZAJE SENA", "ORDEN PRESTACION DE SERVICIOS"
        ]
        self.tipo_contrato_var = ctk.StringVar(value=opciones_tipo_contrato[0])
        self.tipo_contrato_menu = ctk.CTkOptionMenu(
            self.form_frame, values=opciones_tipo_contrato, variable=self.tipo_contrato_var,
            fg_color="#D9D9D9", height=40, text_color="black",
            button_color="#06A051", button_hover_color="#048B45",
            dropdown_fg_color="white", dropdown_text_color="black",
            command=self._on_type_contract_change
        )
        self.tipo_contrato_menu.grid(row=1, column=2, columnspan=2, padx=5, pady=(0, 10), sticky="ew")

        self.start_date = create_field("Fecha inicio", 2, 0, 1, "start_date")
        self.start_date.bind("<Button-1>", lambda e: abrir_calendario(self, self.start_date))

        self.end_date = create_field("Fecha fin", 2, 1, 1, "end_date")
        self.end_date.bind("<Button-1>", lambda e: abrir_calendario(self, self.end_date))
        
        self.label_pago1 = ctk.CTkLabel(self.form_frame, text="", **self.label_style)
        self.entry_pago1 = ctk.CTkEntry(self.form_frame, **self.entry_style)
        self.label_pago2 = ctk.CTkLabel(self.form_frame, text="", **self.label_style)
        self.entry_pago2 = ctk.CTkEntry(self.form_frame, **self.entry_style)
        
        self.contractor = create_field("Contratante", 4, 0, 2, "contractor")
        
        ctk.CTkLabel(self.form_frame, text="Estado", **self.label_style).grid(
            row=4, column=2, columnspan=2, sticky="w", pady=(5, 0), padx=5
        )
        opciones_estado = ["ACTIVO", "FINALIZADO", "RETIRADO"]
        self.estado_var = ctk.StringVar(value=opciones_estado[0])
        self.estado_menu = ctk.CTkOptionMenu(
            self.form_frame, values=opciones_estado, variable=self.estado_var,
            fg_color="#D9D9D9", height=40, text_color="black",
            button_color="#06A051", button_hover_color="#048B45",
            dropdown_fg_color="white", dropdown_text_color="black"
        )
        self.estado_menu.grid(row=5, column=2, columnspan=2, padx=5, pady=(0, 10), sticky="ew")
        
        self.entry_empleado.empleados_dict = self.empleados_dict
        self.lista_empleados = ctk.CTkFrame(self.form_frame, fg_color="white", corner_radius=15, width=200)
        self.lista_empleados.place(x=0, y=0)
        self.lista_empleados.lower()
        self.entry_empleado.bind(
            "<KeyRelease>",
            crear_autocompletado(self.entry_empleado, self.lista_empleados, self.seleccionar_empleado)
        )

    def _on_type_contract_change(self, choice):
        self._ocultar_todos_los_campos_pago()
        self._mostrar_campos_pago(choice, None, None, None, None, None, None)

    def _ocultar_todos_los_campos_pago(self):
        self.label_pago1.grid_remove()
        self.entry_pago1.grid_remove()
        self.label_pago2.grid_remove()
        self.entry_pago2.grid_remove()

    def cargar_datos(self):
        contrato_data = contract_service.obtener_contrato_por_id(self.contrato_id)
        if not contrato_data:
            messagebox.showerror("Error", "No se encontró el contrato.")
            if self.volver_callback and self.volver_callback.winfo_exists():
                self.volver_callback.pack(fill="both", expand=True)
            return

        self.original_contract_data = contrato_data
    
        # Actualizar la línea de desempaquetado para que coincida con la consulta
        (id_, employee_id, empleado_nombre, type_contract, start_date, end_date, state,
         contractor, total_payment, payment_frequency, monthly_payment, transport,
         value_hour, number_hour, new_total_payment, new_payment_frequency) = contrato_data

        fill_entry_field(self.entry_empleado, empleado_nombre)
        self.entry_empleado.employee_id = employee_id

        fill_entry_field(self.start_date, format_date_for_entry(start_date))
        fill_entry_field(self.end_date, format_date_for_entry(end_date))
        fill_entry_field(self.contractor, contractor)
    
        self.tipo_contrato_var.set(type_contract)
        self.estado_var.set(state)

        # La lógica para mostrar los campos de pago debe usar las nuevas variables
        # para los contratos de "Orden de Prestación de Servicios".
        self._mostrar_campos_pago(
            type_contract, monthly_payment, transport, value_hour,
            number_hour, new_total_payment, new_payment_frequency
        )

    def _mostrar_campos_pago(self, type_contract, monthly_payment, transport, value_hour, number_hour, total_payment, payment_frequency):
        self._ocultar_todos_los_campos_pago()
        
        campos_a_mostrar = []
        if type_contract in ['CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO', 'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO', 'CONTRATO APRENDIZAJE SENA']:
            campos_a_mostrar = [
                ("Mensualidad", format_money_for_entry(monthly_payment)),
                ("Transporte", format_money_for_entry(transport))
            ]
        elif type_contract == 'CONTRATO SERVICIO HORA CATEDRA':
            campos_a_mostrar = [
                ("Valor Hora", format_money_for_entry(value_hour)),
                ("Número de Horas", number_hour)
            ]
        elif type_contract == 'ORDEN PRESTACION DE SERVICIOS':
            campos_a_mostrar = [
                ("Pago Total", format_money_for_entry(total_payment)),
                ("Frecuencia de Pago", payment_frequency)
            ]
        
        if len(campos_a_mostrar) == 2:
            self.label_pago1.configure(text=campos_a_mostrar[0][0])
            fill_entry_field(self.entry_pago1, campos_a_mostrar[0][1])
            self.label_pago1.grid(row=2, column=2, sticky="w", pady=(5, 0), padx=5)
            self.entry_pago1.grid(row=3, column=2, padx=5, pady=(0, 10), sticky="ew")

            self.label_pago2.configure(text=campos_a_mostrar[1][0])
            fill_entry_field(self.entry_pago2, campos_a_mostrar[1][1])
            self.label_pago2.grid(row=2, column=3, sticky="w", pady=(5, 0), padx=5)
            self.entry_pago2.grid(row=3, column=3, padx=5, pady=(0, 10), sticky="ew")

    def guardar_cambios(self):
        empleado_nombre = self.entry_empleado.get()
        employee_id = getattr(self.entry_empleado, 'employee_id', None) 
        
        if employee_id is None: 
            employee_id = self.empleados_dict.get(empleado_nombre)
        
        if employee_id is None:
            messagebox.showerror("Error", "Debes seleccionar un empleado válido de la lista.")
            return

        type_contract = self.tipo_contrato_var.get()
        
        try:
            start_date = datetime.strptime(self.start_date.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha de inicio inválido. Use DD/MM/YYYY.")
            return
        
        end_date = None
        if self.end_date.get():
            try:
                end_date = datetime.strptime(self.end_date.get(), '%d/%m/%Y').strftime('%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha fin inválido. Use DD/MM/YYYY.")
                return

        monthly_payment = None
        transport = None
        value_hour = None
        number_hour = None
        total_payment = None
        payment_frequency = None

        if type_contract in ['CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO', 'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO', 'CONTRATO APRENDIZAJE SENA']:
            monthly_payment = parse_money_from_entry(self.entry_pago1.get())
            transport = parse_money_from_entry(self.entry_pago2.get())
            if monthly_payment is None or transport is None: return

        elif type_contract == 'CONTRATO SERVICIO HORA CATEDRA':
            value_hour = parse_money_from_entry(self.entry_pago1.get())
            try:
                number_hour = float(self.entry_pago2.get() or 0)
            except ValueError:
                messagebox.showerror("Error", "Número de Horas debe ser un valor numérico válido.")
                return
            if value_hour is None: return

        elif type_contract == 'ORDEN PRESTACION DE SERVICIOS':
            total_payment = parse_money_from_entry(self.entry_pago1.get())
            payment_frequency = self.entry_pago2.get()
            if total_payment is None: return
        
        try:
            contrato_actualizado = Contrato(
                id=self.contrato_id,
                employee_id=employee_id,
                type_contract=type_contract,
                start_date=start_date,
                end_date=end_date,
                state=self.estado_var.get(),
                contractor=self.contractor.get(),
                total_payment=total_payment,
                payment_frequency=payment_frequency,
                monthly_payment=monthly_payment,
                transport=transport,
                value_hour=value_hour,
                number_hour=number_hour
            )

            contract_service.actualizar_contrato(self.contrato_id, contrato_actualizado)
        
            messagebox.showinfo("Éxito", "Contrato actualizado exitosamente.")
            
            if self.volver_callback:
                self.volver_callback.actualizar_lista()
                self.destroy()
                self.volver_callback.pack(fill="both", expand=True)

        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo actualizar el contrato: {e}")

    def cancelar(self):
        if self.volver_callback:
            self.destroy()
            self.volver_callback.pack(fill="both", expand=True)

    def seleccionar_empleado(self, nombre):
        fill_entry_field(self.entry_empleado, nombre)
        self.entry_empleado.employee_id = self.empleados_dict.get(nombre) 
        self.lista_empleados.lower()
# C:\Users\Usuario\Documents\proyectos python\app_empleados\views\contracts\register_contracts.py

import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from models.contract import Contrato
from controllers import contract_controller
from utils.canvas import agregar_fondo_decorativo
from services import contract_service, employee_service
from utils.autocomplete import crear_autocompletado

class RegistrarContrato(ctk.CTkFrame):
    def __init__(self, parent, username=None, rol=None, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.calendario_abierto = None

        # Estilos y configuración inicial
        self.configure(fg_color="#F5F5F5")
        agregar_fondo_decorativo(self)
        empleados = employee_service.obtener_empleados_para_combobox()
        self.empleados_dict = {f"{nombre}": id for id, nombre in empleados}
        self.entry_style = {"border_width": 0, "fg_color": "#D9D9D9", "text_color": "#000000", "height": 40}
        self.boton_style = {"font": ("Georgia", 14), "text_color": "black", "height": 50}

        # === Estructura principal ===
        ctk.CTkLabel(self, text="REGISTRAR CONTRATO", font=("Georgia", 16), text_color="#06A051").pack(pady=(40, 0), padx=(250, 0), anchor="w")
        self.card = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card.place(relx=0.52, rely=0.52, anchor="center", relwidth=0.70, relheight=0.80)
        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_rowconfigure(0, weight=1)

        self.form_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.form_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        self.form_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self._crear_widgets()
        self.actualizar_campos_pago()

        botones_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        botones_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        botones_frame.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(botones_frame, text="Registrar", fg_color="#06A051", hover_color="#048B45", command=self.guardar_contrato, **self.boton_style, corner_radius=10).grid(row=0, column=0, padx=30, pady=30, sticky="ew")
        ctk.CTkButton(botones_frame, text="Cancelar", fg_color="#D12B1B", hover_color="#B81D0F", command=self.volver_callback, **self.boton_style, corner_radius=10).grid(row=0, column=1, padx=30, pady=30, sticky="ew")

    def _crear_widgets(self):
        # Campo nombre empleado
        self.crear_label_entry("Nombre empleado", 0, 0, 2, "entry_empleado")
        self.lista_empleados = ctk.CTkFrame(self.form_frame, fg_color="white", corner_radius=15, width=200)
        self.entry_empleado.empleados_dict = self.empleados_dict
        self.entry_empleado.bind("<KeyRelease>", crear_autocompletado(self.entry_empleado, self.lista_empleados, self.seleccionar_empleado))
        self.lista_empleados.place(x=0, y=0)
        self.lista_empleados.lower()

        # Tipo de contrato
        self.crear_option_menu("Tipo contrato", 0, 2, ["CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO", "CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO", "CONTRATO SERVICIO HORA CATEDRA", "CONTRATO APRENDIZAJE SENA", "ORDEN PRESTACION DE SERVICIOS"], "tipo_contrato_var", self.actualizar_campos_pago)
        
        # Fechas
        self.start_date = self.crear_label_entry("Fecha inicio", 2, 0, 1, "start_date")
        self.start_date.bind("<Button-1>", lambda e: self.abrir_calendario(self.start_date))
        self.end_date = self.crear_label_entry("Fecha fin", 2, 1, 1, "end_date")
        self.end_date.bind("<Button-1>", lambda e: self.abrir_calendario(self.end_date))
        
        # Campos de pago (creados en el mismo form_frame)
        self.label_mensualidad = ctk.CTkLabel(self.form_frame, text="Mensualidad", font=("Georgia", 12, "bold"))
        self.monthly_payment = ctk.CTkEntry(self.form_frame, placeholder_text="Mensualidad", **self.entry_style)
        self.label_transporte = ctk.CTkLabel(self.form_frame, text="Transporte", font=("Georgia", 12, "bold"))
        self.transport = ctk.CTkEntry(self.form_frame, placeholder_text="Transporte", **self.entry_style)
        
        self.label_valor_hora = ctk.CTkLabel(self.form_frame, text="Valor hora", font=("Georgia", 12, "bold"))
        self.value_hour = ctk.CTkEntry(self.form_frame, placeholder_text="Valor hora", **self.entry_style)
        self.label_numero_horas = ctk.CTkLabel(self.form_frame, text="Número de horas", font=("Georgia", 12, "bold"))
        self.number_hour = ctk.CTkEntry(self.form_frame, placeholder_text="Número de horas", **self.entry_style)

        self.label_pago_total = ctk.CTkLabel(self.form_frame, text="Pago total", font=("Georgia", 12, "bold"))
        self.total_payment = ctk.CTkEntry(self.form_frame, placeholder_text="Pago total", **self.entry_style)
        self.label_frecuencia_pago  = ctk.CTkLabel(self.form_frame, text="Número de Cuotas", font=("Georgia", 12, "bold"))
        self.payment_frequency = ctk.CTkEntry(self.form_frame, placeholder_text="Número de cuotas", **self.entry_style)
        # Otros campos que siempre son visibles
        self.crear_label_entry("Empleador", 4, 0, 2, "contractor")
        self.crear_option_menu("Estado", 4, 2, ["ACTIVO", "FINALIZADO", "RETIRADO"], "estado_var")

    def crear_label_entry(self, texto, fila, col, colspan=1, atributo="", parent_frame=None, placeholder=""):
        parent_frame = parent_frame or self.form_frame
        ctk.CTkLabel(parent_frame, text=texto, font=("Georgia", 12, "bold")).grid(row=fila, column=col, columnspan=colspan, sticky="w", pady=(5, 0), padx=5)
        entry = ctk.CTkEntry(parent_frame, placeholder_text=placeholder or texto, **self.entry_style)
        entry.grid(row=fila + 1, column=col, columnspan=colspan, padx=5, pady=(0, 10), sticky="ew")
        setattr(self, atributo, entry)
        return entry

    def crear_option_menu(self, texto, fila, col, opciones, atributo, command=None):
        ctk.CTkLabel(self.form_frame, text=texto, font=("Georgia", 12, "bold")).grid(row=fila, column=col, columnspan=2, sticky="w", pady=(5, 0), padx=5)
        var = ctk.StringVar(value=opciones[0])
        menu = ctk.CTkOptionMenu(self.form_frame, values=opciones, variable=var, fg_color="#D9D9D9", height=40, text_color="black", button_color="#06A051", button_hover_color="#048B45", dropdown_fg_color="white", dropdown_text_color="black", command=command)
        menu.grid(row=fila + 1, column=col, columnspan=2, padx=5, pady=(0, 10), sticky="ew")
        setattr(self, atributo, var)
        return menu

    def abrir_calendario(self, entry_widget):
        if self.calendario_abierto:
            self.calendario_abierto.destroy()
        
        self.calendario_abierto = tk.Toplevel(self)
        self.calendario_abierto.title("Seleccionar fecha")
        self.calendario_abierto.geometry("300x300+500+300")
        self.calendario_abierto.transient(self)
        self.calendario_abierto.grab_set()
        
        cal = Calendar(self.calendario_abierto, selectmode="day", date_pattern="dd/mm/yyyy")
        cal.pack(padx=10, pady=10)

        def seleccionar_fecha():
            fecha = cal.get_date()
            entry_widget.delete(0, "end")
            entry_widget.insert(0, fecha)
            self.calendario_abierto.grab_release()
            self.calendario_abierto.destroy()
            self.calendario_abierto = None

        def cerrar_calendario():
            self.calendario_abierto.grab_release()
            self.calendario_abierto.destroy()
            self.calendario_abierto = None

        tk.Button(self.calendario_abierto, text="Seleccionar", command=seleccionar_fecha).pack(pady=10)
        tk.Button(self.calendario_abierto, text="Cancelar", command=cerrar_calendario).pack(pady=5)
        self.calendario_abierto.protocol("WM_DELETE_WINDOW", cerrar_calendario)

    def actualizar_campos_pago(self, *args):
        # Lista de todos los widgets de pago
        pago_widgets = [self.label_mensualidad, self.monthly_payment, self.label_transporte, self.transport,
                        self.label_valor_hora, self.value_hour, self.label_numero_horas, self.number_hour,
                        self.label_pago_total, self.total_payment,self.label_frecuencia_pago, self.payment_frequency]

        # Ocultar todos los widgets de pago
        for widget in pago_widgets:
            widget.grid_remove()
        
        tipo_contrato = self.tipo_contrato_var.get()
        
        # Lógica para mostrar los widgets relevantes
        if tipo_contrato in ["CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO", "CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO", "CONTRATO APRENDIZAJE SENA"]:
            self.label_mensualidad.grid(row=2, column=2, sticky="w", pady=(5, 0), padx=5)
            self.monthly_payment.grid(row=3, column=2, padx=5, pady=(0, 10), sticky="ew")
            self.label_transporte.grid(row=2, column=3, sticky="w", pady=(5, 0), padx=5)
            self.transport.grid(row=3, column=3, padx=5, pady=(0, 10), sticky="ew")
            
            self.end_date.configure(state="normal", fg_color="#D9D9D9")
            self.end_date.bind("<Button-1>", lambda e: self.abrir_calendario(self.end_date))

            if tipo_contrato == "CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO":
                self.end_date.delete(0, "end")
                self.end_date.configure(state="disabled", fg_color="lightgray")
                self.end_date.unbind("<Button-1>")
            
            if tipo_contrato == "CONTRATO APRENDIZAJE SENA":
                salario_minimo = 1300000.00
                subsidio_transporte = 162000.00
                self.monthly_payment.insert(0, str(salario_minimo))
                self.transport.insert(0, str(subsidio_transporte))
            else:
                self.monthly_payment.delete(0, "end")
                self.transport.delete(0, "end")
                
        elif tipo_contrato == "CONTRATO SERVICIO HORA CATEDRA":
            self.label_valor_hora.grid(row=2, column=2, sticky="w", pady=(5, 0), padx=5)
            self.value_hour.grid(row=3, column=2, padx=5, pady=(0, 10), sticky="ew")
            self.label_numero_horas.grid(row=2, column=3, sticky="w", pady=(5, 0), padx=5)
            self.number_hour.grid(row=3, column=3, padx=5, pady=(0, 10), sticky="ew")
            
            self.end_date.configure(state="normal", fg_color="#D9D9D9")
            self.end_date.bind("<Button-1>", lambda e: self.abrir_calendario(self.end_date))
            
        elif tipo_contrato == 'ORDEN PRESTACION DE SERVICIOS':
            self.label_pago_total.grid(row=2, column=2, sticky="w", pady=(5, 0), padx=5)
            self.total_payment.grid(row=3, column=2, padx=5, pady=(0, 10), sticky="ew")

            self.label_frecuencia_pago.grid(row=2, column=3, sticky="w", pady=(5, 0), padx=5)
            self.payment_frequency.grid(row=3, column=3, padx=5, pady=(0, 10), sticky="ew")

    def guardar_contrato(self):
        empleado_nombre = self.entry_empleado.get()
        employee_id = self.empleados_dict.get(empleado_nombre)

        if employee_id is None:
            messagebox.showerror("Error", "Debes seleccionar un empleado válido.")
            return

        tipo_contrato = self.tipo_contrato_var.get()
        
        contrato_data = {
            'employee_id': employee_id,
            'type_contract': tipo_contrato,
            'start_date': self.start_date.get(),
            'end_date': self.end_date.get(),
            'state': self.estado_var.get(),
            'contractor': self.contractor.get(),
            'total_payment': float(self.total_payment.get()) if tipo_contrato == "ORDEN PRESTACION DE SERVICIOS" and self.total_payment.get() else 0.0,
            'payment_frequency': float(self.payment_frequency.get()) if tipo_contrato == "ORDEN PRESTACION DE SERVICIOS" and self.payment_frequency.get() else 0.0,
            'monthly_payment': float(self.monthly_payment.get()) if tipo_contrato in ["CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO", "CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO", "CONTRATO APRENDIZAJE SENA"] and self.monthly_payment.get() else 0.0,
            'transport': float(self.transport.get()) if tipo_contrato in ["CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO", "CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO", "CONTRATO APRENDIZAJE SENA"] and self.transport.get() else 0.0,
            'value_hour': float(self.value_hour.get()) if tipo_contrato == "CONTRATO SERVICIO HORA CATEDRA" and self.value_hour.get() else 0.0,
            'number_hour': float(self.number_hour.get()) if tipo_contrato == "CONTRATO SERVICIO HORA CATEDRA" and self.number_hour.get() else 0.0
        }

        try:
            contrato = Contrato(**contrato_data)
            contract_service.crear_contrato(contrato)
            messagebox.showinfo("Éxito", "Contrato registrado correctamente.")
            if self.volver_callback:
                self.volver_callback()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar contrato: {e}")

    def seleccionar_empleado(self, nombre):
        self.entry_empleado.delete(0, "end")
        self.entry_empleado.insert(0, nombre)
        self.lista_empleados.lower()
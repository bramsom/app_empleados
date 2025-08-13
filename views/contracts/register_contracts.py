import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from models.contract import Contrato
from controllers import contract_controller, employee_controller
from utils.canvas import agregar_fondo_decorativo
from services import contract_service, employee_service
from utils.autocomplete import crear_autocompletado


class RegistrarContrato(ctk.CTkFrame):
    def __init__(self, parent, username=None, rol=None, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback

        # Configuración visual general
        agregar_fondo_decorativo(self)
        self.configure(fg_color="#F5F5F5")

        # Obtener empleados
        empleados = employee_service.obtener_empleados_para_combobox()
        self.empleados_dict = {f"{nombre}": id for id, nombre in empleados}

        # ==== Estilos comunes ====
        entry_style = {
            "border_width": 0,
            "fg_color": "#D9D9D9",
            "text_color": "#000000",
            "height": 40
        }
        boton_style = {
            "font": ("Georgia", 14),
            "text_color": "black",
            "height": 50
        }

        # ==== Título ====
        ctk.CTkLabel(
            self, text="REGISTRAR CONTRATO", fg_color="transparent",
            font=("Georgia", 16), text_color="#06A051"
        ).pack(pady=(40, 0), padx=(250, 0), anchor="w")

        # ==== Tarjeta principal ====
        self.card = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card.place(relx=0.52, rely=0.52, anchor="center", relwidth=0.70, relheight=0.80)
        self.card.rowconfigure(0, weight=1)
        self.card.columnconfigure(0, weight=1)

        # ==== Formulario ====
        form_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        form_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        form_frame.columnconfigure((0, 1, 2, 3), weight=1)

        def crear_label_entry(texto, fila, col, colspan=1, atributo=""):
            ctk.CTkLabel(form_frame, text=texto, font=("Georgia", 12, "bold")).grid(
                row=fila, column=col, columnspan=colspan, sticky="w", pady=(5, 0), padx=5
            )
            entry = ctk.CTkEntry(form_frame, placeholder_text=texto, **entry_style)
            entry.grid(row=fila + 1, column=col, columnspan=colspan, padx=5, pady=(0, 10), sticky="ew")
            setattr(self, atributo, entry)

        # Campo nombre empleado
        crear_label_entry("Nombre empleado", 0, 0, 2, "entry_empleado")

        # Campo tipo contrato con OptionMenu
        ctk.CTkLabel(form_frame, text="Tipo contrato", font=("Georgia", 12, "bold")).grid(
            row=0, column=2, columnspan=2, sticky="w", pady=(5, 0), padx=5
        )
        opciones_tipo_contrato = [
            " ", "CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIGO",
            "CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO",
            "CONTRATO SERVICIO HORA CATEDRA",
            "CONTRATO APRENDIZAJE SENA",
            "ORDEN PRESTACION DE SERVICIOS"
        ]
        self.tipo_contrato_var = ctk.StringVar(value=opciones_tipo_contrato[0])
        tipo_contrato_menu = ctk.CTkOptionMenu(
            form_frame, values=opciones_tipo_contrato, variable=self.tipo_contrato_var,
            fg_color="#D9D9D9", height=40, text_color="black",
            button_color="#06A051", button_hover_color="#048B45",
            dropdown_fg_color="white", dropdown_text_color="black"
        )
        tipo_contrato_menu.grid(row=1, column=2, columnspan=2, padx=5, pady=(0, 10), sticky="ew")

        # ==== Fechas con calendario ====
        crear_label_entry("Fecha inicio", 2, 0, 1, "start_date")
        self.start_date.bind("<Button-1>", lambda e: self.abrir_calendario(self.start_date))

        crear_label_entry("Fecha fin", 2, 1, 1, "end_date")
        self.end_date.bind("<Button-1>", lambda e: self.abrir_calendario(self.end_date))

        # Otros campos
        crear_label_entry("valor hora", 2, 2, 1, "value_hour")
        crear_label_entry("Numero de horas", 2, 3, 1, "number_hour")
        crear_label_entry("Mensualidad", 4, 0, 1, "monthly_payment")
        crear_label_entry("Transporte", 4, 1, 1, "transport")
        crear_label_entry("Empleador", 4, 2, 2, "contractor")

        # Campo estado con OptionMenu
        ctk.CTkLabel(form_frame, text="Estado", font=("Georgia", 12, "bold")).grid(
            row=6, column=1,columnspan=2, sticky="w", pady=(5, 0), padx=5
        )
        opciones_estado = ["ACTIVO", "FINALIZADO", "RETIRADO"]
        self.estado_var = ctk.StringVar(value=opciones_estado[0])
        estado_menu = ctk.CTkOptionMenu(
            form_frame, values=opciones_estado, variable=self.estado_var,
            fg_color="#D9D9D9", height=40, text_color="black",
            button_color="#06A051", button_hover_color="#048B45",
            dropdown_fg_color="white", dropdown_text_color="black"
        )
        estado_menu.grid(row=7, column=1,columnspan=2, padx=5, pady=(0, 10), sticky="ew")

        # Autocompletado
        self.entry_empleado.empleados_dict = self.empleados_dict
        self.lista_empleados = ctk.CTkFrame(form_frame, fg_color="white", corner_radius=15, width=200)
        self.lista_empleados.place(x=0, y=0)
        self.lista_empleados.lower()
        self.entry_empleado.bind(
            "<KeyRelease>",
            crear_autocompletado(self.entry_empleado, self.lista_empleados, self.seleccionar_empleado)
        )

        # ==== Botones ====
        botones_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        botones_frame.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="ew")
        botones_frame.columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            botones_frame, text="Registrar", fg_color="#06A051", hover_color="#048B45",
            command=self.guardar_contrato, **boton_style, corner_radius=10
        ).grid(row=0, column=0, padx=30, pady=30, sticky="ew")
        ctk.CTkButton(
            botones_frame, text="Cancelar", fg_color="#D12B1B", hover_color="#B81D0F",
            command=self.volver_callback, **boton_style, corner_radius=10
        ).grid(row=0, column=1, padx=30, pady=30, sticky="ew")

    def abrir_calendario(self, entry_widget):
        top = tk.Toplevel(self)
        top.title("Seleccionar fecha")
        top.geometry("+500+300")

        cal = Calendar(top, selectmode="day", date_pattern="dd/mm/yyyy")
        cal.pack(padx=10, pady=10)

        def seleccionar_fecha():
            fecha = cal.get_date()
            entry_widget.delete(0, "end")
            entry_widget.insert(0, fecha)
            top.destroy()

        tk.Button(top, text="Seleccionar", command=seleccionar_fecha).pack(pady=10)

    def guardar_contrato(self):
        empleado_nombre = self.entry_empleado.get()
        employee_id = self.empleados_dict.get(empleado_nombre)

        if employee_id is None:
            messagebox.showerror("Error", "Debes seleccionar un empleado válido.")
            return

        contrato = Contrato(
            employee_id=employee_id,
            type_contract=self.tipo_contrato_var.get(),
            start_date=self.start_date.get(),
            end_date=self.end_date.get(),
            value_hour=self.value_hour.get(),
            number_hour=self.number_hour.get(),
            monthly_payment=self.monthly_payment.get(),
            transport=self.transport.get(),
            state=self.estado_var.get(),
            contractor=self.contractor.get()
        )

        contract_service.crear_contrato(contrato)
        messagebox.showinfo("Éxito", "Contrato registrado correctamente")
        if self.volver_callback:
            self.volver_callback()

    def seleccionar_empleado(self, nombre):
        self.entry_empleado.delete(0, "end")
        self.entry_empleado.insert(0, nombre)
        self.lista_empleados.lower()

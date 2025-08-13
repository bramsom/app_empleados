import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from datetime import datetime
from models.contract import Contrato
from controllers import contract_controller, employee_controller
from utils.canvas import agregar_fondo_decorativo
from services import contract_service, employee_service
from views.contracts.edit_contracts import EditarContrato
from utils.autocomplete import crear_autocompletado


class MostrarContrato(ctk.CTkFrame):
    def __init__(self, parent,contract_id, username=None, rol=None, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.contrato_id = contract_id

        # Configuración visual general
        agregar_fondo_decorativo(self)
        self.configure(fg_color="#F5F5F5")
        
        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))

        # Botón de regresar (puedes colocarlo donde prefieras, aquí un ejemplo arriba a la derecha)
        ctk.CTkButton(
            self,image=self.icon_back,text="",corner_radius=0,width=40,height=40,fg_color="#D2D2D2",hover_color="#E0E0E0",command=self.cancelar  # O el método que uses para volver a la tabla
        ).place(relx=0.98, rely=0.02, anchor="ne") 
        

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
            self, text="DETALLE CONTRATO", fg_color="transparent",
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
            botones_frame, text="Editar", fg_color="#06A051", hover_color="#048B45",
            command=self.abrir_editar_contrato, **boton_style, corner_radius=10
        ).grid(row=0, column=0, padx=30, pady=30, sticky="ew")


        self.cargar_datos()

    def cancelar(self):
        self.destroy()
        if self.volver_callback:
            self.volver_callback()

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

    def cargar_datos(self):
        contrato = contract_service.obtener_contrato_por_id(self.contrato_id)
        if not contrato:
            messagebox.showerror("Error", "No se encontró la afiliación.")
            if self.volver_callback:
                self.volver_callback()
            return

        (
            id_, employee_id, tipo, inicio, corte, valor_hora,
            num_horas, mensualidad, transporte, estado, contratante
        ) = contrato

        # Convertir fechas a formato dd/mm/yyyy para mostrar
        try:
            inicio_mostrar = datetime.strptime(inicio, '%Y-%m-%d').strftime('%d/%m/%Y')
        except Exception:
            inicio_mostrar = inicio
        try:
            corte_mostrar = datetime.strptime(corte, '%Y-%m-%d').strftime('%d/%m/%Y')
        except Exception:
            corte_mostrar = corte

        empleado_nombre = next((nombre for nombre, id in self.empleados_dict.items() if id == employee_id), "")
        self.entry_empleado.insert(0, empleado_nombre)
        self.tipo_contrato_var.set(tipo)
        self.start_date.insert(0, inicio_mostrar)
        self.end_date.insert(0, corte_mostrar)
        self.value_hour.insert(0, valor_hora)
        self.number_hour.insert(0, num_horas)
        self.monthly_payment.insert(0, mensualidad)
        self.transport.insert(0, transporte)
        self.contractor.insert(0, contratante)
        self.estado_var.set(estado)

    def abrir_editar_contrato(self):
        from views.contracts.search_contracts import BuscarContratos
        # Limpiar el área actual de contenido
        for widget in self.master.winfo_children():
            widget.destroy()
        EditarContrato(
            parent=self.master,
            contract_id=self.contrato_id,
            username=self.username,
            rol=self.rol,
            volver_callback=lambda: BuscarContratos(self.master, self.username, self.rol).pack(fill="both", expand=True)
        ).pack(fill="both", expand=True)

    def seleccionar_empleado(self, nombre):
        self.entry_empleado.delete(0, "end")
        self.entry_empleado.insert(0, nombre)
        self.lista_empleados.lower()

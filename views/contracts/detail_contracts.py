import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from datetime import datetime
from services import contract_service, employee_service
from views.contracts.edit_contracts import EditarContrato
from utils.canvas import agregar_fondo_decorativo


class MostrarContrato(ctk.CTkFrame):
    def __init__(self, parent, contract_id, username=None, rol=None, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.contrato_id = contract_id

        self._setup_estilos()
        self._setup_ui()
        self.cargar_datos()

    def _setup_estilos(self):
        """Define estilos y recursos comunes."""
        self.configure(fg_color="#F5F5F5")
        agregar_fondo_decorativo(self)
        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))
        self.entry_style = {
            "border_width": 0, "fg_color": "#D9D9D9", "text_color": "#000000",
            "height": 40, "state": "readonly"
        }
        self.label_style = {"font": ("Georgia", 12, "bold")}
        self.title_style = {"font": ("Georgia", 16), "text_color": "#06A051"}

    def _setup_ui(self):
        """Crea y posiciona todos los widgets de la interfaz."""
        # Botón de regresar
        ctk.CTkButton(
            self, image=self.icon_back, text="", corner_radius=0, width=40, height=40,
            fg_color="#D2D2D2", hover_color="#E0E0E0", command=self.cancelar
        ).place(relx=0.98, rely=0.02, anchor="ne")

        # Título de la vista
        ctk.CTkLabel(self, text="DETALLE CONTRATO", fg_color="transparent", **self.title_style).pack(
            pady=(40, 0), padx=(250, 0), anchor="w")

        # Tarjeta principal
        self.card = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card.place(relx=0.52, rely=0.52, anchor="center", relwidth=0.70, relheight=0.80)
        self.card.rowconfigure(0, weight=1)
        self.card.columnconfigure(0, weight=1)

        # Formulario
        self.form_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.form_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        self.form_frame.columnconfigure((0, 1, 2, 3), weight=1)

        self._crear_widgets()
        self._ocultar_todos_los_campos_pago()

        # Botón de edición
        ctk.CTkButton(
            self.card, text="Editar Contrato", fg_color="#06A051", hover_color="#048B45",
            command=self.abrir_editar_contrato, font=("Georgia", 14), text_color="black", height=50, corner_radius=10
        ).grid(row=1, column=0, padx=30, pady=30, sticky="ew")

    def _crear_widgets(self):
        """Crea todos los widgets del formulario."""
        # Helper para crear labels y entries de forma dinámica
        def create_field(text, row, col, colspan, attr_name, placeholder=""):
            label = ctk.CTkLabel(self.form_frame, text=text, **self.label_style)
            label.grid(row=row, column=col, columnspan=colspan, sticky="w", pady=(5, 0), padx=5)
            entry = ctk.CTkEntry(self.form_frame, placeholder_text=placeholder or text, **self.entry_style)
            entry.grid(row=row + 1, column=col, columnspan=colspan, padx=5, pady=(0, 10), sticky="ew")
            setattr(self, attr_name, entry)
            return label, entry

        # Campos comunes
        self.entry_empleado = create_field("Nombre Empleado", 0, 0, 2, "entry_empleado")[1]
        
        # Campo tipo contrato (usando un Label para modo detalle)
        ctk.CTkLabel(self.form_frame, text="Tipo Contrato", **self.label_style).grid(row=0, column=2, columnspan=2, sticky="w", pady=(5, 0), padx=5)
        self.tipo_contrato_var = ctk.StringVar(value="")
        self.label_tipo_contrato = ctk.CTkLabel(self.form_frame, textvariable=self.tipo_contrato_var, font=("Georgia", 12), text_color="black", fg_color="#D9D9D9", height=40)
        self.label_tipo_contrato.grid(row=1, column=2, columnspan=2, padx=5, pady=(0, 10), sticky="ew")

        self.start_date = create_field("Fecha Inicio", 2, 0, 1, "start_date")[1]
        self.end_date = create_field("Fecha Fin", 2, 1, 1, "end_date")[1]
        self.contractor = create_field("Contratante", 4, 0, 2, "contractor")[1]

        # Campo estado (usando un Label)
        ctk.CTkLabel(self.form_frame, text="Estado", **self.label_style).grid(row=4, column=2, columnspan=2, sticky="w", pady=(5, 0), padx=5)
        self.estado_var = ctk.StringVar(value="")
        self.label_estado = ctk.CTkLabel(self.form_frame, textvariable=self.estado_var, font=("Georgia", 12), text_color="black", fg_color="#D9D9D9", height=40)
        self.label_estado.grid(row=5, column=2, columnspan=2, padx=5, pady=(0, 10), sticky="ew")

        # Crear los labels y entries de pago una sola vez
        self.label_pago1 = ctk.CTkLabel(self.form_frame, text="", **self.label_style)
        self.label_pago2 = ctk.CTkLabel(self.form_frame, text="", **self.label_style)
        self.entry_pago1 = ctk.CTkEntry(self.form_frame, **self.entry_style)
        self.entry_pago2 = ctk.CTkEntry(self.form_frame, **self.entry_style)

    def _ocultar_todos_los_campos_pago(self):
        """Oculta todos los widgets de pago."""
        self.label_pago1.grid_remove()
        self.label_pago2.grid_remove()
        self.entry_pago1.grid_remove()
        self.entry_pago2.grid_remove()

    def _fill_entry_field(self, entry_widget, value):
        """Helper para rellenar un campo de entrada."""
        entry_widget.configure(state="normal")
        entry_widget.delete(0, "end")
        entry_widget.insert(0, value or "")
        entry_widget.configure(state="readonly")

    def _format_date(self, date_str):
        """Formatea una cadena de fecha de YYYY-MM-DD a DD/MM/YYYY."""
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
        except (ValueError, TypeError):
            return date_str or ""

    def _format_money(self, value):
        """Formatea un número con signo de peso y separador de miles."""
        if value is None:
            return ""
        try:
            return f"$ {float(value):,.0f}".replace(",", ".")
        except (ValueError, TypeError):
            return str(value)

    def cargar_datos(self):
        """Obtiene datos del servicio y rellena la interfaz."""
        contrato_data = contract_service.obtener_contrato_por_id(self.contrato_id)
        if not contrato_data:
            messagebox.showerror("Error", "No se encontró el contrato.")
            if self.volver_callback:
                self.volver_callback()
            return
    
        (
            id_, employee_id, empleado_nombre, type_contract, start_date, end_date, state,
            contractor, total_payment, payment_frequency, monthly_payment, transport,
            value_hour, number_hour, new_total_payment, new_payment_frequency
        ) = contrato_data

        # Rellenar campos comunes
        self._fill_entry_field(self.entry_empleado, empleado_nombre)
        self._fill_entry_field(self.start_date, self._format_date(start_date))
        self._fill_entry_field(self.end_date, self._format_date(end_date))
        self._fill_entry_field(self.contractor, contractor)
        self.tipo_contrato_var.set(type_contract)
        self.estado_var.set(state)
        self._mostrar_campos_pago(
            type_contract, monthly_payment, transport, value_hour,
            number_hour, new_total_payment, new_payment_frequency
        )
    def _mostrar_campos_pago(self, type_contract, monthly_payment, transport, value_hour, number_hour, total_payment, payment_frequency):
        """Muestra y rellena los campos de pago según el tipo de contrato."""
        self._ocultar_todos_los_campos_pago()
        
        campos_a_mostrar = []
        if type_contract in ['CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO', 'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO', 'CONTRATO APRENDIZAJE SENA']:
            campos_a_mostrar = [
                ("Mensualidad", self._format_money(monthly_payment)),
                ("Transporte", self._format_money(transport))
            ]
        elif type_contract == 'CONTRATO SERVICIO HORA CATEDRA':
            campos_a_mostrar = [
                ("Valor Hora", self._format_money(value_hour)),
                ("Número de Horas", number_hour)
            ]
        elif type_contract == 'ORDEN PRESTACION DE SERVICIOS':
            campos_a_mostrar = [
                ("Pago Total", self._format_money(total_payment)),
                ("Frecuencia de Pago", payment_frequency)
            ]
        
        if len(campos_a_mostrar) == 2:
            # Mostrar primer campo
            self.label_pago1.configure(text=campos_a_mostrar[0][0])
            self._fill_entry_field(self.entry_pago1, campos_a_mostrar[0][1])
            self.label_pago1.grid(row=2, column=2, sticky="w", pady=(5, 0), padx=5)
            self.entry_pago1.grid(row=3, column=2, padx=5, pady=(0, 10), sticky="ew")

            # Mostrar segundo campo
            self.label_pago2.configure(text=campos_a_mostrar[1][0])
            self._fill_entry_field(self.entry_pago2, campos_a_mostrar[1][1])
            self.label_pago2.grid(row=2, column=3, sticky="w", pady=(5, 0), padx=5)
            self.entry_pago2.grid(row=3, column=3, padx=5, pady=(0, 10), sticky="ew")

    def cancelar(self):
        self.destroy()
        if self.volver_callback:
            self.volver_callback()

    def abrir_editar_contrato(self):
        from views.contracts.search_contracts import BuscarContratos
        for widget in self.master.winfo_children():
            widget.destroy()
        EditarContrato(
            parent=self.master,
            contract_id=self.contrato_id,
            username=self.username,
            rol=self.rol,
            volver_callback=lambda: BuscarContratos(self.master, self.username, self.rol).pack(fill="both", expand=True)
        ).pack(fill="both", expand=True)
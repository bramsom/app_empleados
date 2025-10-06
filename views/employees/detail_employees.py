import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from datetime import datetime
from models.contract import Contrato
from controllers import contract_controller, affiliation_controller, employee_controller
from utils.canvas import agregar_fondo_decorativo
from services import contract_service, employee_service
from views.contracts.edit_contracts import EditarContrato
from views.employees.edit_employees import EditarEmpleado
from utils.autocomplete import crear_autocompletado
from views.contracts.register_contracts import RegistrarContrato # Importar la vista de registro

class MostrarEmpleado(ctk.CTkFrame):
    def __init__(self, parent, employee_id, username=None, rol=None, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.empleado_id = employee_id

        self.configure(fg_color="#F2F2F2")
        agregar_fondo_decorativo(self)
        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))

        # Configuración principal del grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Título y botón "Volver" directamente en el frame principal
        self.title_label = ctk.CTkLabel(
            self,
            text="", # Se actualiza con el nombre del empleado en cargar_datos_empleado
            font=("Georgia", 20, "bold"),
            text_color="#282828",
            fg_color="#F5F5F5"
        )
        self.title_label.grid(row=0, column=0, sticky="w", padx=(115, 3), pady=20)

        ctk.CTkButton(
            self,
            image=self.icon_back,
            text="",
            corner_radius=0,
            width=40,
            height=40,
            fg_color="#D2D2D2",
            hover_color="#E0E0E0",
            command=self.cancelar
        ).grid(row=0, column=1, sticky="e", padx=(0, 20), pady=3)

        # Frame general para las tarjetas
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="#F5F5F5", corner_radius=10)
        self.main_frame.grid(row=1, column=0, columnspan=2, padx=(100, 50), pady=3, sticky="nsew")

        # Botones de acción, colocados directamente en la cuadrícula principal
        btn_editar = ctk.CTkButton(self,height=40,width=200, text="Editar empleado", fg_color="#06A051", text_color="black", hover_color="#088D48",font=("Georgia", 14),command=self.editar_empleado_callback)
        btn_editar.grid(row=2, column=0, padx=(110, 10), pady=(20, 60), sticky="w")

        btn_nuevo_contrato = ctk.CTkButton(self,height=40,width=200, text="Nuevo contrato", fg_color="#06A051", text_color="black", hover_color="#088D48",font=("Georgia", 14),command=self.crear_contrato_callback)
        btn_nuevo_contrato.grid(row=2, column=0, padx=(340, 10), pady=(20, 60), sticky="w")
        
        btn_eliminar = ctk.CTkButton(self,height=40,width=200, text="Eliminar empleado", fg_color="#D12B1B", text_color="black", hover_color="#BB1E10",font=("Georgia", 14), command=self.eliminar_empleado)
        btn_eliminar.grid(row=2, column=0, padx=(570, 10), pady=(20, 60), sticky="w")

        # Cargar los datos iniciales
        self.cargar_datos_empleado()

    def limpiar_vista(self):
        """Limpia todos los widgets del frame principal para recargar los datos."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        
    def cargar_datos_empleado(self):
        """Carga y muestra la información completa del empleado."""
        self.limpiar_vista()

        self.empleado = employee_service.obtener_empleado_por_id(self.empleado_id)
        if not self.empleado:
            messagebox.showerror("Error", "Empleado no encontrado.")
            if self.volver_callback:
                self.volver_callback()
            return
        
        self.title_label.configure(text=f"DETALLES DE {self.empleado.name} {self.empleado.last_name}")

        self.afiliaciones = affiliation_controller.consultar_afiliaciones_por_empleado(self.empleado.id)
        self.contratos = contract_controller.consultar_contratos_por_empleado(self.empleado.id)
        
        # Configurar la cuadrícula del main_frame para que las tarjetas se adapten
        self.main_frame.grid_columnconfigure((0, 1), weight=1)

        # Contenedor para la fila superior con "Datos Personales" y "Afiliaciones"
        top_row_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_row_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        top_row_frame.grid_columnconfigure((0, 1), weight=1)

        # Marco de información del empleado (izquierda)
        info_empleado_frame = ctk.CTkFrame(top_row_frame, fg_color="#FFFFFF", corner_radius=10)
        info_empleado_frame.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        info_empleado_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.mostrar_info_empleado(info_empleado_frame)

        # Marco de información de afiliación (derecha)
        info_afiliacion_frame = ctk.CTkFrame(top_row_frame, fg_color="#FFFFFF", corner_radius=10)
        info_afiliacion_frame.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        info_afiliacion_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.mostrar_afiliaciones(info_afiliacion_frame)

        # Contenedor de contratos (debajo)
        contratos_frame = ctk.CTkFrame(self.main_frame, fg_color="#FFFFFF", corner_radius=10)
        contratos_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
        self.mostrar_contratos(contratos_frame)

    def crear_campo(self, parent_frame, label, valor, fila, columna, colspan=1, padx=10, pady=10):
        """Función para crear un campo de información con estilo de burbuja."""
        frame = ctk.CTkFrame(parent_frame, fg_color="#B0B0B0", corner_radius=6)
        frame.grid(row=fila, column=columna, columnspan=colspan, padx=padx, pady=pady, sticky="nsew")
        ctk.CTkLabel(frame, text=label, font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
        ctk.CTkLabel(frame, text=valor or "-", font=("arial", 11), anchor="w", justify="left",
                      corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")

    def mostrar_info_empleado(self, parent_frame):
        ctk.CTkLabel(
            parent_frame,
            text="DATOS PERSONALES",
            font=("Georgia", 16),
            text_color="#06A051"
        ).grid(row=0, column=0, columnspan=5, sticky="w", padx=10, pady=5)

        campos = [
            ("Nombre:", f"{self.empleado.name} {self.empleado.last_name}", 1, 0, 2),
            ("Tipo documento:", self.empleado.document_type, 1, 2),
            ("Número documento:", self.empleado.document_number, 1, 3),
            ("Expedida en:", self.empleado.document_issuance, 1, 4),
            ("Fecha nacimiento:", self.empleado.birthdate, 2, 0),
            ("No telefono:", self.empleado.phone_number, 2, 1),
            ("Dirección residencia:", self.empleado.residence_address, 2, 2, 2),
            ("RUT:", self.empleado.RUT, 2, 4),
            ("Correo electrónico:", self.empleado.email, 3, 0, 2),
            ("Cargo:", self.empleado.position, 3, 2),
        ]
        
        for campo in campos:
            self.crear_campo(parent_frame, *campo)

    def mostrar_afiliaciones(self, parent_frame):
        ctk.CTkLabel(
            parent_frame,
            text="AFILIACIONES",
            font=("Georgia", 16,),
            text_color="#06A051"
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=5)

        if not self.afiliaciones:
            ctk.CTkLabel(parent_frame, text="Sin afiliaciones registradas", text_color="gray").grid(row=1, column=0, columnspan=3, padx=10, pady=5)
            return

        # Asume que un empleado solo tiene una afiliación para el diseño de tarjeta
        afiliacion = self.afiliaciones[0]

        # Lista de campos: (Etiqueta, Valor, Fila, Columna, Columnspan)
        campos_afiliaciones = [
            ("EPS:", afiliacion.eps, 1, 0),
            ("ARL:", afiliacion.arl, 1, 1),
            ("Nivel riesgo:", afiliacion.risk_level, 1, 2),
            ("AFP:", afiliacion.afp, 2, 0),
            ("Caja compensacion:", afiliacion.compensation_box, 2, 1, 2),
            ("Banco:", afiliacion.bank, 3, 0),
            ("No cuenta:", afiliacion.account_number, 3, 1),
            ("Tipo cuenta:", afiliacion.account_type, 3, 2)
        ]

        for campo in campos_afiliaciones:
            self.crear_campo(parent_frame, *campo)

    def mostrar_contratos(self, parent_frame):
        ctk.CTkLabel(
            parent_frame,
            text="CONTRATOS",
            font=("Georgia", 16),
            text_color="#06A051"
        ).grid(row=0, column=0, columnspan=10, sticky="w", padx=10, pady=5)

        if not self.contratos:
            ctk.CTkLabel(parent_frame, text="Sin contratos registrados", text_color="gray").grid(row=1, column=0, padx=10, pady=5)
            return

        # Configurar la columna del `parent_frame` donde irán los contratos para que se expanda
        parent_frame.grid_columnconfigure(0, weight=1)

        for idx, contrato in enumerate(self.contratos):
            fila_contrato = idx + 1
            
            # Un solo frame para toda la fila del contrato, actuando como una "tarjeta"
            contrato_frame = ctk.CTkFrame(parent_frame, fg_color="#FFFFFF", corner_radius=10)
            # Usar 'sticky="ew"' para expandir en la dirección este-oeste
            contrato_frame.grid(row=fila_contrato, column=0, pady=5, padx=10, sticky="ew")
            
            # Recolectar todos los campos para el contrato actual
            campos_contrato = [
                ("Fecha de inicio:", contrato.start_date),
                ("Fecha de corte:", contrato.end_date or "Actual"),
                ("Tipo de contrato:", contrato.type_contract),
                ("Estado:", contrato.state),
                ("Empleador:", contrato.contractor or "-")
            ]

            if contrato.type_contract in ['CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO', 'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO', 'CONTRATO APRENDIZAJE SENA']:
                campos_contrato.extend([
                    ("Mensualidad:", f"${contrato.monthly_payment:,.2f}" if contrato.monthly_payment is not None else "-"),
                    ("Transporte:", f"${contrato.transport:,.2f}" if contrato.transport is not None else "-")
                ])
            elif contrato.type_contract == 'CONTRATO SERVICIO HORA CATEDRA':
                campos_contrato.extend([
                    ("Valor hora:", f"${contrato.value_hour:,.2f}" if contrato.value_hour is not None else "-"),
                    ("No horas:", contrato.number_hour or "-")
                ])
            elif contrato.type_contract == 'ORDEN PRESTACION DE SERVICIOS':
                campos_contrato.extend([
                    ("Valor total:", f"${contrato.total_payment:,.2f}" if contrato.total_payment is not None else "-"),
                    ("Frecuencia de pago:", contrato.payment_frequency or "-")
                ])
            
            # Configurar las columnas dentro del frame del contrato para que se expandan uniformemente
            for i in range(len(campos_contrato)):
                contrato_frame.grid_columnconfigure(i, weight=1)
            
            # Crear y ubicar las etiquetas de forma individual dentro del frame del contrato
            for i, (label, value) in enumerate(campos_contrato):
                inner_frame = ctk.CTkFrame(contrato_frame, fg_color="#A0A0A0", corner_radius=6)
                inner_frame.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
                ctk.CTkLabel(inner_frame, text=label, font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
                ctk.CTkLabel(inner_frame, text=value, font=("arial", 11), anchor="w", justify="left", corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")

    def crear_contrato_callback(self):
        # Ocultar la vista actual
        self.pack_forget()
        # Navegar a la vista de registro de contratos, pasando el ID del empleado
        registrar_contrato_view = RegistrarContrato(
            parent=self.master, 
            employee_id=self.empleado_id, 
            volver_callback=self.volver_a_detalle
        )
        registrar_contrato_view.pack(fill="both", expand=True)

    def volver_a_detalle(self):
        # Destruir la vista de registro de contratos
        for widget in self.master.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self:
                widget.destroy()
        
        # Volver a mostrar la vista de detalle y recargar los datos
        self.pack(fill="both", expand=True)
        self.cargar_datos_empleado()

    def eliminar_empleado(self):
        """
        Maneja la eliminación de un empleado después de la confirmación del usuario.
        """
        # Mostrar cuadro de diálogo de confirmación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar a {self.empleado.name} {self.empleado.last_name}?\nEsta acción es irreversible y también eliminará todos sus contratos y afiliaciones."
        )

        # Si el usuario confirma
        if respuesta:
            try:
                # Lógica para eliminar el empleado
                if employee_controller.eliminar_empleado(self.empleado.id):
                    messagebox.showinfo("Éxito", f"Empleado {self.empleado.name} {self.empleado.last_name} eliminado correctamente.")
                    self.cancelar() # Volver a la vista anterior después de la eliminación
                else:
                    messagebox.showerror("Error", "No se pudo eliminar al empleado.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al intentar eliminar el empleado: {e}")

    def editar_empleado_callback(self):
        """Muestra la vista para editar la información del empleado."""
        self.pack_forget()
        editar_empleado_view = EditarEmpleado(
            parent=self.master,
            employee_id=self.empleado_id,
            volver_callback=self.volver_a_detalle
        )
        editar_empleado_view.pack(fill="both", expand=True)
    def cancelar(self):
        self.destroy()
        if self.volver_callback:
            self.volver_callback()

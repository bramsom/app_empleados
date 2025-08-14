import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from datetime import datetime
from models.contract import Contrato
from controllers import contract_controller, affiliation_controller, employee_controller
from utils.canvas import agregar_fondo_decorativo
from services import contract_service, employee_service 
from views.contracts.edit_contracts import EditarContrato
from utils.autocomplete import crear_autocompletado


class MostrarEmpleado(ctk.CTkFrame):
    def __init__(self, parent, employee_id, username=None, rol=None, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.empleado_id = employee_id

        # --- Cargar el objeto Empleado aquí ---
        # Asumo que employee_service.consultar_empleado_por_id existe y retorna un objeto Empleado o None
        self.empleado = employee_service.obtener_empleado_por_id(self.empleado_id)

        if not self.empleado:
            # Si el empleado no se encuentra, puedes mostrar un mensaje y/o volver a la vista anterior
            messagebox.showerror("Error", "Empleado no encontrado.")
            if self.volver_callback:
                self.volver_callback()
            return # Detiene la ejecución si no hay empleado

        agregar_fondo_decorativo(self)

        # Frame general
        self.card2 = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card2.place(relx=0.52, rely=0.5, anchor="center", relwidth=0.92, relheight=0.80)
        self.frame_detalle = ctk.CTkScrollableFrame(self.card2, fg_color="transparent")
        self.frame_detalle.pack(fill="both", expand=True, padx=0, pady=0)

        # Contenedor superior con dos columnas
        fila_superior = ctk.CTkFrame(self.frame_detalle, fg_color="#F3EFEF")
        fila_superior.pack(fill="x", padx=0, pady=0)
        fila_superior.grid_columnconfigure((0, 1), weight=1)

        # Configurar título y columnas
        card_info = ctk.CTkFrame(fila_superior, fg_color="#F5F5F5", corner_radius=10)
        card_info.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        card_info.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        def crear_campo(label, valor, fila, columna, colspan=1):
            frame = ctk.CTkFrame(card_info, fg_color="#B0B0B0", corner_radius=6)
            frame.grid(row=fila, column=columna, columnspan=colspan, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(frame, text=label, font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(frame, text=valor or "-", font=("arial", 11), anchor="w", justify="left",
                         corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")

        ctk.CTkLabel(card_info, text="DATOS PERSONALES", font=("Georgia", 16), text_color="#06A051").grid(
            row=0, column=0, columnspan=5, sticky="w", padx=10, pady=5
        )

        # Lista de campos: (Etiqueta, Valor, Fila, Columna, Columnspan)
        # Usa self.empleado para acceder a los datos
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

        # Crear los campos con la función
        for campo in campos:
            crear_campo(*campo)


        # Tarjeta: Afiliaciones
        card_afiliaciones = ctk.CTkFrame(fila_superior, fg_color="#F5F5F5", corner_radius=10)
        card_afiliaciones.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(card_afiliaciones, text="AFILIACIONES", font=("Georgia", 16,), text_color="#06A051").grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=5)

        # Usa self.empleado.id para consultar afiliaciones
        afiliaciones = affiliation_controller.consultar_afiliaciones_por_empleado(self.empleado.id)

        # Define ancho y alto fijo para los campos

        if afiliaciones:
            # Asume que un empleado solo tiene una afiliación para el diseño de tarjeta
            afiliacion = afiliaciones[0]

            # Fila 1
            # EPS
            contenedor_eps = ctk.CTkFrame(card_afiliaciones, fg_color="#B0B0B0", corner_radius=6, width=250, height=60)
            contenedor_eps.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(contenedor_eps, text="EPS:", font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(contenedor_eps, text=afiliacion.eps,font=("arial", 11), fg_color="transparent", corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")

            # ARL
            contenedor_arl = ctk.CTkFrame(card_afiliaciones, fg_color="#B0B0B0", corner_radius=6, width=250, height=60)
            contenedor_arl.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(contenedor_arl, text="ARL:", font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(contenedor_arl, text=afiliacion.arl,font=("arial", 11), fg_color="transparent", corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")

            # Nivel de Riesgo
            contenedor_riesgo = ctk.CTkFrame(card_afiliaciones, fg_color="#B0B0B0", corner_radius=6, width=250, height=60)
            contenedor_riesgo.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(contenedor_riesgo, text="Nivel riesgo:", font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(contenedor_riesgo, text=afiliacion.risk_level,font=("arial", 11), fg_color="transparent", corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")

            # Fila 2
            # AFP
            contenedor_afp = ctk.CTkFrame(card_afiliaciones, fg_color="#B0B0B0", corner_radius=6, width=250, height=60)
            contenedor_afp.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(contenedor_afp, text="AFP:", font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(contenedor_afp, text=afiliacion.afp,font=("arial", 11), fg_color="transparent", corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")

            # Caja de Compensacion (ocupa 2 columnas)
            contenedor_caja = ctk.CTkFrame(card_afiliaciones, fg_color="#B0B0B0", corner_radius=6, height=60, width=520)
            contenedor_caja.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(contenedor_caja, text="Caja compensacion:", font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(contenedor_caja, text=afiliacion.compensation_box,font=("arial", 11), fg_color="transparent", corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")

            # Fila 3
            # Banco
            contenedor_banco = ctk.CTkFrame(card_afiliaciones, fg_color="#B0B0B0", corner_radius=6, width=250, height=60)
            contenedor_banco.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(contenedor_banco, text="Banco:", font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(contenedor_banco, text=afiliacion.bank,font=("arial", 11), fg_color="transparent", corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")

            # No Cuenta
            contenedor_cuenta = ctk.CTkFrame(card_afiliaciones, fg_color="#B0B0B0", corner_radius=6, width=250, height=60)
            contenedor_cuenta.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(contenedor_cuenta, text="No cuenta:", font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(contenedor_cuenta, text=afiliacion.account_number,font=("arial", 11), fg_color="transparent", corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")

            # Tipo de Cuenta
            contenedor_tipo_cuenta = ctk.CTkFrame(card_afiliaciones, fg_color="#B0B0B0", corner_radius=6, width=50, height=60)
            contenedor_tipo_cuenta.grid(row=3, column=2, padx=10, pady=10, sticky="nsew")
            ctk.CTkLabel(contenedor_tipo_cuenta, text="Tipo cuenta:", font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(contenedor_tipo_cuenta, text=afiliacion.account_type, font=("arial", 11),fg_color="transparent", corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")

        else:
            ctk.CTkLabel(card_afiliaciones, text="Sin afiliaciones registradas", text_color="gray").grid(row=1, column=0, columnspan=3, padx=10, pady=5)
        
        card_contratos = ctk.CTkFrame(self.frame_detalle, fg_color="#F5F5F5", corner_radius=10)
        card_contratos.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(card_contratos, text="CONTRATOS", font=("Georgia", 16), text_color="#06A051").grid(row=0, column=0, columnspan=10, sticky="w", padx=10, pady=5)

        # Usa self.empleado.id para consultar contratos
        contratos = contract_controller.consultar_contratos_por_empleado(self.empleado.id)
        if contratos:
            for idx, contrato in enumerate(contratos):
                fila = idx + 1
                columnas = [
                    ("Fecha de inicio:", contrato.start_date),
                    ("Fecha de corte:", contrato.end_date or "Actual"),
                    ("Tipo de contrato:", contrato.type_contract),
                    ("valor hora:", f"${contrato.value_hour:,.2f}"),
                    ("No horas:", contrato.number_hour),
                    ("Mensualida:", f"${contrato.monthly_payment:,.2f}"),
                    ("Transporte:", f"${contrato.transport:,.2f}"),
                    ("Estado:", contrato.state),
                    ("Empleador:", contrato.contractor or "-")
                ]
                for col_idx, (etq, val) in enumerate(columnas):
                    contenedor = ctk.CTkFrame(card_contratos, fg_color="#B0B0B0", corner_radius=6)
                    contenedor.grid(row=fila, column=col_idx, padx=6, pady=5, sticky="nsew")

                    ctk.CTkLabel(contenedor, text=etq, font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
                    ctk.CTkLabel(contenedor, text=val,font=("Arial", 11), fg_color="#A0A0A0", corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")
        else:
            ctk.CTkLabel(card_contratos, text="Sin contratos registrados", text_color="gray").grid(row=1, column=0, padx=10, pady=5)
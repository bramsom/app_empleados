import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from datetime import datetime
from models.employee import Empleado
from controllers import contract_controller, employee_controller
from utils.canvas import agregar_fondo_decorativo
from services import employee_service
from utils.autocomplete import crear_autocompletado


class EditarEmpleado(ctk.CTkFrame):
    def __init__(self, parent,employee_id, username=None, rol=None, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.empleado_id = employee_id


        # Configuración visual general
        agregar_fondo_decorativo(self)
        self.configure(fg_color="#F5F5F5")

        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))

        # Botón de regresar (puedes colocarlo donde prefieras, aquí un ejemplo arriba a la derecha)
        ctk.CTkButton(
            self,image=self.icon_back,text="",width=40,height=40,fg_color="#D2D2D2",corner_radius=0,hover_color="#E0E0E0",command=self.cancelar  # O el método que uses para volver a la tabla
        ).place(relx=0.98, rely=0.02, anchor="ne")

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
            self, text="EDITAR INFORMACION EMPLEADO", fg_color="transparent",
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
        crear_label_entry("Nombres ", 0, 0, 2, "name")
        crear_label_entry("Apellidos ", 0, 2, 2, "last_name")
        # Campo tipo contrato con OptionMenu
        ctk.CTkLabel(form_frame, text="Tipo documento", font=("Georgia", 12, "bold")).grid(
            row=2, column=0, columnspan=1, sticky="w", pady=(5, 0), padx=5
        )
        opciones_tipo_documento = [
            " ", "C.C.", "T.I.", "C.E.", "NIT", "RUT"
        ]
        self.tipo_documento_var = ctk.StringVar(value=opciones_tipo_documento[0])
        tipo_documento_menu = ctk.CTkOptionMenu(
            form_frame, values=opciones_tipo_documento, variable=self.tipo_documento_var,
            fg_color="#D9D9D9", height=40, text_color="black",
            button_color="#06A051", button_hover_color="#048B45",
            dropdown_fg_color="white", dropdown_text_color="black"
        )
        tipo_documento_menu.grid(row=3, column=0, columnspan=1, padx=5, pady=(0, 10), sticky="ew")

        # ==== Fechas con calendario ====
        crear_label_entry("Numero de documento", 2, 1, 1, "document_number")

        crear_label_entry("Expedicion de documento", 2, 2, 1, "document_issuance")

        crear_label_entry("Fecha de nacimiento", 2, 3, 1, "birthdate")
        self.birthdate.bind("<Button-1>", lambda e: self.abrir_calendario(self.birthdate))

        # Otros campos
        crear_label_entry("Numero de telefono", 4, 0, 1, "phone_number")
        crear_label_entry("Direccion de residencia", 4, 1, 2, "residence_address")
        crear_label_entry("RUT", 4, 3, 1, "RUT")
        crear_label_entry("Correo electronico", 6, 0, 4, "email")

        # ==== Botones ====
        botones_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        botones_frame.grid(row=3, column=0, columnspan=4, pady=10, padx=10, sticky="ew")
        botones_frame.columnconfigure((0, 1), weight=1)

        ctk.CTkButton(
            botones_frame, text="Guardar cambios", fg_color="#06A051", hover_color="#048B45",
            command=self.guardar_cambios, **boton_style, corner_radius=10
        ).grid(row=0, column=0, padx=30, pady=30, sticky="ew")
        ctk.CTkButton(
            botones_frame, text="Cancelar", fg_color="#D12B1B", hover_color="#B81D0F",
            command=self.cancelar, **boton_style, corner_radius=10
        ).grid(row=0, column=1, padx=30, pady=30, sticky="ew")

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
        empleado = employee_service.obtener_empleado_por_id(self.empleado_id)
        if not empleado:
            messagebox.showerror("Error", "No se encontró el empleado.")
            if self.volver_callback:
                self.volver_callback()
            return

            # Convertir fechas a formato dd/mm/yyyy para mostrar
        try:
            # birthdate ahora es un atributo del objeto empleado
            fecha_nacimiento = datetime.strptime(empleado.birthdate, '%Y-%m-%d').strftime('%d/%m/%Y')
        except Exception:
            # En caso de error, usar el valor original
            fecha_nacimiento = empleado.birthdate

        # Usar .insert(0, ...) para CTkEntry widgets
        self.name.insert(0, empleado.name)
        self.last_name.insert(0, empleado.last_name) # last_name es un CTkEntry
        self.document_number.insert(0, empleado.document_number)
        self.document_issuance.insert(0, empleado.document_issuance)
        self.phone_number.insert(0, empleado.phone_number)
        self.residence_address.insert(0, empleado.residence_address)
        self.RUT.insert(0, empleado.RUT)
        self.email.insert(0, empleado.email)

        # Usar .set(...) para CTkOptionMenu (StringVar)
        self.tipo_documento_var.set(empleado.document_type)

        # Asignar la fecha de nacimiento (ya convertida)
        self.birthdate.insert(0, fecha_nacimiento)

    def guardar_cambios(self):

        empleado = Empleado(   
            name=self.name.get(),
            last_name=self.last_name.get(),
            document_type=self.tipo_documento_var.get(),
            document_number=self.document_number.get(),
            document_issuance=self.document_issuance.get(),
            birthdate=self.birthdate.get(),
            phone_number=self.phone_number.get(),
            residence_address=self.residence_address.get(),
            RUT=self.RUT.get(),
            email=self.email.get()
        )

        employee_service.actualizar_empleado(self.empleado_id,empleado)
        messagebox.showinfo("Éxito", "Contrato actualizado correctamente")
        if self.volver_callback:
            self.destroy()
            self.volver_callback()


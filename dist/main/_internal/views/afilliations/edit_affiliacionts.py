import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from models.affiliation import Afiliacion
from services import affiliation_service, employee_service
from utils.canvas import agregar_fondo_decorativo
from utils.autocomplete import crear_autocompletado

class EditarAfiliacion(ctk.CTkFrame):
    def __init__(self, parent, affiliation_id, username=None, rol=None, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.afiliacion_id = affiliation_id

        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))

        agregar_fondo_decorativo(self)
        self.configure(fg_color="#F5F5F5")

        # Obtener empleados
        empleados = employee_service.obtener_empleados_para_combobox()
        self.empleados_dict = {f"{nombre}": id for id, nombre in empleados}

        # ==== Estilos ====
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
            self, text="EDITAR AFILIACION",
            fg_color="transparent", font=("Georgia", 16), text_color="#06A051"
        ).pack(pady=(60, 0), padx=(250, 0), anchor="w")

        self.btn_volver = ctk.CTkButton(
        self,image=self.icon_back,text="",corner_radius=0,hover_color="#F3EFEF", width=30,height=30,command=self.volver_al_panel,fg_color="#D2D2D2"
        )
        self.btn_volver.place(relx=0.98, rely=0.03, anchor="ne")

        # ==== Tarjeta principal ====
        self.card = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card.place(relx=0.52, rely=0.50, anchor="center", relwidth=0.70, relheight=0.70)
        self.card.rowconfigure(0, weight=1)
        self.card.columnconfigure(0, weight=1)

        form_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        form_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        form_frame.columnconfigure((0, 1, 2, 3), weight=1)

        def crear_label_entry(texto, fila, col, colspan=1, atributo=""):
            ctk.CTkLabel(form_frame, text=texto, font=("Georgia", 12,"bold")).grid(row=fila, column=col, columnspan=colspan, sticky="w", pady=(5, 0), padx=5)
            entry = ctk.CTkEntry(form_frame, placeholder_text=texto, **entry_style)
            entry.grid(row=fila+1, column=col, columnspan=colspan, padx=5, pady=(0, 10), sticky="ew")
            setattr(self, atributo, entry)

        # Campos
        crear_label_entry("Nombre empleado", 0, 0, 2, "entry_empleado")
        crear_label_entry("EPS", 0, 2, 1, "entry_eps")
        crear_label_entry("ARL", 0, 3, 1, "entry_arl")
        crear_label_entry("Nivel de Riesgo", 2, 0, 1, "entry_risk_level")
        crear_label_entry("AFP", 2, 1, 1, "entry_afp")
        crear_label_entry("Caja de Compensación", 2, 2, 2, "entry_compensation_box")
        crear_label_entry("Banco", 4, 0, 1, "entry_bank")
        crear_label_entry("Número de Cuenta", 4, 1, 1, "entry_account_number")
        crear_label_entry("Tipo de Cuenta", 4, 2, 1, "entry_account_type")

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
            botones_frame, text="Guardar cambios", fg_color="#06A051", hover_color="#048B45",
            command=self.guardar_cambios, **boton_style, corner_radius=10
        ).grid(row=0, column=0, padx=30, pady=30, sticky="ew")

        ctk.CTkButton(
            botones_frame, text="Cancelar", fg_color="#D12B1B", hover_color="#B81D0F",
            command=self.cancelar, **boton_style, corner_radius=10
        ).grid(row=0, column=1, padx=30, pady=30, sticky="ew")

        # Cargar datos de la afiliación existente
        self.cargar_datos()

    def cancelar(self):
        self.destroy()
        if self.volver_callback:
            self.volver_callback()

    def cargar_datos(self):
        afiliacion = affiliation_service.obtener_afiliacion_por_id(self.afiliacion_id)
        if not afiliacion:
            messagebox.showerror("Error", "No se encontró la afiliación.")
            if self.volver_callback:
                self.volver_callback()
            return

        empleado_nombre = next((nombre for nombre, id in self.empleados_dict.items() if id == afiliacion.employee_id), "")
        self.entry_empleado.insert(0, empleado_nombre)
        self.entry_eps.insert(0, afiliacion.eps)
        self.entry_arl.insert(0, afiliacion.arl)
        self.entry_risk_level.insert(0, afiliacion.risk_level)
        self.entry_afp.insert(0, afiliacion.afp)
        self.entry_compensation_box.insert(0, afiliacion.compensation_box)
        self.entry_bank.insert(0, afiliacion.bank)
        self.entry_account_number.insert(0, afiliacion.account_number)
        self.entry_account_type.insert(0, afiliacion.account_type)

    def guardar_cambios(self):
        empleado_nombre = self.entry_empleado.get()
        employee_id = self.empleados_dict.get(empleado_nombre)

        if employee_id is None:
            messagebox.showerror("Error", "Debes seleccionar un empleado válido.")
            return

        afiliacion = Afiliacion(
            id=self.afiliacion_id,
            employee_id=employee_id,
            eps=self.entry_eps.get(),
            arl=self.entry_arl.get(),
            risk_level=self.entry_risk_level.get(),
            afp=self.entry_afp.get(),
            compensation_box=self.entry_compensation_box.get(),
            bank=self.entry_bank.get(),
            account_number=self.entry_account_number.get(),
            account_type=self.entry_account_type.get()
        )
        affiliation_service.actualizar_afiliacion(self.afiliacion_id, afiliacion)

        messagebox.showinfo("Éxito", "Afiliación actualizada correctamente")
        if self.volver_callback:
            self.destroy()
            self.volver_callback()
            # Redirigir a la vista buscar afiliaciones
    
    def seleccionar_empleado(self, nombre):
        self.entry_empleado.delete(0, "end")
        self.entry_empleado.insert(0, nombre)
        self.lista_empleados.lower()
    
    def volver_al_panel(self):
        if self.volver_callback:
            self.destroy()
            self.volver_callback()

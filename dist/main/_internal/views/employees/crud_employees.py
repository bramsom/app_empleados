import customtkinter as ctk
from tkinter import Canvas
from tkinter import messagebox
from controllers import employee_controller
from models.employee import Empleado

class CrudEmpleados(ctk.CTkFrame):
    def __init__(self, parent, username, rol, volver_callback):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.controller = employee_controller
        self.configure(fg_color="#F5F5F5")

        canvas = Canvas(self, bg="#F5F5F5", highlightthickness=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        

        # Polígonos decorativos
        canvas.create_polygon(860, 0, 990, 0, 1320, 330, 1255, 395, fill="#D2D2D2", outline="")
        canvas.create_polygon(1079, 122, 1140, 60, 1360, 280, 1360, 402, fill="#888888", outline="")
        canvas.create_polygon(1240, 0, 1360, 0, 1360, 120, 1360, 120, fill="#D2D2D2", outline="")
        canvas.create_polygon(1060, 0, 1210, 0, 1340, 130, 1265, 205, fill="#D12B1B", outline="")
        canvas.create_polygon(930, 0, 935, 0, 1195, 259, 1190, 260, fill="#FCFCFC", outline="")
        canvas.create_polygon(1130, 0, 1135, 0, 1260, 125, 1260, 130, fill="#FCFCFC", outline="")
        canvas.create_polygon(355, 640, 505, 640, 105, 241, 30, 315, fill="#D2D2D2", outline="")
        canvas.create_polygon(0, 240, 0, 370, 150, 520, 215, 455, fill="#888888", outline="")
        canvas.create_polygon(300, 640, 160, 640, 10, 490, 81, 420, fill="#D12B1B", outline="")
        canvas.create_polygon(225, 640, 230, 640, 70, 480, 68, 483, fill="#FCFCFC", outline="")
        canvas.create_polygon(425, 640, 430, 640, 180, 390, 178, 395, fill="#FCFCFC", outline="")

        # Tarjeta principal encima del fondo
        self.card = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card.place(relx=0.52, rely=0.5, anchor="center", relwidth=0.85, relheight=0.90)
        # Crear el layout principal
        self.create_layout()
        
    def create_layout(self):
        titulo=ctk.CTkLabel(self.card, text="REGISTRAR NUEVO EMPLEADO", font=("Georgia", 16), text_color="#06A051")
        titulo.pack(pady=(10, 5), padx=(20, 0), anchor="w")

        main_frame = ctk.CTkFrame(self.card, fg_color="#F3EFEF")
        main_frame.pack( expand=True, padx=0, pady=0,fill="both")

        self.scroll_frame = ctk.CTkScrollableFrame(main_frame, fg_color="#F3EFEF")
        self.scroll_frame.pack(padx=0, pady=10, fill="both", expand=True)

        self.create_input_fields()
        self.create_action_buttons()


    def create_input_fields(self):
        campos = [
            ("nombre", "Nombres"),
            ("apellido", "Apellidos"),
            ("tipo_doc", "Documento"),
            ("n_doc", "No Documento"),
            ("expedicion", "Expedida en"),
            ("nacimiento", "Fecha nacimiento"),
            ("telefono", "No de teléfono"),
            ("direccion", "Dirección de residencia"),
            ("rut", "RUT"),
            ("email", "Correo electrónico"),
            ("cargo", "Cargo que desempeña")
        ]

        self.entries = {}

        # Contenedor con grid
       
        grid_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#F3EFEF")
        grid_frame.pack(pady=10, padx=10, fill="both", expand=True)

        for i in range(4):
            grid_frame.grid_columnconfigure(i, weight=1)

        # Organiza en filas y columnas
        label_nombre = ctk.CTkLabel(grid_frame, text="Nombres:",font=("Georgia", 14, "bold"))
        label_nombre.grid(row=0, column=0, sticky="w", padx=5, pady=0)
        entry_nombre = ctk.CTkEntry(grid_frame,fg_color="#E0E0E0",border_width=0,corner_radius=8,height=40)
        entry_nombre.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        label_apellido = ctk.CTkLabel(grid_frame, text="Apellidos:",font=("Georgia", 14, "bold"))
        label_apellido.grid(row=0, column=2, sticky="w", padx=5, pady=0)
        entry_apellido = ctk.CTkEntry(grid_frame,fg_color="#E0E0E0",border_width=0,corner_radius=8,height=40)
        entry_apellido.grid(row=1, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

        # ---------- Fila 2: Documento y Número ----------
        label_tipo_doc = ctk.CTkLabel(grid_frame, text="Documento:",font=("Georgia", 14, "bold"))
        label_tipo_doc.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        entry_tipo_doc = ctk.CTkEntry(grid_frame,fg_color="#E0E0E0",border_width=0,corner_radius=8,height=40)
        entry_tipo_doc.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        label_n_doc = ctk.CTkLabel(grid_frame, text="No Documento:",font=("Georgia", 14, "bold"))
        label_n_doc.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        entry_n_doc = ctk.CTkEntry(grid_frame,fg_color="#E0E0E0",border_width=0,corner_radius=8,height=40)
        entry_n_doc.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        label_expedicion = ctk.CTkLabel(grid_frame, text="Expedida en:",font=("Georgia", 14, "bold"))
        label_expedicion.grid(row=2, column=2, sticky="w", padx=5, pady=5)
        entry_expedicion = ctk.CTkEntry(grid_frame,fg_color="#E0E0E0",border_width=0,corner_radius=8,height=40)
        entry_expedicion.grid(row=3, column=2, padx=5, pady=5, sticky="ew")

        label_nacimiento = ctk.CTkLabel(grid_frame, text="Fecha nacimiento:",font=("Georgia", 14, "bold"))
        label_nacimiento.grid(row=2, column=3, sticky="w", padx=5, pady=5)
        entry_nacimiento = ctk.CTkEntry(grid_frame,fg_color="#E0E0E0",border_width=0,corner_radius=8,height=40)
        entry_nacimiento.grid(row=3, column=3, padx=5, pady=5, sticky="ew")

        # ---------- Fila 4: Teléfono, Dirección, RUT ----------
        label_telefono = ctk.CTkLabel(grid_frame, text="No de teléfono:",font=("Georgia", 14, "bold"))
        label_telefono.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        entry_telefono = ctk.CTkEntry(grid_frame,fg_color="#E0E0E0",border_width=0,corner_radius=8,height=40)
        entry_telefono.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        label_direccion = ctk.CTkLabel(grid_frame, text="Dirección de residencia:",font=("Georgia", 14, "bold"))
        label_direccion.grid(row=4, column=1,columnspan=2, sticky="w", padx=5, pady=5)
        entry_direccion = ctk.CTkEntry(grid_frame,fg_color="#E0E0E0",border_width=0,corner_radius=8,height=40)
        entry_direccion.grid(row=5, column=1,columnspan=2, padx=5, pady=5, sticky="ew")

        label_rut = ctk.CTkLabel(grid_frame, text="RUT:",font=("Georgia", 14, "bold"))
        label_rut.grid(row=4, column=3, sticky="w", padx=5, pady=5)
        entry_rut = ctk.CTkEntry(grid_frame,fg_color="#E0E0E0",border_width=0,corner_radius=8,height=40)
        entry_rut.grid(row=5, column=3, padx=5, pady=5, sticky="ew")

        # ---------- Fila 6: Email y Cargo ocupando 2 columnas cada uno ----------
        label_email = ctk.CTkLabel(grid_frame, text="Correo electrónico:",font=("Georgia", 14, "bold"))
        label_email.grid(row=6, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        entry_email = ctk.CTkEntry(grid_frame,fg_color="#E0E0E0",border_width=0,corner_radius=8,height=40)
        entry_email.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        label_cargo = ctk.CTkLabel(grid_frame, text="Cargo que desempeña:",font=("Georgia", 14, "bold"))
        label_cargo.grid(row=6, column=2, columnspan=2, sticky="w", padx=5, pady=5)
        entry_cargo = ctk.CTkEntry(grid_frame,fg_color="#E0E0E0",border_width=0,corner_radius=8,height=40)
        entry_cargo.grid(row=7, column=2, columnspan=2, padx=5, pady=5, sticky="ew")

        grid_frame.grid_columnconfigure(0, weight=1)
        grid_frame.grid_columnconfigure(1, weight=1)
        grid_frame.grid_columnconfigure(2, weight=1)

    def create_action_buttons(self):
        self.button_outside_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_outside_frame.place(relx=0.5, rely=0.8, anchor="center")

        # Botón Guardar
        btn_guardar = ctk.CTkButton(self.button_outside_frame, text="Guardar", command=self.guardar,
                            fg_color="green", hover_color="darkgreen", width=140, height=35)
        btn_guardar.pack(side="left", padx=10)

        # Botón Limpiar
        btn_limpiar = ctk.CTkButton(self.button_outside_frame, text="Limpiar", command=self.limpiar,
                            fg_color="gray", hover_color="darkgray", width=140, height=35)
        btn_limpiar.pack(side="left", padx=10)

        # Botón Cancelar
        btn_cancelar = ctk.CTkButton(self.button_outside_frame, text="Cancelar", command=self.cancelar,
                            fg_color="red", hover_color="darkred", width=140, height=35)
        btn_cancelar.pack(side="left", padx=10)

    #se mantiene esta funcion
    def guardar(self):
        try:
            datos = Empleado(
                name=self.entries["nombre"].get(),
                last_name=self.entries["apellido"].get(),
                document_type=self.entries["tipo_doc"].get(),
                document_number=self.entries["n_doc"].get(),
                document_issuance=self.entries["expedicion"].get(),
                birthdate=self.entries["nacimiento"].get(),
                phone_number=self.entries["telefono"].get(),
                residence_address=self.entries["direccion"].get(),
                RUT=self.entries["rut"].get(),
                email=self.entries["email"].get(),
                position=self.entries["cargo"].get()
            )
            self.controller.registrar_empleado(datos)
            messagebox.showinfo("Éxito", "Empleado registrado correctamente.")
            self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar empleado: {str(e)}")

    def limpiar(self):
        for campo in self.entries.values():
            campo.delete(0, 'end')
    
    def cancelar(self):
        if messagebox.askyesno("Cancelar", "¿Deseas cancelar el registro y volver al menú?"):
            self.volver_callback()

    # Método eliminado ya que no se necesita para el dashboard
    # def volver_menu(self, username, rol):
    #     from views.main_menu import MainMenu
    #     MainMenu(username, rol).deiconify()
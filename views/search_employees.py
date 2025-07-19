import customtkinter as ctk
from tkinter import Canvas
from tkinter import messagebox
from controllers import employee_controller

class BuscarEmpleado(ctk.CTkFrame):
    def __init__(self, parent,username,rol, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.empleados = []
        self.empleado_actual = None

        # Configuración del contenedor principal
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

        # Título
        titulo = ctk.CTkLabel(self, text="Buscar Empleado", font=("Georgia", 24, "bold"))
        titulo.pack(pady=10, padx=(100, 0),anchor="w")

        # Tarjeta principal encima del fondo
        self.card = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        self.card.place(relx=0.53, rely=0.6, anchor="center", relwidth=0.90, relheight=0.85)
        self.card.lift()

        # Entrada de búsqueda
        self.barra_busqueda = ctk.CTkEntry(self, placeholder_text="Buscar por nombre...",width=300)
        self.barra_busqueda.pack( pady=10, padx=(100, 0),anchor="w")
        self.barra_busqueda.bind("<KeyRelease>", self.actualizar_lista)

        # Lista scrollable de empleados
        self.scroll_frame = ctk.CTkScrollableFrame(self.card, height=300)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        self.cargar_empleados()

    def cargar_empleados(self):
        try:
            self.empleados = employee_controller.listar_empleados()
            self.actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar empleados: {str(e)}")

    def actualizar_lista(self, event=None):
        # Limpiar el frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        filtro = self.barra_busqueda.get().lower()
        for emp in self.empleados:
            nombre_completo = f"{emp.name} {emp.last_name}"
            if filtro in nombre_completo.lower():
                boton = ctk.CTkButton(self.scroll_frame, text=nombre_completo, width=400,
                                      command=lambda e=emp: self.mostrar_detalle(e),
                                      anchor="w")
                boton.pack(pady=5, padx=10)

    def mostrar_detalle(self, empleado):
        self.empleado_actual = empleado

        # Ocultar scroll frame
        self.scroll_frame.pack_forget()
        self.barra_busqueda.pack_forget()

        # Frame de detalles
        self.frame_detalle = ctk.CTkFrame(self, fg_color="white")
        self.frame_detalle.place(relx=0.53, rely=0.6, anchor="center", relwidth=0.90, relheight=0.85)
        self.frame_detalle.lift()

        campos = [
            ("Nombre", empleado.name),
            ("Apellido", empleado.last_name),
            ("Tipo Documento", empleado.document_type),
            ("N° Documento", empleado.document_number),
            ("Lugar Expedición", empleado.document_issuance),
            ("Fecha Nacimiento", empleado.birthdate),
            ("Teléfono", empleado.phone_number),
            ("Dirección", empleado.residence_address),
            ("RUT", empleado.RUT),
            ("Email", empleado.email),
            ("Cargo", empleado.position)
        ]

        for campo, valor in campos:
            fila = ctk.CTkFrame(self.frame_detalle, fg_color="white")
            fila.pack(fill="x", pady=3, padx=10)
            ctk.CTkLabel(fila, text=f"{campo}:", width=140, anchor="w",
                         font=("Georgia", 12, "bold"), text_color="black").pack(side="left")
            ctk.CTkLabel(fila, text=valor or "-", anchor="w", text_color="black").pack(side="left")

        btn_volver = ctk.CTkButton(self.frame_detalle, text="Ver lista completa",
                                   command=self.volver_a_lista, fg_color="#888888", hover_color="#666666")
        btn_volver.pack(pady=10)

    def volver_a_lista(self):
        self.frame_detalle.destroy()
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.barra_busqueda.pack( pady=10, padx=(100, 0),anchor="w")

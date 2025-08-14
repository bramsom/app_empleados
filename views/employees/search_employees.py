import customtkinter as ctk
from PIL import Image
from tkinter import Canvas
from tkinter import messagebox
from controllers import employee_controller
from utils.canvas import agregar_fondo_decorativo
from controllers import affiliation_controller
from controllers import contract_controller
from views.employees.detail_employees import MostrarEmpleado

class BuscarEmpleados(ctk.CTkFrame):
    def __init__(self, parent,username,rol, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.empleados = []
        self.empleado_actual = None
        self.icon_ver = ctk.CTkImage(light_image=Image.open("images/read.png"), size=(20, 20))
        self.icon_editar = ctk.CTkImage(light_image=Image.open("images/edit.png"), size=(20, 20))
        self.icon_eliminar = ctk.CTkImage(light_image=Image.open("images/delete.png"), size=(20, 20))
        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))

        agregar_fondo_decorativo(self)

        # Configuración del contenedor principal
        self.configure(fg_color="#F5F5F5")

        self.btn_volver = ctk.CTkButton(
            self, text="", image=self.icon_back, width=40,
            height=40, fg_color="transparent", hover_color="#D3D3D3", 
            command=self.volver_a_lista
        )
        self.btn_volver.place(x=1300, y=10)
        self.btn_volver.lower()

        # Título
        titulo = ctk.CTkLabel(self, text="Buscar Empleado", font=("Georgia", 24, "bold"))
        titulo.pack(pady=10, padx=(100, 0),anchor="w")

        # Tarjeta principal encima del fondo
        self.card = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card.place(relx=0.52, rely=0.58, anchor="center", relwidth=0.90, relheight=0.80)
        self.card.lift()
        
        # Entrada de búsqueda
        self.barra_busqueda = ctk.CTkEntry(self, placeholder_text="Buscar por nombre...",width=300, corner_radius=20, height=40)
        self.barra_busqueda.pack( pady=10, padx=(100, 0),anchor="w")
        self.barra_busqueda.bind("<KeyRelease>", self.actualizar_lista)

        # Título fuera del scroll, dentro de la tarjeta
        titulo = ctk.CTkLabel(self.card, text="EMPLEADOS", font=("Georgia", 16), text_color="#06A051")
        titulo.pack(pady=(10, 5), padx=(20, 0), anchor="w")  # espacio arriba y separación suave

        # Lista scrollable de empleados
        self.scroll_frame = ctk.CTkScrollableFrame(self.card, height=300, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_empleados()

    def cargar_empleados(self):
        try:
            self.empleados = employee_controller.listar_empleados()
            if not self.empleados:
                messagebox.showinfo("vacio, no hay empleados registrados")
            else:
                self.actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar empleados: {str(e)}")

    def actualizar_lista(self, event=None):
        # Limpiar el frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        filtro = self.barra_busqueda.get().lower()

        # Definir tamaños fijos por columna
        anchos_columnas = {
            0: 140,  # Nombre
            1: 140,  # Apellido
            2: 80,   # Tipo Doc
            3: 80,  # N° Doc
            4: 100,  # Fecha nacimiento
            5: 100,  # Teléfono
            6: 190,  # Correo
            7: 120, # Cargo
            8: 60,  # Mostrar
            9: 60,  # Editar
            10: 70   # Eliminar
        }

        for col, ancho in anchos_columnas.items():
            self.scroll_frame.grid_columnconfigure(col, minsize=ancho)

        # Encabezados
        headers = ["Nombre", "Apellido", "Tipo Doc", "N° Doc", "Fecha\nNacimiento",
                "Teléfono", "Correo", "Cargo", "Ver", "Editar", "Eliminar"]

        for i, header in enumerate(headers):
            cell = ctk.CTkFrame(self.scroll_frame, fg_color="#A9A9A9", corner_radius=5)
            cell.grid(row=0, column=i, padx=2, pady=5, sticky="nsew")
            label = ctk.CTkLabel(cell, text=header, font=("Georgia", 11, "bold"), text_color="black")
            label.pack(expand=True)

        # Filas de empleados
        row = 1
        for emp in self.empleados:
            nombre_completo = f"{emp.name} {emp.last_name} {emp.document_type} {emp.document_number} {emp.birthdate} {emp.phone_number} {emp.email}{emp.position}"
            if filtro in nombre_completo.lower():
                valores = [emp.name, emp.last_name, emp.document_type, emp.document_number,
                   emp.birthdate, emp.phone_number,emp.email, emp.position]

                for col, texto in enumerate(valores):
                    cell = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
                    cell.grid(row=row, column=col, padx=2, pady=3, sticky="nsew")
                    ctk.CTkLabel(cell, text=texto, font=("Arial", 10.5), anchor="center").pack(expand=True)

            # Botones
            btns = [
                ("", self.icon_ver, lambda e=emp: self.mostrar_detalle(e)),
                 ("", self.icon_editar, lambda e=emp: self.mostrar_detalle(e)),
                ("", self.icon_eliminar, lambda e=emp: self.mostrar_detalle(e))
            ]
            for i, (txt, icon, cmd) in enumerate(btns):
                btn = ctk.CTkButton(self.scroll_frame, text=txt, image=icon, width=40, height=30,
                                fg_color="transparent", hover_color="#D3D3D3",
                                command=cmd, compound="left")
                btn.grid(row=row, column=8 + i, padx=2, pady=3)

            row += 1

    def mostrar_detalle(self, empleado):
                # Limpiar el área actual de contenido
        for widget in self.master.winfo_children():
            widget.destroy()

        MostrarEmpleado(
            parent=self.master, username=self.username,rol=self.rol,
            volver_callback=lambda: BuscarEmpleados(self.master, self.username, self.rol).pack(fill="both", expand=True),
            employee_id=empleado.id  # <-- Aquí pasas el id correcto
        ).pack(fill="both", expand=True)

    def volver_a_lista(self):
        self.btn_volver.lower()
        self.card.place(relx=0.52, rely=0.58, anchor="center", relwidth=0.90, relheight=0.80)
        
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.barra_busqueda.pack(pady=10, padx=(100, 0), anchor="w")

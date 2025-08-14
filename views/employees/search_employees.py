import customtkinter as ctk
from PIL import Image
from tkinter import Canvas
from tkinter import messagebox
from controllers import employee_controller
from utils.canvas import agregar_fondo_decorativo
from controllers import affiliation_controller
from controllers import contract_controller
from views.employees.detail_employees import MostrarEmpleado
from views.employees.edit_employees import EditarEmpleado

class BuscarEmpleados(ctk.CTkFrame):
    def __init__(self, parent,username,rol, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.empleados = [] # Esta lista contendrá TODOS los empleados cargados inicialmente
        self.empleado_actual = None
        self.icon_ver = ctk.CTkImage(light_image=Image.open("images/read.png"), size=(20, 20))
        self.icon_editar = ctk.CTkImage(light_image=Image.open("images/edit.png"), size=(20, 20))
        self.icon_eliminar = ctk.CTkImage(light_image=Image.open("images/delete.png"), size=(20, 20))
        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))
        self.icon_seeker = ctk.CTkImage(Image.open("images/seeker.png"), size=(25, 25))

        agregar_fondo_decorativo(self)

        # Configuración del contenedor principal
        self.configure(fg_color="#F5F5F5")

        self.btn_volver = ctk.CTkButton(
            self, text="", image=self.icon_back, width=40,
            height=40, fg_color="transparent", hover_color="#D3D3D3", 
            command=self.volver_al_panel
        )
        self.btn_volver.place(x=1300, y=10)
        self.btn_volver.lower()

        self.btn_volver = ctk.CTkButton(
        self,image=self.icon_back,text="",corner_radius=0,hover_color="#F3EFEF", width=30,height=30,command=self.volver_al_panel,fg_color="#d2d2d2"
        )
        self.btn_volver.place(relx=0.98, rely=0.02, anchor="ne")

        # Tarjeta principal encima del fondo
        self.card = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card.place(relx=0.52, rely=0.54, anchor="center", relwidth=0.90, relheight=0.80)
        self.card.lift()
        
        barra_busqueda_frame = ctk.CTkFrame(
        self,border_width=2,border_color="#B0B0B0",fg_color="white", corner_radius=20,width=300
        )
        barra_busqueda_frame.place(relx=0.08, rely=0.02, relwidth=0.206, relheight=0.07)


        # Entry y botón más pequeños y con fondo blanco
        self.barra_busqueda = ctk.CTkEntry(
            barra_busqueda_frame,placeholder_text="Buscar por nombre...",border_width=0,width=200,height=36,corner_radius=20,fg_color="white"
        )
        self.barra_busqueda.pack(side="left", padx=(8, 0), pady=6)
        self.barra_busqueda.bind("<Return>", self.actualizar_lista)

        btn_buscar = ctk.CTkButton(
            barra_busqueda_frame,text="",image=self.icon_seeker,width=36,height=36,corner_radius=20,fg_color="white",hover_color="#F0F0F0",command=self.actualizar_lista
        )
        btn_buscar.pack(side="left", padx=(0, 8), pady=6)

        # Título fuera del scroll, dentro de la tarjeta
        titulo = ctk.CTkLabel(self.card, text="EMPLEADOS", font=("Georgia", 16), text_color="#06A051")
        titulo.pack(pady=(10, 5), padx=(20, 0), anchor="w") 

        # Lista scrollable de empleados
        self.scroll_frame = ctk.CTkScrollableFrame(self.card, height=300, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_empleados()

    def cargar_empleados(self):
        try:
            # Carga todos los empleados inicialmente
            self.empleados = employee_controller.listar_empleados()
            if not self.empleados:
                messagebox.showinfo("Información", "No hay empleados registrados.")
            
            self.actualizar_lista() # Muestra todos los empleados al cargar

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar empleados: {str(e)}")

    def actualizar_lista(self, event=None):
        # Limpiar el frame antes de dibujar las nuevas filas
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        filtro = self.barra_busqueda.get().lower().strip() # Obtener el texto del filtro y limpiar espacios

        # === Aplicar el filtro ===
        empleados_a_mostrar = []
        if filtro: # Si hay texto en el filtro
            for emp in self.empleados:
                # Concatenar todos los campos relevantes para la búsqueda
                nombre_completo = f"{emp.name} {emp.last_name} {emp.document_type} {emp.document_number} {emp.birthdate} {emp.phone_number} {emp.email} {emp.position}".lower()
                if filtro in nombre_completo:
                    empleados_a_mostrar.append(emp)
        else: # Si el filtro está vacío, mostrar todos los empleados
            empleados_a_mostrar = self.empleados

        # Si no se encuentra ningún empleado con el filtro, mostrar un mensaje
        if not empleados_a_mostrar and filtro:
            ctk.CTkLabel(self.scroll_frame, text="No se encontraron empleados que coincidan con la búsqueda.",
                         font=("Arial", 11), text_color="gray").grid(row=0, column=0, columnspan=11, pady=20)
            return

        # Definir tamaños fijos por columna
        anchos_columnas = {
            0: 140,  # Nombre
            1: 140,  # Apellido
            2: 80,   # Tipo Doc
            3: 80,   # N° Doc
            4: 100,  # Fecha nacimiento
            5: 100,  # Teléfono
            6: 190,  # Correo
            7: 120,  # Cargo
            8: 60,   # Ver
            9: 60,   # Editar
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

        # Filas de empleados filtrados
        row = 1
        for emp in empleados_a_mostrar: # Ahora itera sobre la lista ya filtrada
            valores = [emp.name, emp.last_name, emp.document_type, emp.document_number,
                       emp.birthdate, emp.phone_number, emp.email, emp.position]

            for col, texto in enumerate(valores):
                cell = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
                cell.grid(row=row, column=col, padx=2, pady=3, sticky="nsew")
                ctk.CTkLabel(cell, text=texto, font=("Arial", 10.5), anchor="center").pack(expand=True)

            # Botones
            btns = [
                ("", self.icon_ver, lambda e=emp: self.mostrar_detalle(e)),
                ("", self.icon_editar, lambda e=emp: self.editar_empleado(e)),
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
            employee_id=empleado.id
        ).pack(fill="both", expand=True)

    def editar_empleado(self, empleado):
        # Limpiar el área actual de contenido
        for widget in self.master.winfo_children():
            widget.destroy()

        EditarEmpleado(
            parent=self.master,username=self.username, rol=self.rol,
            volver_callback=lambda: BuscarEmpleados(self.master, self.username, self.rol).pack(fill="both", expand=True),
            employee_id=empleado.id  # <-- Aquí pasas el id correcto
        ).pack(fill="both", expand=True)
    def volver_al_panel(self):
        if self.volver_callback:
            self.volver_callback()


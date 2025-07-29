import customtkinter as ctk
from PIL import Image
from tkinter import Canvas
from tkinter import messagebox
from controllers import employee_controller
from controllers import affiliation_controller
from controllers import contract_controller

class BuscarEmpleado(ctk.CTkFrame):
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

        # Configuración del contenedor principal
        self.configure(fg_color="#F5F5F5")

        self.btn_volver = ctk.CTkButton(
            self,text="",image=self.icon_back,width=40,
            height=40,fg_color="transparent",hover_color="#D3D3D3",command=self.volver_a_lista  # o tu función personalizada
        )
      
        self.btn_volver.place(x=1300, y=10)  # Puedes ajustar la posición
        self.btn_volver.lower()

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
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

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
            0: 100,  # Nombre
            1: 100,  # Apellido
            2: 50,   # Tipo Doc
            3: 80,  # N° Doc
            4: 100,  # Fecha nacimiento
            5: 90,  # Teléfono
            6: 130,  # Dirección
            7: 160,  # Correo
            8: 90, # Cargo
            9: 80,  # Mostrar
            10: 80,  # Editar
            11: 80   # Eliminar
        }

        for col, ancho in anchos_columnas.items():
            self.scroll_frame.grid_columnconfigure(col, minsize=ancho)

        # Encabezados
        headers = ["Nombre", "Apellido", "Tipo\nDoc", "N°\nDoc", "Fecha\nNacimiento",
                "Teléfono", "Dirección", "Correo", "Cargo", "Mostrar", "Editar", "Eliminar"]

        for i, header in enumerate(headers):
            cell = ctk.CTkFrame(self.scroll_frame, fg_color="#A9A9A9", corner_radius=8)
            cell.grid(row=0, column=i, padx=2, pady=5, sticky="nsew")
            label = ctk.CTkLabel(cell, text=header, font=("Georgia", 11, "bold"), text_color="black")
            label.pack(expand=True)

        # Filas de empleados
        row = 1
        for emp in self.empleados:
            nombre_completo = f"{emp.name} {emp.last_name} {emp.document_type} {emp.document_number} {emp.birthdate} {emp.phone_number} {emp.residence_address}{emp.email}{emp.position}"
            if filtro in nombre_completo.lower():
                valores = [emp.name, emp.last_name, emp.document_type, emp.document_number,
                   emp.birthdate, emp.phone_number, emp.residence_address,
                   emp.email, emp.position]

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
                btn.grid(row=row, column=9 + i, padx=2, pady=3)

            row += 1

    def mostrar_detalle(self, empleado):
        self.empleado_actual = empleado
        self.scroll_frame.pack_forget()
        self.barra_busqueda.pack_forget()
        self.card.place_forget()
        self.btn_volver.lift()

        # Frame general
        self.card2 = ctk.CTkFrame(self, fg_color="transparent", corner_radius=10)
        self.card2.place(relx=0.52, rely=0.5, anchor="center", relwidth=0.90, relheight=0.80)
        self.frame_detalle = ctk.CTkScrollableFrame(self.card2, fg_color="transparent")
        self.frame_detalle.pack(fill="both", expand=True, padx=0, pady=0)

        # Contenedor superior con dos columnas
        fila_superior = ctk.CTkFrame(self.frame_detalle, fg_color="transparent")
        fila_superior.pack(fill="x", padx=20, pady=10)
        fila_superior.grid_columnconfigure((0, 1), weight=1)

        # Configurar título y columnas
        card_info = ctk.CTkFrame(fila_superior, fg_color="#E6E6E6", corner_radius=10)
        card_info.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        card_info.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

        def crear_campo(label, valor, fila, columna, colspan=1):
            frame = ctk.CTkFrame(card_info, fg_color="#B0B0B0", corner_radius=6)
            frame.grid(row=fila, column=columna, columnspan=colspan, padx=5, pady=5, sticky="nsew")
            ctk.CTkLabel(frame, text=label, font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
            ctk.CTkLabel(frame, text=valor or "-", font=("arial", 11), anchor="w", justify="left",
                 corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")

        ctk.CTkLabel(card_info, text="DATOS PERSONALES", font=("Georgia", 16), text_color="#06A051").grid(
        row=0, column=0, columnspan=5, sticky="w", padx=10, pady=5
        )

        # Lista de campos: (Etiqueta, Valor, Fila, Columna, Columnspan)
        campos = [
            ("Nombre:", f"{empleado.name} {empleado.last_name}", 1, 0, 2),
            ("Tipo documento:", empleado.document_type, 1, 2),
            ("Número documento:", empleado.document_number, 1, 3),
            ("Expedida en:", empleado.document_issuance, 1, 4),

            ("Fecha nacimiento:", empleado.birthdate, 2, 0),
            ("No telefono:", empleado.phone_number, 2, 1),
            ("Dirección residencia:", empleado.residence_address, 2, 2, 2),
            ("RUT:", empleado.RUT, 2, 4),

            ("Correo electrónico:", empleado.email, 3, 0, 2),
            ("Cargo:", empleado.position, 3, 2),
        ]

            # Crear los campos con la función
        for campo in campos:
                crear_campo(*campo)
    
            
        # Tarjeta: Afiliaciones
        card_afiliaciones = ctk.CTkFrame(fila_superior, fg_color="#E6E6E6", corner_radius=10)
        card_afiliaciones.grid(row=0, column=1, sticky="nsew", padx=10)

        ctk.CTkLabel(card_afiliaciones, text="AFILIACIONES", font=("Georgia", 16,), text_color="#06A051").grid(row=0, column=0, columnspan=4, sticky="w", padx=10, pady=5)

        afiliaciones = affiliation_controller.consultar_afiliaciones_por_empleado(empleado.id)
        if afiliaciones:
            for idx, afi in enumerate(afiliaciones):
                texto = f"{afi.affiliation_type}: {afi.name}"
                fila = idx // 2 + 1
                col = (idx % 2) * 2
                contenedor = ctk.CTkFrame(card_afiliaciones, fg_color="#B0B0B0", corner_radius=6)
                contenedor.grid(row=fila, column=col, padx=10, pady=5, sticky="nsew", columnspan=2)

                ctk.CTkLabel(contenedor, text=afi.affiliation_type + ":", font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
                ctk.CTkLabel(contenedor, text=afi.name or "-", fg_color="#A0A0A0", corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")
        else:
            ctk.CTkLabel(card_afiliaciones, text="Sin afiliaciones registradas", text_color="gray").grid(row=1, column=0, columnspan=4, padx=10, pady=5)

        # Tarjeta: Contratos (una sola fila)
        card_contratos = ctk.CTkFrame(self.frame_detalle, fg_color="#E6E6E6", corner_radius=10)
        card_contratos.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(card_contratos, text="CONTRATOS", font=("Georgia", 16), text_color="#06A051").grid(row=0, column=0, columnspan=10, sticky="w", padx=10, pady=5)

        contratos = contract_controller.consultar_contratos_por_empleado(empleado.id)
        if contratos:
            for idx, contrato in enumerate(contratos):
                fila = idx + 1
                columnas = [
                    ("No contrato:", contrato.id),
                    ("Fecha de inicio:", contrato.start_date),
                    ("Fecha de corte:", contrato.end_date or "Actual"),
                    ("Tipo de contrato:", contrato.type_contract),
                    ("Salario mensual:", f"${contrato.monthly_payment:,.2f}"),
                    ("Estado:", contrato.state),
                    ("Persona que lo contrató:", contrato.contractor or "-")
                ]
                for col_idx, (etq, val) in enumerate(columnas):
                    contenedor = ctk.CTkFrame(card_contratos, fg_color="#B0B0B0", corner_radius=6)
                    contenedor.grid(row=fila, column=col_idx, padx=10, pady=5, sticky="nsew")

                ctk.CTkLabel(contenedor, text=etq, font=("Georgia", 11, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
                ctk.CTkLabel(contenedor, text=val, fg_color="#A0A0A0", corner_radius=5).pack(anchor="w", padx=10, pady=(0, 5), fill="x")
        else:
            ctk.CTkLabel(card_contratos, text="Sin contratos registrados", text_color="gray").grid(row=1, column=0, padx=10, pady=5)
        

    def volver_a_lista(self):
        self.btn_volver.lower()
        self.card2.destroy()
        
        self.card.place(relx=0.52, rely=0.58, anchor="center", relwidth=0.90, relheight=0.80)
        
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.barra_busqueda.pack(pady=10, padx=(100, 0), anchor="w")

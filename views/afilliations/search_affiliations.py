import customtkinter as ctk
from PIL import Image
from tkinter import Canvas,messagebox
from utils.canvas import agregar_fondo_decorativo
from services import affiliation_service, employee_service
from controllers import affiliation_controller, employee_controller
from views.afilliations.edit_affiliacionts import EditarAfiliacion

class BuscarAfiliaciones(ctk.CTkFrame):
    def __init__(self, parent, username=None, rol=None, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback

        # Cargar imágenes una sola vez
        self.icon_editar = ctk.CTkImage(light_image=Image.open("images/edit.png"), size=(20, 20))
        self.icon_eliminar = ctk.CTkImage(light_image=Image.open("images/delete.png"), size=(20, 20))
        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))
        self.icon_seeker = ctk.CTkImage(Image.open("images/seeker.png"), size=(25, 25))

        agregar_fondo_decorativo(self)
        self.configure(fg_color="#F5F5F5")


        # Buscador
        # ==== Tarjeta principal ====
        self.card = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card.place(relx=0.52, rely=0.55, anchor="center", relwidth=0.92, relheight=0.80)
        self.card.rowconfigure(0, weight=1)
        self.card.columnconfigure(0, weight=1)

        # Título
        titulo2 = ctk.CTkLabel(self.card, text="AFILIACIONES", font=("Georgia", 16), text_color="#06A051")
        titulo2.pack(pady=(10, 5), padx=(20, 0), anchor="w")

        barra_filtros_frame = ctk.CTkFrame(self, fg_color="#F3EFEF", width=700, corner_radius=10)
        barra_filtros_frame.place(relx=0.06, rely=0.01, relwidth=0.92, relheight=0.1)

        canvas = Canvas(barra_filtros_frame, bg="#F5F5F5", highlightthickness=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        canvas.create_polygon(783, 0, 914, 0, 1243, 330, 1180, 395, fill="#D2D2D2", outline="")
        canvas.create_polygon(983, 0, 1134, 0, 1263, 130, 1188, 205, fill="#D12B1B", outline="")
        canvas.create_polygon(1164, 0, 1284, 0, 1284, 120, 1284, 120, fill="#D2D2D2", outline="")
        canvas.create_polygon(854, 0, 860, 0, 1118, 259, 1114, 260, fill="#FCFCFC", outline="")
        canvas.create_polygon(1054, 0, 1059, 0, 1184, 125, 1184, 130, fill="#FCFCFC", outline="")

        self.btn_volver = ctk.CTkButton(
        barra_filtros_frame,image=self.icon_back,text="",corner_radius=0,hover_color="#F3EFEF", width=30,height=30,command=self.volver_al_panel,fg_color="#D2D2D2"
        )
        self.btn_volver.place(relx=1.001, rely=0.2, anchor="ne")

        barra_busqueda_frame = ctk.CTkFrame(
            barra_filtros_frame,border_width=2,border_color="#B0B0B0",fg_color="white", corner_radius=20,width=300
        )
        barra_busqueda_frame.pack(side="left", padx=(10, 10), pady=10)

        self.btn_volver = ctk.CTkButton(
        barra_filtros_frame,image=self.icon_back,text="",corner_radius=0,hover_color="#F3EFEF", width=30,height=30,command=self.volver_al_panel,fg_color="#d2d2d2"
        )
        self.btn_volver.place(relx=1.001, rely=0.2, anchor="ne")

        # Entry y botón más pequeños y con fondo blanco
        self.entry_busqueda = ctk.CTkEntry(
            barra_busqueda_frame,placeholder_text="Buscar por nombre...",border_width=0,width=200,height=36,corner_radius=20,fg_color="white"
        )
        self.entry_busqueda.pack(side="left", padx=(8, 0), pady=6)
        self.entry_busqueda.bind("<Return>", self.buscar_afiliaciones)

        btn_buscar = ctk.CTkButton(
            barra_busqueda_frame,text="",image=self.icon_seeker,width=36,height=36,corner_radius=20,fg_color="white",hover_color="#F0F0F0",command=self.buscar_afiliaciones
        )
        btn_buscar.pack(side="left", padx=(0, 8), pady=6)
        
        self.filtro_eps = ctk.CTkEntry(barra_filtros_frame, placeholder_text="EPS", width=150)
        self.filtro_eps.pack(side="left", padx=5)
        self.filtro_eps.bind("<Return>", self.buscar_afiliaciones)
        

        self.filtro_arl = ctk.CTkEntry(barra_filtros_frame, placeholder_text="ARL", width=150)
        self.filtro_arl.pack(side="left", padx=5)
        self.filtro_arl.bind("<Return>", self.buscar_afiliaciones)

        self.filtro_afp = ctk.CTkEntry(barra_filtros_frame, placeholder_text="AFP", width=150)
        self.filtro_afp.pack(side="left", padx=5)
        self.filtro_afp.bind("<Return>", self.buscar_afiliaciones)

        self.filtro_caja_compensacion = ctk.CTkEntry(barra_filtros_frame, placeholder_text="Caja de Compensación", width=150)
        self.filtro_caja_compensacion.pack(side="left", padx=5)
        self.filtro_caja_compensacion.bind("<Return>", self.buscar_afiliaciones)

        self.filtro_banco = ctk.CTkEntry(barra_filtros_frame, placeholder_text="Banco", width=150)
        self.filtro_banco.pack(side="left", padx=5)
        self.filtro_banco.bind("<Return>", self.buscar_afiliaciones)

        # Frame contenedor con scroll
        self.scroll_frame = ctk.CTkScrollableFrame(self.card, fg_color="#F3EFEF")
        self.scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self.mostrar_afiliaciones()

    def mostrar_afiliaciones(self, filtros=None):
        # 1. Eliminar widgets anteriores
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # 2. Obtener datos y aplicar filtros
        afiliaciones = affiliation_controller.listar_afiliaciones()
    
        if filtros:
            def cumple_filtros(afi):
                nombre_empleado = (afi.get('empleado') or "").lower()
                return (
                    filtros["nombre"] in nombre_empleado and
                    filtros["eps"] in (afi.get('eps') or "").lower() and
                    filtros["arl"] in (afi.get('arl') or "").lower() and
                    filtros["afp"] in (afi.get('afp') or "").lower() and
                    filtros["caja_compensacion"] in (afi.get('compensation_box') or "").lower() and
                    filtros["banco"] in (afi.get('bank') or "").lower()
                )
            afiliaciones = list(filter(cumple_filtros, afiliaciones))

        columnas = [
            ("Empleado", 260),
            ("EPS", 90),
            ("ARL", 90),
            ("Riesgo", 60),
            ("AFP", 90),
            ("Caja Compensacion.", 150),
            ("Banco", 80),
            ("Cuenta", 90),
            ("Tipo", 140),
            ("Editar", 50),
            ("Eliminar", 50)
        ]
        
        # Asegurar que el scroll_frame tenga configuradas las columnas
        for col_index in range(len(columnas)):
            self.scroll_frame.grid_columnconfigure(col_index, weight=0)

        # === ENCABEZADOS ===
        for col_index, (texto, ancho) in enumerate(columnas):
            label = ctk.CTkLabel(self.scroll_frame, text=texto, font=("Georgia", 11, "bold"),
                                 width=ancho, anchor="w", fg_color="#D12B1B", corner_radius=3, text_color="black")
            label.grid(row=0, column=col_index, padx=1, pady=5, sticky="nsew")

        
        # === FILAS DE DATOS (CON COLORES ALTERNOS) ===
        for row_index, afiliacion in enumerate(afiliaciones, start=1):
            
            # 1. Definir color de fila
            if row_index % 2 == 0:
                color_fila = "#F0F0F0"  # Gris claro
            else:
                color_fila = "#D9D9D9"  # Gris más oscuro
                
            valores = [
                afiliacion.get('empleado') or "-",
                afiliacion.get('eps') or "-",
                afiliacion.get('arl') or "-",
                afiliacion.get('risk_level') or "-",
                afiliacion.get('afp') or "-",
                afiliacion.get('compensation_box') or "-",
                afiliacion.get('bank') or "-",
                afiliacion.get('account_number') or "-",
                afiliacion.get('account_type') or "-"
            ]

            # 2. Crear las celdas de datos con el color de fondo de la fila
            for col_index, valor in enumerate(valores):
                
                # Usamos un CTkFrame para contener la etiqueta y darle el color
                celda_frame = ctk.CTkFrame(self.scroll_frame, fg_color=color_fila, corner_radius=0, 
                                           width=columnas[col_index][1], height=30)
                celda_frame.grid(row=row_index, column=col_index, padx=0, pady=0, sticky="nsew")
                
                # La etiqueta dentro del frame usa el mismo color de fondo
                campo = ctk.CTkLabel(celda_frame, text=valor, anchor="w", font=("Arial", 11), 
                                     fg_color="transparent", text_color="black")
                campo.pack(fill="both", expand=True, padx=10, pady=5) # Usamos pack para centrar verticalmente

            # 3. Botones de acción (Editar y Eliminar)
            
            # Botón Editar
            col_editar = len(columnas) - 2
            celda_editar = ctk.CTkFrame(self.scroll_frame, fg_color=color_fila, corner_radius=0, width=columnas[col_editar][1], height=30)
            celda_editar.grid(row=row_index, column=col_editar, padx=0, pady=0, sticky="nsew")
            
            ctk.CTkButton(
                celda_editar, image=self.icon_editar, text="", width=30, height=30,
                fg_color="transparent", command=lambda id=afiliacion['id']: self.editar_afiliacion(id), hover_color="#B0B0B0"
            ).pack(expand=True, padx=4, pady=4)

            # Botón Eliminar
            col_eliminar = len(columnas) - 1
            celda_eliminar = ctk.CTkFrame(self.scroll_frame, fg_color=color_fila, corner_radius=0, width=columnas[col_eliminar][1], height=30)
            celda_eliminar.grid(row=row_index, column=col_eliminar, padx=0, pady=0, sticky="nsew")
            
            ctk.CTkButton(
                celda_eliminar, image=self.icon_eliminar, text="", width=30, height=30,
                fg_color="transparent", command=lambda id=afiliacion['id']: self.eliminar_afiliacion(id), hover_color="#B0B0B0"
            ).pack(expand=True, padx=4, pady=4)


    def buscar_afiliaciones(self, event=None):
        filtros = {
            "nombre": self.entry_busqueda.get().lower(),
            "eps": self.filtro_eps.get().lower(),
            "arl": self.filtro_arl.get().lower(),
            "afp": self.filtro_afp.get().lower(),
            "caja_compensacion": self.filtro_caja_compensacion.get().lower(),
            "banco": self.filtro_banco.get().lower(),
        }
        self.mostrar_afiliaciones(filtros)

    def editar_afiliacion(self, affiliation_id):
        # Limpiar el área actual de contenido
        for widget in self.master.winfo_children():
            widget.destroy()

        EditarAfiliacion(
                parent=self.master,
                username=self.username,
                rol=self.rol,
                volver_callback=lambda: BuscarAfiliaciones(self.master).pack(fill="both", expand=True),
                affiliation_id=affiliation_id
            ).pack(fill="both", expand=True)
        
    def eliminar_afiliacion(self, afiliacion_id):
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta afiliación?")
        if respuesta:
            # Accede al 'id' usando la clave del diccionario
            affiliation_service.eliminar_afiliacion(afiliacion_id)
            messagebox.showinfo("Éxito", "Afiliación eliminada correctamente.")
            self.mostrar_afiliaciones()
    
    def volver_al_panel(self):
        if self.volver_callback:
            self.destroy()
            self.volver_callback()

import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
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

        agregar_fondo_decorativo(self)
        self.configure(fg_color="#F5F5F5")

        titulo = ctk.CTkLabel(self, text="Buscar Afiliacion", font=("Georgia", 24, "bold"))
        titulo.pack(pady=10, padx=(100, 0), anchor="w")
    
        self.btn_volver = ctk.CTkButton(
        self,image=self.icon_back,text="",corner_radius=0,hover_color="#F3EFEF", width=30,height=30,command=self.volver_al_panel,fg_color="#D2D2D2"
    )
        self.btn_volver.place(relx=0.97, y=3, anchor="ne")

        # Buscador
        # ==== Tarjeta principal ====
        self.card = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card.place(relx=0.52, rely=0.58, anchor="center", relwidth=0.90, relheight=0.80)
        self.card.rowconfigure(0, weight=1)
        self.card.columnconfigure(0, weight=1)

        # Título
        titulo2 = ctk.CTkLabel(self.card, text="AFILIACIONES", font=("Georgia", 16), text_color="#06A051")
        titulo2.pack(pady=(10, 5), padx=(20, 0), anchor="w")

        buscador_frame = ctk.CTkFrame(self, fg_color="#F3EFEF", width=700, corner_radius=10)
        buscador_frame.place(relx=0.07, rely=0.07, relwidth=0.90, relheight=0.1)

        self.entry_busqueda = ctk.CTkEntry(buscador_frame, placeholder_text="Buscar por nombre...",width=300, corner_radius=20, height=40)
        self.entry_busqueda.pack(side="left", padx=(10, 5))
        self.entry_busqueda.bind("<Return>", lambda event: self.buscar_afiliaciones())
        
        self.filtro_eps = ctk.CTkEntry(buscador_frame, placeholder_text="EPS", width=150)
        self.filtro_eps.pack(side="left", padx=5)
        self.filtro_eps.bind("<Return>", lambda event: self.buscar_afiliaciones())
        

        self.filtro_arl = ctk.CTkEntry(buscador_frame, placeholder_text="ARL", width=150)
        self.filtro_arl.pack(side="left", padx=5)
        self.filtro_arl.bind("<Return>", lambda event: self.buscar_afiliaciones())

        self.filtro_afp = ctk.CTkEntry(buscador_frame, placeholder_text="AFP", width=150)
        self.filtro_afp.pack(side="left", padx=5)
        self.filtro_afp.bind("<Return>", lambda event: self.buscar_afiliaciones())

        self.filtro_banco = ctk.CTkEntry(buscador_frame, placeholder_text="Banco", width=150)
        self.filtro_banco.pack(side="left", padx=5)
        self.filtro_banco.bind("<Return>", lambda event: self.buscar_afiliaciones())

        btn_buscar = ctk.CTkButton(buscador_frame, text="Buscar", command=self.buscar_afiliaciones)
        btn_buscar.pack(side="left")

        # Frame contenedor con scroll
        self.scroll_frame = ctk.CTkScrollableFrame(self.card, fg_color="#F3EFEF")
        self.scroll_frame.pack(fill="both", expand=True, padx=0, pady=0)

        self.mostrar_afiliaciones()

    def mostrar_afiliaciones(self, filtros=None):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        afiliaciones = affiliation_controller.listar_afiliaciones()
        empleados = dict(employee_service.obtener_empleados_para_combobox())
        
        if filtros:
            def cumple_filtros(afi):
                nombre_empleado = empleados.get(afi.employee_id, "").lower()
                return (
                    filtros["nombre"] in nombre_empleado and
                    filtros["eps"] in (afi.eps or "").lower() and
                    filtros["arl"] in (afi.arl or "").lower() and
                    filtros["afp"] in (afi.afp or "").lower() and
                    filtros["banco"] in (afi.bank or "").lower()
                )
            afiliaciones = list(filter(cumple_filtros, afiliaciones))
        columnas = [
            ("Empleado", 200),
            ("EPS", 70),
            ("ARL", 70),
            ("Riesgo", 60),
            ("AFP", 70),
            ("Caja Compensacion.", 110),
            ("Banco", 80),
            ("Cuenta", 90),
            ("Tipo", 90),
            ("Editar", 50),   # Nueva columna para editar
            ("Eliminar", 50)  # Nueva columna para eliminar

        ]

        # === ENCABEZADOS ===
        for col_index, (texto, ancho) in enumerate(columnas):
            label = ctk.CTkLabel(self.scroll_frame, text=texto, font=("Georgia", 11, "bold"),
                                 width=ancho, anchor="w", fg_color="#A9A9A9", corner_radius=8, text_color="black")
            label.grid(row=0, column=col_index, padx=2, pady=5, sticky="nsew")

        # === FILAS DE DATOS ===
        for row_index, afiliacion in enumerate(afiliaciones, start=1):
            nombre = empleados.get(afiliacion.empleado, "No encontrado")
            valores = [
                nombre,
                afiliacion.eps,
                afiliacion.arl,
                afiliacion.risk_level,
                afiliacion.afp,
                afiliacion.compensation_box,
                afiliacion.bank,
                afiliacion.account_number,
                afiliacion.account_type
            ]

            for col_index, valor in enumerate(valores):
                campo = ctk.CTkLabel(self.scroll_frame, text=valor or "-", anchor="w", font=("Arial", 11),
                                     width=columnas[col_index][1], fg_color="#F2F2F2", text_color="black")
                campo.grid(row=row_index, column=col_index, padx=10, pady=5, sticky="nsew")

            # Botón Editar
            ctk.CTkButton(
                self.scroll_frame, image=self.icon_editar, text="", width=30, height=30,
                fg_color="transparent", command=lambda id=afiliacion.id: self.editar_afiliacion(id),hover_color="#D3D3D3"
            ).grid(row=row_index, column=len(columnas)-2, padx=5, pady=5)

            # Botón Eliminar
            ctk.CTkButton(
                self.scroll_frame, image=self.icon_eliminar, text="", width=30, height=30,
                fg_color="transparent", command=lambda a=afiliacion: self.eliminar_afiliacion(a),hover_color="#D3D3D3"
            ).grid(row=row_index, column=len(columnas)-1, padx=5, pady=5)

    def buscar_afiliaciones(self):
        filtros = {
            "nombre": self.entry_busqueda.get().lower(),
            "eps": self.filtro_eps.get().lower(),
            "arl": self.filtro_arl.get().lower(),
            "afp": self.filtro_afp.get().lower(),
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
        
    def eliminar_afiliacion(self, afiliacion):
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta afiliación?")
        if respuesta:
            affiliation_service.eliminar_afiliacion(afiliacion.id)
            messagebox.showinfo("Éxito", "Afiliación eliminada correctamente.")
            self.mostrar_afiliaciones()
    
    def volver_al_panel(self):
        if self.volver_callback:
            self.volver_callback()

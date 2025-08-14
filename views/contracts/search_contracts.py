import customtkinter as ctk
from PIL import Image
from tkinter import Canvas, messagebox
from controllers import employee_controller
from services import contract_service, employee_service
from controllers import contract_controller
from datetime import datetime, date
from utils.canvas import agregar_fondo_decorativo
from utils.filters import crear_combobox
from utils.filters import crear_filtro_fecha, abrir_calendario_avanzado
from views.contracts.edit_contracts import EditarContrato
from views.contracts.detail_contracts import MostrarContrato


class BuscarContratos(ctk.CTkFrame):
    def __init__(self, parent, username, rol, volver_callback=None, ver_detalle_callback=None, editar_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        self.ver_detalle_callback = ver_detalle_callback
        self.editar_callback = editar_callback

        agregar_fondo_decorativo(self)

        self.configurar_iconos()
        self.configurar_filtros()
        self.configurar_tabla()
        self.cargar_contratos()
        
        # Iconos
    def configurar_iconos(self):
        self.icon_ver = ctk.CTkImage(light_image=Image.open("images/read.png"), size=(20, 20))
        self.icon_editar = ctk.CTkImage(light_image=Image.open("images/edit.png"), size=(20, 20))
        self.icon_eliminar = ctk.CTkImage(light_image=Image.open("images/delete.png"), size=(20, 20))
        self.icon_calendar = ctk.CTkImage(light_image=Image.open("images/calendar.png"), size=(20, 20))
        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))
        self.icon_seeker = ctk.CTkImage(Image.open("images/seeker.png"), size=(25, 25))

        # Configuración del contenedor principal
        self.configure(fg_color="#F5F5F5")

        # Tarjeta principal
        self.card = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card.place(relx=0.52, rely=0.53, anchor="center", relwidth=0.92, relheight=0.80)
        self.card.lift()
    

    def configurar_filtros(self):
        # === CONTENEDOR DE BARRA Y FILTROS EN UNA MISMA FILA ===
        barra_filtros_frame = ctk.CTkFrame(self, fg_color="#F5F5F5", width=700, corner_radius=10)
        barra_filtros_frame.place(relx=0.06, rely=0.01, relwidth=0.92, relheight=0.1)
        # Crea un canvas dentro del frame
        canvas = Canvas(barra_filtros_frame, bg="#F5F5F5", highlightthickness=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        canvas.create_polygon(783, 0, 914, 0, 1243, 330, 1180, 395, fill="#D2D2D2", outline="")
        canvas.create_polygon(983, 0, 1134, 0, 1263, 130, 1188, 205, fill="#D12B1B", outline="")
        canvas.create_polygon(1164, 0, 1284, 0, 1284, 120, 1284, 120, fill="#D2D2D2", outline="")
        canvas.create_polygon(854, 0, 860, 0, 1118, 259, 1114, 260, fill="#FCFCFC", outline="")
        canvas.create_polygon(1054, 0, 1059, 0, 1184, 125, 1184, 130, fill="#FCFCFC", outline="")
        # === BARRA DE BÚSQUEDA ===
        # Frame con borde visible
        barra_busqueda_frame = ctk.CTkFrame(
            barra_filtros_frame,border_width=2,border_color="#B0B0B0",fg_color="white", corner_radius=20,width=300
        )
        barra_busqueda_frame.pack(side="left", padx=(10, 10), pady=10)

        self.btn_volver = ctk.CTkButton(
        barra_filtros_frame,image=self.icon_back,text="",corner_radius=0,hover_color="#F3EFEF", width=30,height=30,command=self.volver_al_panel,fg_color="#d2d2d2"
        )
        self.btn_volver.place(relx=1.001, rely=0.2, anchor="ne")

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

        # === FILTROS ===
        filtro_frame = ctk.CTkFrame(barra_filtros_frame, fg_color="transparent")
        filtro_frame.pack(side="left")

        self.filtro_tipo = crear_combobox(
        filtro_frame, ["Todos", "FIJO", "INDEFINIDO", "HORA CATEDRA", "APRENDIZAJE", "SERVICIOS"], 160,
        )
        self.filtro_tipo.bind("<Return>", self.actualizar_lista)
        self.filtro_estado = crear_combobox(
            filtro_frame, ["Todos", "ACTIVO", "FINALIZADO", "RETIRADO"], 130,
        )
        self.filtro_estado.bind("<Return>", self.actualizar_lista)

        # Filtros de fecha usando utilidades y lambdas para limpiar
        self.fecha_inicio_cal, _ = crear_filtro_fecha(
            filtro_frame, "Desde:", lambda: self.fecha_inicio_cal.delete(0, "end"), lambda: None
        )
        self.fecha_inicio_cal.bind("<Button-1>", lambda e: abrir_calendario_avanzado(self, self.fecha_inicio_cal, self.fecha_corte_cal, lambda: None))
        self.fecha_inicio_cal.bind("<Return>", self.actualizar_lista)
        self.fecha_corte_cal, _ = crear_filtro_fecha(
            filtro_frame, "Hasta:", lambda: self.fecha_corte_cal.delete(0, "end"), lambda: None
        )
        self.fecha_corte_cal.bind("<Button-1>", lambda e: abrir_calendario_avanzado(self, self.fecha_inicio_cal, self.fecha_corte_cal, lambda: None))
        self.fecha_corte_cal.bind("<Return>", self.actualizar_lista)
        # Variables de control (si las necesitas para lógica adicional)
        self.fecha_inicio_activa = False
        self.fecha_corte_activa = False

    def configurar_tabla(self):
        # Título de la tabla
        titulo_tabla = ctk.CTkLabel(self.card, text="CONTRATOS", font=("Georgia", 16), text_color="#06A051")
        titulo_tabla.pack(pady=(10, 5), padx=(20, 0), anchor="w")

        # Lista scrollable
        self.scroll_frame = ctk.CTkScrollableFrame(self.card, height=300, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=5, pady=10)


    def cargar_contratos(self):
        try:
            self.contratos = contract_controller.listar_contratos()
            if not self.contratos:
                messagebox.showinfo("Información", "No hay contratos registrados")
            else:
                self.actualizar_lista()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar contratos: {str(e)}")

    def actualizar_lista(self, event=None):
        # Limpiar frame anterior
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        filtro = self.barra_busqueda.get().lower()
        tipo_filtro = self.filtro_tipo.get()
        estado_filtro = self.filtro_estado.get()

        # Actualizar estado de los filtros de fecha
        self.fecha_inicio_activa = bool(self.fecha_inicio_cal.get())
        self.fecha_corte_activa = bool(self.fecha_corte_cal.get())

        # Obtener fechas seleccionadas si están activas
        fecha_inicio_filtro = None
        fecha_corte_filtro = None

        if self.fecha_inicio_activa:
            try:
                fecha_inicio_filtro = datetime.strptime(self.fecha_inicio_cal.get(), "%d/%m/%Y").date()
            except Exception:
                fecha_inicio_filtro = None
        if self.fecha_corte_activa:
            try:
                fecha_corte_filtro = datetime.strptime(self.fecha_corte_cal.get(), "%d/%m/%Y").date()
            except Exception:
                fecha_corte_filtro = None

        # Definir columnas
        columnas = [
            ("Empleado", 220), ("Tipo", 220), ("Inicio", 90), ("Corte", 90),
            ("Estado", 90), ("Contratante", 170), ("Valor Estimado", 130),
            ("Ver", 60), ("Editar", 60), ("Eliminar", 70)
        ]

        for i, (_, ancho) in enumerate(columnas):
            self.scroll_frame.grid_columnconfigure(i, minsize=ancho)

        # Crear encabezado
        for col, (nombre, _) in enumerate(columnas):
            celda = ctk.CTkFrame(self.scroll_frame, fg_color="#A9A9A9", corner_radius=5)
            celda.grid(row=0, column=col, padx=2, pady=5, sticky="nsew")
            label = ctk.CTkLabel(celda, text=nombre, font=("Georgia", 11, "bold"), text_color="black")
            label.pack(expand=True)

        # Mostrar contratos filtrados
        row = 1
        for contrato in self.contratos:

            # Filtro por nombre
            if filtro and filtro not in contrato["empleado"].lower():
                continue

            # Filtro por tipo
            if tipo_filtro != "Todos" and tipo_filtro.lower() not in contrato["tipo"].lower():
                continue

            # Filtro por estado
            if estado_filtro != "Todos" and contrato["estado"] != estado_filtro:
                continue

            # Filtro por fecha
            if fecha_inicio_filtro or fecha_corte_filtro:
                try:
                    fecha_inicio_contrato = datetime.strptime(contrato["inicio"], '%Y-%m-%d').date()
                    fecha_corte_contrato = datetime.strptime(contrato["corte"], '%Y-%m-%d').date()

                    if fecha_inicio_filtro and fecha_inicio_contrato < fecha_inicio_filtro:
                        continue
                    if fecha_corte_filtro and fecha_corte_contrato > fecha_corte_filtro:
                        continue

                except ValueError:
                    continue

            # Convertir fechas para mostrar en formato día/mes/año
            try:
                inicio_mostrar = datetime.strptime(contrato["inicio"], '%Y-%m-%d').strftime('%d/%m/%Y')
            except Exception:
                inicio_mostrar = contrato["inicio"]
            try:
                corte_mostrar = datetime.strptime(contrato["corte"], '%Y-%m-%d').strftime('%d/%m/%Y')
            except Exception:
                corte_mostrar = contrato["corte"]
            
            tipo_normalizado = contrato["tipo"].lower().replace("_", " ")

            valor_estimado = contrato.get("valor_estimado", 0)
                # Crear fila
            valores = [
                contrato["empleado"], contrato["tipo"], inicio_mostrar,
                corte_mostrar, contrato["estado"], contrato["contratante"],
                f"${valor_estimado:,.2f}"
            ]

            for col, valor in enumerate(valores):
                celda = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
                celda.grid(row=row, column=col, padx=1, pady=2, sticky="nsew")
                ctk.CTkLabel(celda, text=valor, font=("Arial", 10.5)).pack(expand=True)

            # Botones de acción
            acciones = [
                ("", self.icon_ver, lambda c=contrato: self.ver_detalle(c)),
                ("", self.icon_editar, lambda c=contrato: self.editar_contrato(c)),
                ("", self.icon_eliminar, lambda c=contrato: self.eliminar_contrato(c))
            ]
            
            for i, (texto, icono, comando) in enumerate(acciones):
                btn = ctk.CTkButton(
                    self.scroll_frame, text=texto, image=icono, width=40, height=30,
                    fg_color="transparent", hover_color="#D3D3D3", command=comando
                )
                btn.grid(row=row, column=7 + i, padx=1, pady=2)

            row += 1

    def ver_detalle(self, contrato):
        # Limpiar el área actual de contenido
        for widget in self.master.winfo_children():
            widget.destroy()

        MostrarContrato(
            parent=self.master, username=self.username,rol=self.rol,
            volver_callback=lambda: BuscarContratos(self.master, self.username, self.rol).pack(fill="both", expand=True),
            contract_id=contrato["id"]  # <-- Aquí pasas el id correcto
        ).pack(fill="both", expand=True)

    def editar_contrato(self, contrato):
        # Limpiar el área actual de contenido
        for widget in self.master.winfo_children():
            widget.destroy()

        EditarContrato(
            parent=self.master,username=self.username, rol=self.rol,
            volver_callback=lambda: BuscarContratos(self.master, self.username, self.rol).pack(fill="both", expand=True),
            contract_id=contrato["id"]  # <-- Aquí pasas el id correcto
        ).pack(fill="both", expand=True)

    def eliminar_contrato(self, contrato):
        respuesta = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta afiliación?")
        if respuesta:
            contract_service.eliminar_contrato(contrato['id'])
            messagebox.showinfo("Éxito", "Afiliación eliminada correctamente.")

    def volver_al_panel(self):
        if self.volver_callback:
            self.volver_callback()


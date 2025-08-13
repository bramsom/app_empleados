import customtkinter as ctk
from tkinter import Canvas, messagebox
import os
from PIL import Image

class Dashboard(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.username = username
        self.rol = rol
        self.menu_expanded = False
        self.user_button_expanded = False
        self.menu_width = {"collapsed": 60, "expanded": 200}
        
        # Configuración de vistas disponibles
        self.views = {
            "empleados": ("views.crud_employees", "CrudEmpleados", "Gestión de Empleados"),
            "empleados_buscar": ("views.employees.search_employees", "BuscarEmpleados", "Búsqueda de Empleados"),
            "contratos": ("views.contracts.register_contracts", "RegistrarContrato", "Gestión de contratos"),
            "contratos_buscar": ("views.contracts.search_contracts", "BuscarContratos", "Gestión de Contratos"),
            "afiliaciones": ("views.afilliations.register_affiliations", "RegistrarAfiliacion", "Gestión de afiliaciones"),
            "afiliaciones_buscar": ("views.afilliations.search_affiliations", "BuscarAfiliaciones", "Búsqueda de afiliaciones"),
            "usuarios": ("views.crud_users", "CrudUsuarios", "Gestión de usuarios y roles")
     }
        
        # Estados de submenús
        self.submenu_states = {}
        self.submenu_widgets = {}
        self.menu_widgets = {}
        self.active_section = None
        
        self.setup_window()
        self.create_layout()
        self.show_default_view()
        
    def setup_window(self):
        """Configuración inicial de la ventana"""
        self.geometry("1100x600")
        self.title("Dashboard - Sistema de Gestión")
        
    def create_layout(self):
        """Crear layout principal"""
        # Header
        self.header = ctk.CTkFrame(self, height=60, fg_color="#A9A9A9")
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        
        # Contenedor principal
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(side="top", fill="both", expand=True)
        
        self.init_header()
        
        # Área de contenido
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="#F5F5F5")
        self.content_area.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_container, width=self.menu_width["collapsed"], fg_color="#A9A9A9")
        self.sidebar.place(x=2, y=2, relheight=1.0)

        self.menu_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.menu_frame.pack(fill="both", expand=True)

        self.menu_inner_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        self.menu_inner_frame.pack(fill="y", anchor="n")
        
        self.create_menu()
        self.setup_menu_events()
        
    def create_menu(self):
        """Crear menú con configuración simplificada"""
        ruta_img = os.path.join(os.getcwd(), "images")
        
        # Configuración del menú
        menu_items = [
            ("logo.png", "MENÚ", None, True),
            ("home.png", "Home", self.show_default_view),
            ("emplooye.png", "Empleados", {
                "Registrar Empleado": lambda: self.show_view("empleados", "registrar"),
                "Buscar Empleado": lambda: self.show_view("empleados_buscar")
            }),
            ("contract.png", "Contratos", {
                "Registrar Contrato": lambda: self.show_view("contratos", "registrar"),
                "Buscar Contrato": lambda: self.show_view("contratos_buscar")
            }),
            ("affiliation.png", "Afiliaciones", {
                "Registrar Afiliación": lambda: self.show_view("afiliaciones", "registrar"),
                "Buscar Afiliación": lambda: self.show_view("afiliaciones_buscar")
            }),
            ("export.png", "Reportes", lambda: self.create_view_placeholder("Reportes y Estadísticas")),
            ("config.png", "Usuarios", {
                "Registrar Usuario": lambda: self.show_view("usuarios", "registrar"),
                "Buscar Usuario": lambda: self.show_view("usuarios", "buscar")
            })
        ]
        
        for item in menu_items:
            icon_file, text, action = item[:3]
            is_title = len(item) > 3 and item[3]
            
            image_path = os.path.join(ruta_img, icon_file)
            img = ctk.CTkImage(dark_image=Image.open(image_path), size=(27, 27))

            if is_title:
                continue
            elif isinstance(action, dict):
                self._create_menu_with_submenu(img, text, action)
            else:
                self._create_simple_menu_button(img, text, action)
            
        
    def _create_simple_menu_button(self, img, text, command):
        """Crear botón simple del menú"""
        btn = ctk.CTkButton(
            self.menu_inner_frame, text="", image=img, compound="left", command=command,
            width=60, height=60, fg_color="#A9A9A9", hover_color="#888888",
            font=("Georgia", 14), anchor="center"
        )
        btn.image = img
        btn.pack(fill="x")
        self.menu_widgets[text.lower()] = btn
        
    def _create_menu_with_submenu(self, img, text, submenu_items):
        """Crear botón con submenú"""
        # Botón principal
        btn = ctk.CTkButton(
            self.menu_inner_frame, text="", image=img, compound="left",
            command=lambda: self.toggle_submenu(text.lower()),
            width=60, height=60, fg_color="#A9A9A9", hover_color="#888888",
            font=("Georgia", 14), anchor="center"
        )
        btn.image = img
        btn.pack(fill="x")
        self.menu_widgets[text.lower()] = btn
        
        # Crear submenú
        submenu_key = text.lower()
        self.submenu_states[submenu_key] = False
        
        submenu_frame = ctk.CTkFrame(self.menu_inner_frame, fg_color="transparent")
        submenu_frame.pack_forget()
        
        submenu_buttons = []
        for option_text, option_command in submenu_items.items():
            sub_btn = ctk.CTkButton(
                submenu_frame, text="", width=35, height=35,
                fg_color="#808080", hover_color="#606060",
                font=("Georgia", 11), anchor="w", command=option_command
            )
            sub_btn.pack(fill="x")
            submenu_buttons.append((sub_btn, option_text))
        
        self.submenu_widgets[submenu_key] = {
            "frame": submenu_frame,
            "buttons": submenu_buttons,
            "parent_button": btn
        }
                
    def toggle_submenu(self, section_key):
        """Alternar visibilidad de submenú"""
        if section_key not in self.submenu_widgets:
            return

        # Cerrar otros submenús
        for key in list(self.submenu_states.keys()):
            if key != section_key and self.submenu_states[key]:
                self.submenu_states[key] = False
                self.submenu_widgets[key]["frame"].pack_forget()

        # Alternar submenú actual
        self.submenu_states[section_key] = not self.submenu_states[section_key]
        submenu_data = self.submenu_widgets[section_key]
        
        if self.submenu_states[section_key]:
            submenu_data["frame"].pack(after=submenu_data["parent_button"], fill="x", padx=10)
            self._update_submenu_visibility(section_key)
        else:
            submenu_data["frame"].pack_forget()
                
    def setup_menu_events(self):
        """Configurar eventos del menú de forma simplificada"""
        # Obtener todos los widgets relevantes
        widgets_to_bind = [self.sidebar] + list(self.menu_widgets.values())
        
        # Agregar widgets de submenús
        for submenu_data in self.submenu_widgets.values():
            widgets_to_bind.append(submenu_data["frame"])
            widgets_to_bind.extend([btn for btn, _ in submenu_data["buttons"]])
        
        # Aplicar eventos a todos los widgets
        for widget in widgets_to_bind:
            widget.bind("<Enter>", lambda e: self.toggle_menu(True))
            widget.bind("<Leave>", lambda e: self.toggle_menu(False))
            
    def toggle_menu(self, expand):
        """Alternar estado del menú"""
        if expand and not self.menu_expanded:
            self._expand_menu()
        elif not expand and self.menu_expanded:
            self.after(100, self._collapse_menu_delayed)
            
    def _expand_menu(self):
        """Expandir menú"""
        self.menu_expanded = True
        self.sidebar.place_configure(width=self.menu_width["expanded"])
        if 'title' in self.menu_widgets:
           self.menu_widgets['title'].pack(side="left", padx=(0, 10))
        
        # Actualizar textos de botones principales
        button_texts = {'home': 'Home', 'empleados': 'Empleados', 'contratos': 'Contratos', 
                       'afiliaciones': 'Afiliaciones', 'reportes': 'Reportes', 'usuarios': 'Usuarios'}
        
        for key, text in button_texts.items():
            if key in self.menu_widgets:
                self.menu_widgets[key].configure(text=f"  {text}", width=200, anchor="w")
                
        # Actualizar submenús visibles
        for section_key, is_visible in self.submenu_states.items():
            if is_visible:
                self._update_submenu_visibility(section_key)
                
    def _collapse_menu_delayed(self):
        """Contraer menú con verificación"""
        if self._cursor_over_sidebar():
             return

        self.menu_expanded = False
        self.sidebar.place_configure(width=self.menu_width["collapsed"])

        if 'title' in self.menu_widgets:
            self.menu_widgets['title'].pack_forget()

        # Restaurar botones principales
        for key, widget in self.menu_widgets.items():
            widget.configure(text="", width=60, anchor="center")

        # Ocultar texto de submenús y cerrarlos
        for section_key, submenu_data in self.submenu_widgets.items():
            # Ocultar frame de submenú si estaba visible
            submenu_data["frame"].pack_forget()
            self.submenu_states[section_key] = False  # Marcar como cerrado

            # Ocultar texto de los botones del submenú
            for btn, _ in submenu_data["buttons"]:
                btn.configure(text="", width=35)
                
    def _update_submenu_visibility(self, section_key):
        """Actualizar visibilidad de submenú"""
        if section_key in self.submenu_widgets:
            submenu_data = self.submenu_widgets[section_key]
            for btn, text in submenu_data["buttons"]:
                if self.menu_expanded:
                    btn.configure(text=f"    • {text}", width=160)
                else:
                    btn.configure(text="", width=35)
                
    def _cursor_over_sidebar(self):
        """Verificar si cursor está sobre sidebar"""
        try:
            x, y = self.winfo_pointerxy()
            sx, sy = self.sidebar.winfo_rootx(), self.sidebar.winfo_rooty()
            sw, sh = self.sidebar.winfo_width(), self.sidebar.winfo_height()
            return sx <= x <= sx + sw and sy <= y <= sy + sh
        except:
            return False
            
    def init_header(self):
        """Crear header"""
        self._create_institutional_logo()
        
        # Contenedor de usuario
        self.user_container = ctk.CTkFrame(self.header, fg_color="transparent")
        self.user_container.pack(side="right", padx=10)
        
        # Info usuario
        ctk.CTkLabel(
            self.user_container, 
            text=f"Bienvenido {self.username} | Rol: {self.rol}", 
            font=("Georgia", 14), text_color="black"
        ).pack(side="left", padx=(0, 50))
        
        # Cargar imagen de ícono
        icon_path = os.path.join(os.getcwd(), "images", "logout.png")  # Cambia el nombre si es logout_icon.png
        user_img = ctk.CTkImage(dark_image=Image.open(icon_path), size=(24, 24))

        # Botón usuario con imagen
        self.user_button = ctk.CTkButton(
        self.user_container, text="", image=user_img, width=36, height=36,
        fg_color="#A9A9A9", hover_color="#888888", command=self.toggle_user_menu
        )
        self.user_button.image = user_img  # para evitar que se recoja el recolector de basura
        self.user_button.pack(side="right", padx=(50, 30))

        # Botón logout
        self.logout_button = ctk.CTkButton(
            self.main_container, text="Cerrar sesión", width=120, height=40,
            text_color="black", fg_color="#D12B1B", hover_color="#C00013",
            font=("Georgia", 12), command=self.cerrar_sesion
        )
        self.logout_button.place_forget()
        
    def _create_institutional_logo(self):
        """Crear logo institucional"""
        try:
            logo_path = os.path.join(os.getcwd(), "images", "logo2.png")
            logo_img = ctk.CTkImage(dark_image=Image.open(logo_path), size=(60, 60))
            logo_label = ctk.CTkLabel(self.header, image=logo_img, text="")
            logo_label.image = logo_img
            logo_label.pack(side="left", padx=10)
        except Exception:
            ctk.CTkLabel(
                self.header, text="🏛️ FCCP", 
                font=("Arial", 16, "bold"), text_color="white"
            ).pack(side="left", padx=10)
        
    def toggle_user_menu(self):
        """Alternar menú de usuario"""
        if not self.user_button_expanded:
            self.user_button_expanded = True
            self.logout_button.place(x=self.winfo_width() - 120, y=2)
            self.logout_button.lift()
        else:
            self.user_button_expanded = False
            self.logout_button.place_forget()
            
    def clear_content_area(self):
        """Limpiar área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
    def create_view_placeholder(self, title):
        """Crear placeholder para vistas"""
        self.clear_content_area()
        placeholder = ctk.CTkLabel(self.content_area, text=title, font=("Arial", 24, "bold"))
        placeholder.pack(expand=True)
        
    def show_view(self, view_name, action=None):
        """Mostrar vista específica"""
        if view_name not in self.views:
            return
            
        self.clear_content_area()

        for key in self.submenu_widgets:
            if view_name.startswith(key):
                self.set_active_section(key)
                break
            else:
                self.set_active_section(view_name)

        module_name, class_name, placeholder_text = self.views[view_name]
        
        if action:
            action_text = "Registro" if action == "registrar" else "Búsqueda"
            placeholder_text = f"{action_text} de {view_name.title()}"
        
        try:
            module = __import__(module_name, fromlist=[class_name])
            crud_class = getattr(module, class_name)
            try:
                crud = crud_class(self.content_area, self.username, self.rol, self.volver_al_menu)
            except TypeError:
                crud = crud_class(self.content_area, self.username, self.rol)
            else:
                crud = crud_class(self.content_area, self.username, self.rol, self.volver_al_menu)
            crud.pack(fill="both", expand=True, padx=0, pady=0)
        except ImportError:
            self.create_view_placeholder(placeholder_text)

    def set_active_section(self, section_key):
        """Marcar botón principal como activo"""
        self.active_section = section_key

        for key, btn in self.menu_widgets.items():
            if key not in ['icon', 'title']:
                if key == section_key:
                    btn.configure(fg_color="#888888")  # Color más oscuro
                else:
                    btn.configure(fg_color="#A9A9A9")  # Color normal
        
    def show_default_view(self):
        """Vista por defecto con diseño geométrico"""
        self.clear_content_area()
        
        canvas = Canvas(self.content_area, bg="#F5F5F5", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Título principal
        self.title_label = ctk.CTkLabel(
            self.content_area,
            text="Bienvenidos al programa de gestion de\n\npersonal . Fundacion colegio ciudad de\n\nPiendamo(FCCP)",
            font=("Georgia", 24, "bold"), text_color="#333333"
        )
        self.title_label.place(relx=0.55, rely=0.45, anchor="center")
        
        # Frame para contenido
        welcome_frame = ctk.CTkFrame(canvas, fg_color="transparent")
        welcome_window = canvas.create_window(0, 0, window=welcome_frame, anchor="nw")
        
        # Polígonos (mantenidos igual)
        polygons = [
            ([860, 0, 990, 0, 1320, 330, 1255, 395], "#D2D2D2"),
            ([1079, 122, 1140, 60, 1360, 280, 1360, 402], "#888888"),
            ([1240, 0, 1360, 0, 1360, 120, 1360, 120], "#D2D2D2"),
            ([1060, 0, 1210, 0, 1340, 130, 1265, 205], "#D12B1B"),
            ([930, 0, 935, 0, 1195, 259, 1190, 260], "#FCFCFC"),
            ([1130, 0, 1135, 0, 1260, 125, 1260, 130], "#FCFCFC"),
            ([355, 640, 505, 640, 105, 241, 30, 315], "#D2D2D2"),
            ([0, 240, 0, 370, 150, 520, 215, 455], "#888888"),
            ([300, 640, 160, 640, 10, 490, 81, 420], "#D12B1B"),
            ([225, 640, 230, 640, 70, 480, 68, 483], "#FCFCFC"),
            ([425, 640, 430, 640, 180, 390, 178, 395], "#FCFCFC")
        ]
        
        def update_canvas(event=None):
            canvas.delete("all")
            width, height = canvas.winfo_width(), canvas.winfo_height()
            for points, color in polygons:
                canvas.create_polygon(points, fill=color, outline="")
            canvas.coords(welcome_window, width // 2 - 150, height // 2 - 80)
            
        canvas.bind("<Configure>", update_canvas)
        
        # Contenido de bienvenida
        welcome_texts = [
            (f"Bienvenido, {self.username}", ("Arial", 28, "bold"), None),
            (f"Rol: {self.rol}", ("Arial", 16), None),
            ("Pasa el cursor sobre el menú lateral para expandir las opciones", ("Arial", 14), "gray")
        ]
        
        for text, font, color in welcome_texts:
            label = ctk.CTkLabel(welcome_frame, text=text, font=font)
            if color:
                label.configure(text_color=color)
            label.pack(expand=True if "Bienvenido" in text else False, 
                      pady=(0, 10) if "Rol:" in text else 10)
    
    def volver_al_menu(self):
        """Función de retorno desde vistas"""
        self.show_default_view()
            
    def cerrar_sesion(self):
        """Cerrar sesión"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas cerrar sesión?"):
            self.destroy()
    

def inicializar_dashboard(username, rol):
    """Inicializar dashboard"""
    dashboard = Dashboard(username, rol)
    dashboard.mainloop()

if __name__ == "__main__":
    inicializar_dashboard("usuario_ejemplo", "administrador")
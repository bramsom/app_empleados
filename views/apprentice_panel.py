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
            "contratos": ("views.crud_contracts", "CrudContratos", "Gestión de contratos"),
            "afiliaciones": ("views.crud_afiliations", "CrudAfiliaciones", "Gestión de afiliaciones"),
            "usuarios": ("views.crud_users", "CrudUsuarios", "Gestion de usuarios y roles")
        }
        
        # Estado y widgets de submenús simplificado
        self.submenu_states = {}
        self.submenu_widgets = {}
        
        self.setup_window()
        self.create_layout()
        self.show_default_view()
        
    def setup_window(self):
        """Configuración inicial de la ventana"""
        self.geometry("1100x600")
        self.title("Dashboard - Sistema de Gestión")
        
    def create_layout(self):
        """Crear layout principal con header, sidebar y contenido"""
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
        """Crear menú con íconos desde carpeta 'images'"""
        ruta_img = os.path.join(os.getcwd(), "images")
        
        # Configuración simplificada del menú
        menu_config = [
            ("logo.png", "MENÚ", None, True),
            ("home.png", "Home", self.show_default_view, False),
            ("emplooye.png", "Empleados", None, False, {
                "Registrar Empleado": lambda: self.show_view("empleados", "registrar"),
                "Buscar Empleado": lambda: self.show_view("empleados", "buscar")
            }),
            ("contract.png", "Contratos", None, False, {
                "Registrar Contrato": lambda: self.show_view("contratos", "registrar"),
                "Buscar Contrato": lambda: self.show_view("contratos", "buscar")
            }),
            ("affiliation.png", "Afiliaciones", None, False, {
                "Registrar Afiliación": lambda: self.show_view("afiliaciones", "registrar"),
                "Buscar Afiliación": lambda: self.show_view("afiliaciones", "buscar")
            }),
            ("export.png", "Reportes", lambda: self.create_view_placeholder("Reportes y Estadísticas"), False),
            ("config.png", "Usuarios", None, False, {
                "Registrar Usuario": lambda: self.show_view("usuarios", "registrar"),
                "Buscar Usuario": lambda: self.show_view("usuarios", "buscar")
            })
        ]
        
        self.menu_widgets = {}
        
        for item in menu_config:
            icon_file, text, command, is_title = item[:4]
            submenu_items = item[4] if len(item) > 4 else None
            
            image_path = os.path.join(ruta_img, icon_file)
            img = ctk.CTkImage(dark_image=Image.open(image_path), size=(24, 24))

            if is_title:
                self._create_menu_title(img, text)
            else:
                button = self._create_menu_button(img, text, command, submenu_items)
                if submenu_items:
                    self._create_submenu(text, submenu_items, button)
                
    def _create_menu_title(self, img, text):
        """Crear título del menú con logo"""
        self.logo_container = ctk.CTkFrame(self.menu_inner_frame, fg_color="transparent")
        self.logo_container.pack(pady=(20, 20), fill="x")
        
        self.menu_widgets['icon'] = ctk.CTkLabel(self.logo_container, image=img, text="")
        self.menu_widgets['icon'].image = img
        self.menu_widgets['icon'].pack(side="left", padx=(15, 10))
        
        self.menu_widgets['title'] = ctk.CTkLabel(self.logo_container, text=text, font=("Georgia", 16))
        self.menu_widgets['title'].pack_forget()
        
    def _create_menu_button(self, img, text, command, has_submenu):
        """Crear botón del menú"""
        if has_submenu:
            command = lambda t=text: self.toggle_submenu(t)
            
        btn = ctk.CTkButton(
            self.menu_inner_frame, text="", image=img, compound="left", command=command,
            width=40, height=40, fg_color="#A9A9A9", hover_color="#888888",
            font=("Georgia", 14), anchor="w"
        )
        btn.image = img
        btn.pack(pady=3, padx=3)
        self.menu_widgets[text.lower()] = btn
        return btn
        
    def _create_submenu(self, parent_text, submenu_items, parent_button):
        """Crear submenú para opciones específicas"""
        submenu_key = parent_text.lower()
        
        # Inicializar estado
        self.submenu_states[submenu_key] = False
        
        # Crear frame del submenú
        submenu_frame = ctk.CTkFrame(self.menu_inner_frame, fg_color="transparent")
        submenu_frame.pack_forget()
        
        # Crear botones del submenú
        submenu_buttons = []
        for option_text, option_command in submenu_items.items():
            sub_btn = ctk.CTkButton(
                submenu_frame, text="", width=35, height=35,
                fg_color="#808080", hover_color="#606060",
                font=("Georgia", 11), anchor="w", command=option_command
            )
            sub_btn.pack(pady=2, padx=(20, 3))
            submenu_buttons.append((sub_btn, option_text))
        
        # Guardar widgets del submenú
        self.submenu_widgets[submenu_key] = {
            "frame": submenu_frame,
            "buttons": submenu_buttons,
            "parent_button": parent_button
        }
                
    def toggle_submenu(self, section):
        """Alternar visibilidad de submenú"""
        section_key = section.lower()
        
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
            # Mostrar submenú después del botón padre
            submenu_data["frame"].pack(after=submenu_data["parent_button"], fill="x", padx=10)
            self._update_submenu_visibility(section_key)
        else:
            submenu_data["frame"].pack_forget()
                
    def setup_menu_events(self):
        """Configurar eventos del menú"""
        # Widgets principales para bind
        main_widgets = [self.sidebar, self.logo_container, self.menu_widgets['icon']]
        main_widgets.extend([widget for key, widget in self.menu_widgets.items() 
                           if key not in ['title', 'icon']])
        
        # Bind eventos principales
        for widget in main_widgets:
            widget.bind("<Enter>", lambda e: self.toggle_menu(True))
            widget.bind("<Leave>", lambda e: self.toggle_menu(False))
            
        # Bind eventos de submenús
        for submenu_data in self.submenu_widgets.values():
            submenu_data["frame"].bind("<Enter>", lambda e: self.toggle_menu(True))
            submenu_data["frame"].bind("<Leave>", lambda e: self.toggle_menu(False))
            
            for btn, text in submenu_data["buttons"]:
                btn.bind("<Enter>", lambda e: self.toggle_menu(True))
                btn.bind("<Leave>", lambda e: self.toggle_menu(False))
            
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
        self.menu_widgets['title'].pack(side="left", padx=(0, 10))
        
        # Actualizar botones principales
        button_texts = {
            'home': 'Home',
            'empleados': 'Empleados',
            'contratos': 'Contratos',
            'afiliaciones': 'Afiliaciones',
            'reportes': 'Reportes',
            'usuarios': 'Usuarios'
        }
        
        for key, text in button_texts.items():
            if key in self.menu_widgets:
                self.menu_widgets[key].configure(text=f"  {text}", width=180, anchor="w")
                
        # Actualizar submenús visibles
        for section_key, is_visible in self.submenu_states.items():
            if is_visible:
                self._update_submenu_visibility(section_key)
                
    def _collapse_menu_delayed(self):
        """Contraer menú con verificación de posición del cursor"""
        if self._cursor_over_sidebar():
            return
        
        self.menu_expanded = False
        self.sidebar.place_configure(width=self.menu_width["collapsed"])
        self.menu_widgets['title'].pack_forget()
        
        # Restaurar botones principales
        for key, widget in self.menu_widgets.items():
            if key not in ['title', 'icon']:
                widget.configure(text="", width=40, anchor="center")
                
        # Ocultar texto de submenús
        for submenu_data in self.submenu_widgets.values():
            for btn, text in submenu_data["buttons"]:
                btn.configure(text="", width=35)
                
    def _update_submenu_visibility(self, section_key):
        """Actualizar visibilidad de opciones del submenú"""
        if section_key in self.submenu_widgets:
            submenu_data = self.submenu_widgets[section_key]
            for btn, text in submenu_data["buttons"]:
                if self.menu_expanded:
                    btn.configure(text=f"    • {text}", width=160)
                else:
                    btn.configure(text="", width=35)
                
    def _cursor_over_sidebar(self):
        """Verificar si el cursor está sobre el sidebar"""
        try:
            x, y = self.winfo_pointerxy()
            sx, sy = self.sidebar.winfo_rootx(), self.sidebar.winfo_rooty()
            sw, sh = self.sidebar.winfo_width(), self.sidebar.winfo_height()
            return sx <= x <= sx + sw and sy <= y <= sy + sh
        except:
            return False
            
    def init_header(self):
        """Crear header con logo institucional e información del usuario"""
        self._create_institutional_logo()
        
        # Contenedor de usuario
        self.user_container = ctk.CTkFrame(self.header, fg_color="transparent")
        self.user_container.pack(side="right", padx=10)
        
        # Información del usuario
        user_info = ctk.CTkLabel(
            self.user_container, 
            text=f"Bienvenido {self.username} | Rol: {self.rol}", 
            font=("Georgia", 14), 
            text_color="black"
        )
        user_info.pack(side="left", padx=(0, 10))
        
        # Botón de usuario expandible
        self.user_button = ctk.CTkButton(
            self.user_container, text="▼", width=30, height=30,
            fg_color="#888888", hover_color="#666666",
            font=("Georgia", 12, "bold"), command=self.toggle_user_menu
        )
        self.user_button.pack(side="right")

        # Botón de cerrar sesión
        self.logout_button = ctk.CTkButton(
            self.main_container, text="Cerrar sesión", width=120, height=40,
            text_color="black", fg_color="#D12B1B", hover_color="#C00013",
            font=("Georgia", 12), command=self.cerrar_sesion
        )
        self.logout_button.place_forget()
        
    def _create_institutional_logo(self):
        """Crear logo institucional en el header"""
        try:
            logo_path = os.path.join(os.getcwd(), "images", "logo2.png")
            logo_img = ctk.CTkImage(dark_image=Image.open(logo_path), size=(60, 60))
            logo_label = ctk.CTkLabel(self.header, image=logo_img, text="")
            logo_label.image = logo_img
            logo_label.pack(side="left", padx=10)
        except Exception:
            logo_label = ctk.CTkLabel(
                self.header, text="🏛️ FCCP", 
                font=("Arial", 16, "bold"), text_color="white"
            )
            logo_label.pack(side="left", padx=10)
        
    def toggle_user_menu(self):
        """Alternar botón de cerrar sesión desplegable"""
        if not self.user_button_expanded:
            self.user_button_expanded = True
            self.user_button.configure(text="▲")
            self.logout_button.place(x=self.winfo_width() - 120, y=2)
            self.logout_button.lift()
        else:
            self.user_button_expanded = False
            self.user_button.configure(text="▼")
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
        """Mostrar vista específica usando configuración centralizada"""
        if view_name not in self.views:
            return
            
        self.clear_content_area()
        module_name, class_name, placeholder_text = self.views[view_name]
        
        # Modificar el título según la acción
        if action:
            action_text = "Registro" if action == "registrar" else "Búsqueda"
            placeholder_text = f"{action_text} de {view_name.title()}"
        
        try:
            module = __import__(module_name, fromlist=[class_name])
            crud_class = getattr(module, class_name)
            # Pasar la acción como parámetro si la clase lo soporta
            if action:
                try:
                    crud = crud_class(self.content_area, self.username, self.rol, action)
                except TypeError:
                    crud = crud_class(self.content_area, self.username, self.rol)
            else:
                crud = crud_class(self.content_area, self.username, self.rol)
            crud.pack(fill="both", expand=True, padx=10, pady=10)
        except ImportError:
            self.create_view_placeholder(placeholder_text)
        
    def show_default_view(self):
        """Vista por defecto con diseño geométrico"""
        self.clear_content_area()
        
        canvas = Canvas(self.content_area, bg="#F5F5F5", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Título principal
        self.title_label = ctk.CTkLabel(
            self.content_area,
            text="Bienvenidos al programa de gestion de\n\npersonal . Fundacion colegio ciudad de\n\nPiendamo(FCCP)",
            font=("Georgia", 24, "bold"),
            text_color="#333333"
        )
        self.title_label.place(relx=0.55, rely=0.45, anchor="center")
        
        # Frame para contenido
        welcome_frame = ctk.CTkFrame(canvas, fg_color="transparent")
        welcome_window = canvas.create_window(0, 0, window=welcome_frame, anchor="nw")
        
        # Polígonos para el fondo (mantenidos exactamente igual)
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
            
    def cerrar_sesion(self):
        """Cerrar sesión con confirmación"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas cerrar sesión?"):
            self.destroy()

def inicializar_dashboard(username, rol):
    """Inicializar dashboard"""
    dashboard = Dashboard(username, rol)
    dashboard.mainloop()

if __name__ == "__main__":
    inicializar_dashboard("usuario_ejemplo", "administrador")
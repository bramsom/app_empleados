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
        
        # Inicializar header después de crear main_container
        self.init_header()
    
        # Área de contenido
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="#F5F5F5")
        self.content_area.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self.main_container, width=self.menu_width["collapsed"], fg_color="#A9A9A9")
        self.sidebar.place(x=2, y=2, relheight=1.0)
        
        self.create_menu()
        self.setup_menu_events()
        
    def create_menu(self):
        """Crear menú con íconos desde carpeta 'images'"""
        ruta_img = os.path.join(os.getcwd(), "images")
        
        # Configuración del menú
        menu_items = [
            ("logo.png", "MENÚ", None, True),
            ("home.png", "Home", self.show_default_view),
            ("emplooye.png", "Gestion Empleados", lambda: self.show_view("empleados")),
            ("contract.png", "Contratos", lambda: self.show_view("contratos")),
            ("affiliation.png", "Afiliaciones", lambda: self.show_view("afiliaciones")),
            ("export.png", "Exportar excel/pdf", lambda: self.create_view_placeholder("Reportes y Estadísticas")),
            ("config.png", "Administrar Usuarios", lambda: self.show_view("usuarios"))
        ]
        
        self.menu_widgets = {}
        
        for item in menu_items:
            icon_file, text, command = item[:3]
            is_title = len(item) > 3
            
            image_path = os.path.join(ruta_img, icon_file)
            img = ctk.CTkImage(dark_image=Image.open(image_path), size=(24, 24))

            if is_title:
                self._create_menu_title(img, text)
            else:
                self._create_menu_button(img, text, command)
                
    def _create_menu_title(self, img, text):
        """Crear título del menú con logo"""
        self.logo_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.logo_container.pack(pady=(20, 20), fill="x")
        
        self.menu_widgets['icon'] = ctk.CTkLabel(self.logo_container, image=img, text="")
        self.menu_widgets['icon'].image = img
        self.menu_widgets['icon'].pack(side="left", padx=(15, 10))
        
        self.menu_widgets['title'] = ctk.CTkLabel(self.logo_container, text=text, font=("Georgia", 16))
        self.menu_widgets['title'].pack_forget()
        
    def _create_menu_button(self, img, text, command):
        """Crear botón del menú"""
        btn = ctk.CTkButton(
            self.sidebar, text="", image=img, compound="left", command=command,
            width=40, height=40, fg_color="#A9A9A9", hover_color="#888888",
            font=("Georgia", 14), anchor="w",text_color="black"
        )
        btn.image = img
        btn.pack(pady=3, padx=3)
        self.menu_widgets[text.lower().replace(" ", "_")] = btn
                
    def setup_menu_events(self):
        """Configurar eventos del menú"""
        widgets_to_bind = [self.sidebar, self.logo_container, self.menu_widgets['icon']] + [
            widget for key, widget in self.menu_widgets.items() 
            if key not in ['title', 'icon']
        ]
        
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
        self.menu_widgets['title'].pack(side="left", padx=(0, 10))
        
        # Actualizar botones con texto
        for key, widget in self.menu_widgets.items():
            if key not in ['title', 'icon']:
                original_text = key.replace("_", " ").title()
                widget.configure(text=f"  {original_text}", width=180, anchor="w")
                
    def _collapse_menu_delayed(self):
        """Contraer menú con verificación de posición del cursor"""
        if self._cursor_over_sidebar():
            return
        
        self.menu_expanded = False
        self.sidebar.place_configure(width=self.menu_width["collapsed"])
        self.menu_widgets['title'].pack_forget()
        
        # Restaurar botones solo con iconos
        for key, widget in self.menu_widgets.items():
            if key not in ['title', 'icon']:
                widget.configure(text="", width=40, anchor="center")
                
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
        # Logo institucional
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
                font=("Georgia", 16, "bold"), text_color="black"
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
        placeholder = ctk.CTkLabel(self.content_area, text=title, font=("Georgia", 24, "bold"))
        placeholder.pack(expand=True)
        
    def show_view(self, view_name):
        """Mostrar vista específica usando configuración centralizada"""
        if view_name not in self.views:
            return
            
        self.clear_content_area()
        module_name, class_name, placeholder_text = self.views[view_name]
        
        try:
            module = __import__(module_name, fromlist=[class_name])
            crud_class = getattr(module, class_name)
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
        
        # Polígonos para el fondo
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
            (f"Bienvenido, {self.username}", ("Georgia", 28, "bold"), None),
            (f"Rol: {self.rol}", ("Georgia", 16), None),
            ("Pasa el cursor sobre el menú lateral para expandir las opciones", ("Georgia", 14), "black")
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
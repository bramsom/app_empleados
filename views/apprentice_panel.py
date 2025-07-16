import customtkinter as ctk
from tkinter import Canvas, messagebox

class Dashboard(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.username = username
        self.rol = rol
        self.menu_expanded = False
        self.menu_width = {"collapsed": 60, "expanded": 200}
        
        self.setup_window()
        self.create_layout()
        self.show_default_view()
        
    def setup_window(self):
        """Configuración inicial de la ventana"""
        self.geometry("1200x800")
        self.title("Dashboard - Sistema de Gestión")
        
    def create_layout(self):
        """Crear layout principal con header, sidebar y contenido"""
        # Header
        self.header = ctk.CTkFrame(self, height=60, fg_color="#A9A9A9")
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        self.init_header()
        
        # Contenedor principal para el área debajo del header
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(side="top", fill="both", expand=True)
        
        # Área de contenido (ocupa todo el espacio disponible)
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="#F5F5F5")
        self.content_area.pack(fill="both", expand=True, padx=2, pady=2)
        
        # Sidebar sobrepuesto usando place (se posiciona encima del contenido)
        self.sidebar = ctk.CTkFrame(
            self.main_container, 
            width=self.menu_width["collapsed"],
            
            fg_color="#A9A9A9"
        )
        # Posicionar el sidebar en la esquina superior izquierda del main_container
        self.sidebar.place(x=2, y=2,relheight=1.0)  # height ajustado para el contenedor
        
        self.create_menu()
        self.setup_menu_events()
        
    def create_menu(self):
        """Crear menú con configuración unificada"""
        # Configuración del menú
        self.menu_config = [
            ("☰", "MENÚ", None, True),  # Icono especial del menú
            ("🏠", "Home", self.show_default_view, False),
            ("👥", "Gestion Empleados", self.show_empleados_view, False),
            ("🏢", "Contratos", self.show_contratos_view, False),
            ("🗼", "Afiliaciones", self.show_afiliaciones_view, False),
            ("[]–>", "Exportar excel/pdf", self.show_reportes_view, False),
            ("🧭", "Administrar Usuarios", self.show_usuarios_view, False),
            ("(–", "Cerrar Sesión", self.cerrar_sesion, False)
        ]
        
        self.menu_widgets = {}
        
        # Crear widgets del menú
        for i, (icon, text, command, is_title) in enumerate(self.menu_config):
            if is_title:
                # Título del menú
                self.menu_widgets['title'] = ctk.CTkLabel(self.sidebar, text=text, font=("Georgia", 16))
                self.menu_widgets['title'].pack_forget()
                # Icono hamburguesa
                self.menu_widgets['icon'] = ctk.CTkLabel(self.sidebar, text=icon, font=("Georgia", 24))
                self.menu_widgets['icon'].pack(pady=(20, 10))
            else:
                # Botones del menú
                btn_config = {
                    "text": icon, "command": command, "width": 40, "height": 40,
                    "fg_color": "#A9A9A9","font":("Georgia", 16),"hover_color": "#888888"
                }
                if text == "Cerrar Sesión":
                    btn_config.update({"fg_color": "red", "hover_color": "darkred"})
                    
                btn = ctk.CTkButton(self.sidebar, **btn_config)
                pack_config = {"pady": 10, "padx": 10}
                if text == "Cerrar Sesión":
                    pack_config.update({"side": "bottom", "pady": 20})
                    
                btn.pack(**pack_config)
                self.menu_widgets[text.lower().replace(" ", "_")] = btn
                
    def setup_menu_events(self):
        """Configurar eventos del menú de forma unificada"""
        widgets_to_bind = [self.sidebar, self.menu_widgets['icon']] + [
            widget for key, widget in self.menu_widgets.items() 
            if key not in ['title', 'icon']
        ]
        
        for widget in widgets_to_bind:
            widget.bind("<Enter>", lambda e: self.toggle_menu(True))
            widget.bind("<Leave>", lambda e: self.toggle_menu(False))
            
    def toggle_menu(self, expand):
        """Alternar estado del menú"""
        if expand and not self.menu_expanded:
            self.menu_expanded = True
            # Cambiar el ancho del sidebar usando place
            self.sidebar.place_configure(width=self.menu_width["expanded"])
            self.menu_widgets['title'].pack(pady=(20, 30))
            self.menu_widgets['icon'].pack_forget()
            
            # Actualizar botones con texto
            for i, (icon, text, command, is_title) in enumerate(self.menu_config):
                if not is_title:
                    key = text.lower().replace(" ", "_")
                    self.menu_widgets[key].configure(text=text, width=160, height=40)
                    self.menu_widgets[key].pack_configure(padx=20, fill="both")
                    
        elif not expand and self.menu_expanded:
            self.after(100, self._collapse_menu_delayed)
            
    def _collapse_menu_delayed(self):
        """Contraer menú con verificación de posición del cursor"""
        if self._cursor_over_sidebar():
            return
            
        self.menu_expanded = False
        # Cambiar el ancho del sidebar usando place
        self.sidebar.place_configure(width=self.menu_width["collapsed"])
        self.menu_widgets['title'].pack_forget()
        self.menu_widgets['icon'].pack(pady=(20, 10))
        
        # Restaurar botones con iconos
        for i, (icon, text, command, is_title) in enumerate(self.menu_config):
            if not is_title:
                key = text.lower().replace(" ", "_")
                self.menu_widgets[key].configure(text=icon, width=40, height=40)
                self.menu_widgets[key].pack_configure(padx=10, fill="both")
                
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
        """Crear header con información del usuario"""
        header_items = [
            ("left", f"👤 {self.username}", {"font": ("Arial", 14, "bold"), "text_color": "white"}),
            ("left", f"Rol: {self.rol}", {"font": ("Arial", 14), "text_color": "white"}),
            ("right", "Cerrar sesión", {"fg_color": "red", "hover_color": "darkred", "command": self.cerrar_sesion})
        ]
        
        for side, text, config in header_items:
            if side == "right":
                widget = ctk.CTkButton(self.header, text=text, width=120, **config)
            else:
                widget = ctk.CTkLabel(self.header, text=text, **config)
            widget.pack(side=side, padx=20 if side == "left" else 20)
            
    def clear_content_area(self):
        """Limpiar área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
    def create_view_placeholder(self, title):
        """Crear placeholder para vistas"""
        placeholder = ctk.CTkLabel(self.content_area, text=title, font=("Arial", 24, "bold"))
        placeholder.pack(expand=True)
        
    def show_empleados_view(self):
        """Vista de empleados"""
        self.clear_content_area()
        try:
            from views.crud_employees import CrudEmpleados
            crud = CrudEmpleados(self.content_area, self.username, self.rol)
            crud.pack(fill="both", expand=True, padx=10, pady=10)
        except ImportError:
            self.create_view_placeholder("Gestión de Empleados")
            
    def show_contratos_view(self):
        """Vista de contratos"""
        self.clear_content_area()
        try:
            from views.crud_contracts import CrudContratos
            crud = CrudContratos(self.content_area, self.username, self.rol)
            crud.pack(fill="both", expand=True, padx=10, pady=10)
        except ImportError:
            self.create_view_placeholder("Gestión de contratos")
        
    def show_afiliaciones_view(self):
        self.clear_content_area()
        try:
            from views.crud_afiliations import CrudAfiliaciones
            crud = CrudAfiliaciones(self.content_area, self.username, self.rol)
            crud.pack(fill="both", expand=True, padx=10, pady=10)
        except ImportError:
            self.create_view_placeholder("Gestión de afiliaciones")
        
    def show_reportes_view(self):
        self.clear_content_area()
        self.create_view_placeholder("Reportes y Estadísticas")
        
    def show_usuarios_view(self):
        self.clear_content_area()
        try:
            from views.crud_users import CrudUsuarios
            crud = CrudUsuarios(self.content_area, self.username, self.rol)
            crud.pack(fill="both", expand=True, padx=10, pady=10)
        except ImportError:
            self.create_view_placeholder("Gestion de usuarios y roles")
        
    def show_default_view(self):
        """Vista por defecto con diseño geométrico"""
        self.clear_content_area()
        
        canvas = Canvas(self.content_area, bg="#F5F5F5", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        # Frame para contenido
        welcome_frame = ctk.CTkFrame(canvas, fg_color="transparent")
        welcome_window = canvas.create_window(0, 0, window=welcome_frame, anchor="nw")
        
        # Definir polígonos para el fondo
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
            
            # Dibujar polígonos
            for points, color in polygons:
                canvas.create_polygon(points, fill=color, outline="")
                
            # Centrar contenido
            canvas.coords(welcome_window, width // 2 - 150, height // 2 - 80)
            
        canvas.bind("<Configure>", update_canvas)
        
        # Contenido de bienvenida
        welcome_content = [
            (f"Bienvenido, {self.username}", ("Arial", 28, "bold")),
            (f"Rol: {self.rol}", ("Arial", 16)),
            ("Pasa el cursor sobre el menú lateral para expandir las opciones", ("Arial", 14))
        ]
        
        for i, (text, font) in enumerate(welcome_content):
            label = ctk.CTkLabel(welcome_frame, text=text, font=font)
            if i == 2:  # Última etiqueta
                label.configure(text_color="gray")
            label.pack(expand=True if i == 0 else False, pady=(0, 10) if i == 1 else 10)
            
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
import customtkinter as ctk
import tkinter as tk
from tkinter import Canvas
from PIL import Image
import math

class Dashboard(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.username = username
        self.rol = rol
        self.title("Sistema de Gestión de Personal")
        self.geometry("900x600")
        
        # Configurar tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Iniciar con sidebar compactado
        self.sidebar_expand = False
        self.current_width = 60  # Ancho actual del sidebar
        
        # Configurar grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header frame
        self.header_frame = ctk.CTkFrame(self, fg_color="#a9a9a9", height=50)
        self.header_frame.place(x=0, y=0, relwidth=1.0)
        self.header_frame.grid_propagate(False)
        
        # Logo en header 
        try:
            logo_img = ctk.CTkImage(Image.open("C:/Users/Usuario/Documents/proyectos python/app_empleados/images/logo2.png"), size=(60, 60))
            logo_label = ctk.CTkLabel(self.header_frame, image=logo_img, text="", fg_color=self.header_frame.cget("fg_color"))
            logo_label.place(relx=0.001, rely=0)
        except:
            # Si no se puede cargar la imagen, usar un emoji como respaldo
            logo_label = ctk.CTkLabel(self.header_frame, text="🛡️", font=("Arial", 20), text_color="white")
            logo_label.place(relx=0.001, rely=0.5, anchor="w")
        
        # Información de usuario
        self.user_info_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.user_info_frame.pack(side="right", padx=10, pady=10)

        self.user_info_frame.grid_columnconfigure(0, weight=1)
        self.user_info_frame.grid_columnconfigure(1, weight=0)
        
        self.welcome_label = ctk.CTkLabel(
            self.user_info_frame, 
            text=f"Bienvenido, {self.username}",
            font=("Georgia", 12),
            text_color="white"
        )
        self.welcome_label.grid(row=0, column=0, sticky="e", padx=(0, 10))
        
        # Botón cerrar sesión
        self.user_icon_button = ctk.CTkButton(
            self.user_info_frame,
            text="👤",  # O usa una imagen si tienes una
            width=40,
            height=30,
            font=("Arial", 18),
            fg_color="transparent",
            hover_color="#AAAAAA",
            command=self.toggle_user_menu
        )
        self.user_icon_button.grid(row=0, column=1)

        # Sidebar frame - iniciar compactado
        self.sidebar_frame = ctk.CTkFrame(self, fg_color="#A9A9A9", width=60)
        self.sidebar_frame.place(x=0, y=50, relheight=1.0)
        self.sidebar_frame.grid_propagate(False)
        
        # Configurar eventos de hover para el sidebar
        self.sidebar_frame.bind("<Enter>", self.on_sidebar_enter)
        self.sidebar_frame.bind("<Leave>", self.on_sidebar_leave)
        
        # Main content frame
        self.content_frame = ctk.CTkFrame(self, fg_color="#F5F5F5")
        self.content_frame.place(x=60, y=50, relwidth=1.0, relheight=1.0)
        
        # Navigation buttons data con iconos más apropiados
        self.nav_data = [
            {"text": "Inicio", "icon": "🏠"},
            {"text": "Empleados", "icon": "👥"},
            {"text": "Reportes", "icon": "📋"},
            {"text": "Configuración", "icon": "⚙️"},
            {"text": "Documentos", "icon": "📄"},
            {"text": "Configuración", "icon": "🔧"}
        ]
        
        # Navigation buttons - iniciar solo con iconos
        self.nav_buttons = []
        for i, item in enumerate(self.nav_data):
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=item["icon"],
                fg_color="#A9A9A9",
                hover_color="#888888",
                text_color="white",
                font=("Arial", 16),
                command=lambda t=item["text"]: self.navigate_to(t),
                width=40,
                height=40,
                corner_radius=8
            )
            btn.pack(pady=9, padx=9)
            self.nav_buttons.append(btn)
            
            # Agregar eventos de hover a cada botón
            btn.bind("<Enter>", lambda e, b=btn: self.on_button_hover(e, b))
            btn.bind("<Leave>", lambda e, b=btn: self.on_button_leave(e, b))
        
        # Contenido principal con canvas decorativo
        self.setup_main_content()

        # Asegurar que el sidebar y header estén en la parte superior
        self.sidebar_frame.lift()
        self.header_frame.lift()

    def toggle_user_menu(self):
        if hasattr(self, "user_menu") and self.user_menu.winfo_exists():
            self.user_menu.destroy()
        else:
            self.user_menu = tk.Menu(self, tearoff=0)
            self.user_menu.add_command(label="Cerrar sesión", command=self.logout)
        
        # Posicionar el menú debajo del botón
        x = self.user_icon_button.winfo_rootx()
        y = self.user_icon_button.winfo_rooty() + self.user_icon_button.winfo_height()
        self.user_menu.tk_popup(x, y)
    
    def setup_main_content(self):
        """Configurar el contenido principal con canvas decorativo responsivo"""
        # Frame para el contenido central - SIN especificar tamaño
        self.main_content_frame = ctk.CTkFrame(self.content_frame, fg_color="#FFEFEF")
        self.main_content_frame.pack(fill="both", expand=True)
        
        # Canvas para elementos decorativos - SIN especificar tamaño inicial
        self.canvas = Canvas(self.main_content_frame, bg="#FFEFEF", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Título principal sobre el canvas
        self.title_label = ctk.CTkLabel(
            self.main_content_frame,
            text="Bienvenido al programa de gestión de\n\npersonal. Fundación Colegio Ciudad de\n\nPiendamó (FCCP)",
            font=("Georgia", 24, "bold"),
            text_color="#333333"
        )
        self.title_label.place(relx=0.5, rely=0.4, anchor="center")
        
        # Vincular el evento de redimensionamiento para redibujar el canvas
        self.canvas.bind("<Configure>", self.on_canvas_configure)
    
    def on_canvas_configure(self, event):
        """Redibujar el canvas cuando cambie de tamaño"""
        # Obtener las dimensiones actuales del canvas
        width = event.width
        height = event.height
        
        # Limpiar el canvas
        self.canvas.delete("all")
        
        # Redibujar los elementos decorativos con proporciones relativas
        self.draw_decorative_elements(width, height)
    
    def draw_decorative_elements(self, width, height):
        """Dibujar elementos decorativos ajustados al tamaño del canvas"""
        # Calcular proporciones basadas en el tamaño original (900x600)
        w_ratio = width / 900
        h_ratio = height / 600
        
        # Función auxiliar para escalar coordenadas
        def scale_coords(coords):
            scaled = []
            for i, coord in enumerate(coords):
                if i % 2 == 0:  # coordenada x
                    scaled.append(int(coord * w_ratio))
                else:  # coordenada y
                    scaled.append(int(coord * h_ratio))
            return scaled
        
        # Redibujar todos los polígonos con coordenadas escaladas
        polygons = [
            ([550, 0, 650, 0, 844, 251, 794, 315], "#D2D2D2"),
            ([710,135, 760, 69, 900, 250, 900, 382], "#888888"),
            ([785, 0, 900, 0, 900, 150, 900, 150], "#D2D2D2"),
            ([670, 0, 780, 0, 860, 105, 806, 176], "#D12B1B"),
            ([600, 0, 603, 0, 803, 259, 800, 260], "#FCFCFC"),
            ([729, 0, 726, 0, 829, 135, 830, 131], "#FCFCFC"),
            ([250, 600, 350, 600, 80, 251, 30, 315], "#D2D2D2"),
            ([0, 240, 0, 365, 130, 533, 178, 470], "#888888"),
            ([190, 600, 90, 600, 0, 485, 51, 420], "#D12B1B"),
            ([144, 600, 148, 600, 40, 460, 38, 463], "#FCFCFC"),
            ([307, 600, 312, 600, 151, 392, 148, 395], "#FCFCFC")
        ]
        
        # Dibujar cada polígono escalado
        for coords, color in polygons:
            scaled_coords = scale_coords(coords)
            self.canvas.create_polygon(scaled_coords, fill=color, outline="")
    
    def on_sidebar_enter(self, event):
        """Expandir sidebar cuando el cursor entra - SIN ANIMACIÓN"""
        if not self.sidebar_expand:
            self.expand_sidebar()
    
    def on_sidebar_leave(self, event):
        """Compactar sidebar cuando el cursor sale - SIN ANIMACIÓN"""
        if self.sidebar_expand:
            # Verificar si el cursor realmente salió del sidebar
            x = self.winfo_pointerx() - self.winfo_rootx()
            if x > 200:  # Si está fuera del área del sidebar expandido
                self.compact_sidebar()
                
    def on_button_hover(self, event, button):
        """Efecto hover adicional para botones"""
        button.configure(fg_color="#888888")
    
    def on_button_leave(self, event, button):
        """Restaurar color normal del botón"""
        button.configure(fg_color="#A9A9A9")
    
    def expand_sidebar(self):
        """Expandir el sidebar - CAMBIO INMEDIATO"""
        self.sidebar_frame.configure(width=200)
        self.current_width = 200
        self.sidebar_expand = True
        
        # Actualizar botones inmediatamente
        for i, btn in enumerate(self.nav_buttons):
            btn.configure(
                text=f"{self.nav_data[i]['icon']} {self.nav_data[i]['text']}", 
                width=180
            )
    
    def compact_sidebar(self):
        """Compactar el sidebar - CAMBIO INMEDIATO"""
        self.sidebar_frame.configure(width=60)
        self.current_width = 60
        self.sidebar_expand = False
        
        # Actualizar botones inmediatamente
        for i, btn in enumerate(self.nav_buttons):
            btn.configure(
                text=self.nav_data[i]['icon'], 
                width=40
            )
    
    def navigate_to(self, page_name):
        """Navegar a una página específica"""
        self.title_label.configure(text=f"Estás ahora en la página de {page_name}")
    
    def logout(self):
        """Cerrar sesión"""
        self.title_label.configure(text="Cerrando sesión...")
        # Aquí podrías agregar lógica para cerrar sesión

if __name__ == "__main__":
    app = Dashboard()
    app.mainloop()
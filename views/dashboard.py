# In your main file (app.py or dashboard.py)

import customtkinter as ctk
from views.view_manager import ViewManager
from views.sidebar_manager import SidebarManager
from tkinter import Canvas, messagebox
from PIL import Image
from utils.canvas import agregar_fondo_decorativo
import os  # Make sure this is imported for file path operations

class Dashboard(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.username = username
        self.rol = rol
        self.user_button_expanded = False
        
        # Correctly define menu_width here, as it's used in create_layout
        self.menu_width = {"collapsed": 60, "expanded": 200}
        
        self.setup_window()
        
        # Initialize the main UI components
        self.create_layout()

        # Initialize the managers with their respective responsibilities
        self.view_manager = ViewManager(
            self.content_area, 
            self.username, 
            self.rol, 
            self.show_default_view
        )
        
        # Pass a reference to the main app instance to the SidebarManager
        self.sidebar_manager = SidebarManager(self.sidebar, self.view_manager, self)
        
        self.show_default_view()

    def setup_window(self):
        """Initial window configuration."""
        self.geometry("1100x600")
        self.title("Dashboard - Sistema de Gestión")

    def create_layout(self):
        """Creates the main layout."""
        # Header
        self.header = ctk.CTkFrame(self, height=60, fg_color="#A9A9A9")
        self.header.pack(side="top", fill="x")
        self.header.pack_propagate(False)
        
        # Main container
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(side="top", fill="both", expand=True)
        
        self.init_header()
        
        # Content area
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="#F5F5F5")
        self.content_area.pack(fill="both", expand=True, padx=2, pady=2)
        
        self.sidebar = ctk.CTkFrame(self.main_container, width=self.menu_width["collapsed"], fg_color="#A9A9A9")
        self.sidebar.place(x=2, y=2, relheight=1.0)
        
        
    def init_header(self):
        """Creates the header."""
        self._create_institutional_logo()
        
        self.user_container = ctk.CTkFrame(self.header, fg_color="transparent")
        self.user_container.pack(side="right", padx=10)
        
        ctk.CTkLabel(
            self.user_container, 
            text=f"Bienvenido {self.username} | Rol: {self.rol}", 
            font=("Georgia", 14), text_color="black"
        ).pack(side="left", padx=(0, 50))
        
        icon_path = os.path.join(os.getcwd(), "images", "logout.png")
        user_img = ctk.CTkImage(dark_image=Image.open(icon_path), size=(24, 24))

        self.user_button = ctk.CTkButton(
            self.user_container, text="", image=user_img, width=36, height=36,
            fg_color="#A9A9A9", hover_color="#888888", command=self.toggle_user_menu
        )
        self.user_button.image = user_img
        self.user_button.pack(side="right", padx=(50, 30))

        self.logout_button = ctk.CTkButton(
            self.main_container, text="Cerrar sesión", width=120, height=40,
            text_color="black", fg_color="#D12B1B", hover_color="#C00013",
            font=("Georgia", 12), command=self.cerrar_sesion
        )
        self.logout_button.place_forget()

    def _create_institutional_logo(self):
        """Creates the institutional logo."""
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
        """Toggles the user menu."""
        if not self.user_button_expanded:
            self.user_button_expanded = True
            # Use self.winfo_width() from the main app window
            self.logout_button.place(x=self.winfo_width() - 120, y=2)
            self.logout_button.lift()
        else:
            self.user_button_expanded = False
            self.logout_button.place_forget()
            
    def show_default_view(self):
        """Displays the home screen with geometric design."""
        # Use the ViewManager to clear the content area
        self.view_manager.clear_content_area()
        
        canvas = Canvas(self.content_area, bg="#F5F5F5", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(
            self.content_area,
            text="Bienvenidos al programa de gestion de\n\npersonal . Fundacion colegio ciudad de\n\nPiendamo(FCCP)",
            font=("Georgia", 24, "bold"), text_color="#333333"
        )
        self.title_label.place(relx=0.55, rely=0.45, anchor="center")

        agregar_fondo_decorativo(canvas)    
        
    
    def cerrar_sesion(self):
        """Logs out the user."""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas cerrar sesión?"):
            self.destroy()
# File: views/sidebar_manager.py

import customtkinter as ctk
from PIL import Image
import os
from tkinter import messagebox

class SidebarManager:
    def __init__(self, sidebar_frame, view_manager, main_app_instance):
        self.sidebar_frame = sidebar_frame
        self.view_manager = view_manager
        self.main_app = main_app_instance  # Reference to the main app instance
        
        self.menu_expanded = False
        self.menu_width = {"collapsed": 60, "expanded": 200}
        
        # New: Create the inner frames for the menu
        self.menu_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.menu_frame.pack(fill="both", expand=True)
        self.menu_inner_frame = ctk.CTkFrame(self.menu_frame, fg_color="transparent")
        self.menu_inner_frame.pack(fill="y", anchor="n")

        self.menu_widgets = {}
        self.submenu_states = {}
        self.submenu_widgets = {}

        self.create_menu()
        self.setup_menu_events()
        
    def create_menu(self):
        """Creates the menu with a simplified configuration."""
        ruta_img = os.path.join(os.getcwd(), "images")
        
        menu_items = [
            ("logo.png", "MENÚ", None, True),
            # Correctly delegate commands to the ViewManager
            ("home.png", "Home", lambda: self.main_app.show_default_view()),
            ("emplooye.png", "Empleados", {
                "Registrar Empleado": lambda: self.view_manager.show_view("empleados_registrar"),
                "Buscar Empleado": lambda: self.view_manager.show_view("empleados_buscar")
            }),
            ("contract.png", "Contratos", {
                "Registrar Contrato": lambda: self.view_manager.show_view("contratos_registrar"),
                "Buscar Contrato": lambda: self.view_manager.show_view("contratos_buscar")
            }),
            ("affiliation.png", "Afiliaciones", {
                "Registrar Afiliación": lambda: self.view_manager.show_view("afiliaciones_registrar"),
                "Buscar Afiliación": lambda: self.view_manager.show_view("afiliaciones_buscar")
            }),
            ("export.png", "Reportes", lambda: self.view_manager.show_view("Reportes")),
            ("config.png", "Usuarios", {
                "Registrar Usuario": lambda: self.view_manager.show_view("usuarios_registrar"),
                "Buscar Usuario": lambda: self.view_manager.show_view("usuarios_buscar")
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
        """Creates a simple menu button."""
        btn = ctk.CTkButton(
            self.menu_inner_frame, text="", image=img, compound="left", command=command,
            width=60, height=60, fg_color="#A9A9A9", hover_color="#888888",
            font=("Georgia", 14), anchor="center"
        )
        btn.image = img
        btn.pack(fill="x")
        self.menu_widgets[text.lower()] = btn

    def _create_menu_with_submenu(self, img, text, submenu_items):
        """Creates a menu button with a submenu."""
        btn = ctk.CTkButton(
            self.menu_inner_frame, text="", image=img, compound="left",
            command=lambda: self.toggle_submenu(text.lower()),
            width=60, height=60, fg_color="#A9A9A9", hover_color="#888888",
            font=("Georgia", 14), anchor="center"
        )
        btn.image = img
        btn.pack(fill="x")
        self.menu_widgets[text.lower()] = btn
        
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
        """Toggles the visibility of a submenu."""
        if section_key not in self.submenu_widgets:
            return
        
        for key in list(self.submenu_states.keys()):
            if key != section_key and self.submenu_states[key]:
                self.submenu_states[key] = False
                self.submenu_widgets[key]["frame"].pack_forget()

        self.submenu_states[section_key] = not self.submenu_states[section_key]
        submenu_data = self.submenu_widgets[section_key]
        
        if self.submenu_states[section_key]:
            submenu_data["frame"].pack(after=submenu_data["parent_button"], fill="x", padx=10)
            self._update_submenu_visibility(section_key)
        else:
            submenu_data["frame"].pack_forget()

    def setup_menu_events(self):
        """Sets up the menu events."""
        widgets_to_bind = [self.sidebar_frame] + list(self.menu_widgets.values())
        
        for submenu_data in self.submenu_widgets.values():
            widgets_to_bind.append(submenu_data["frame"])
            widgets_to_bind.extend([btn for btn, _ in submenu_data["buttons"]])
        
        for widget in widgets_to_bind:
            widget.bind("<Enter>", lambda e: self.toggle_menu(True))
            widget.bind("<Leave>", lambda e: self.toggle_menu(False))

    def toggle_menu(self, expand):
        """Toggles the menu state."""
        if expand and not self.menu_expanded:
            self._expand_menu()
        elif not expand and self.menu_expanded:
            self.main_app.after(100, self._collapse_menu_delayed)
            
    def _expand_menu(self):
        """Expands the menu."""
        self.menu_expanded = True
        self.sidebar_frame.place_configure(width=self.menu_width["expanded"])
        
        if 'title' in self.menu_widgets:
            self.menu_widgets['title'].pack(side="left", padx=(0, 10))
        
        button_texts = {
            'home': 'Home', 'empleados': 'Empleados', 'contratos': 'Contratos', 
            'afiliaciones': 'Afiliaciones', 'reportes': 'Reportes', 'usuarios': 'Usuarios'
        }
        
        for key, text in button_texts.items():
            if key in self.menu_widgets:
                self.menu_widgets[key].configure(text=f"  {text}", width=200, anchor="w")
                
        for section_key, is_visible in self.submenu_states.items():
            if is_visible:
                self._update_submenu_visibility(section_key)
                
    def _collapse_menu_delayed(self):
        """Collapses the menu with a cursor check."""
        if self._cursor_over_sidebar():
            return

        self.menu_expanded = False
        self.sidebar_frame.place_configure(width=self.menu_width["collapsed"])

        if 'title' in self.menu_widgets:
            self.menu_widgets['title'].pack_forget()

        for key, widget in self.menu_widgets.items():
            widget.configure(text="", width=60, anchor="center")

        for section_key, submenu_data in self.submenu_widgets.items():
            submenu_data["frame"].pack_forget()
            self.submenu_states[section_key] = False
            for btn, _ in submenu_data["buttons"]:
                btn.configure(text="", width=35)
                
    def _update_submenu_visibility(self, section_key):
        """Updates the visibility of the submenu."""
        if section_key in self.submenu_widgets:
            submenu_data = self.submenu_widgets[section_key]
            for btn, text in submenu_data["buttons"]:
                if self.menu_expanded:
                    btn.configure(text=f"    • {text}", width=160)
                else:
                    btn.configure(text="", width=35)
                    
    def _cursor_over_sidebar(self):
        """Checks if the cursor is over the sidebar."""
        try:
            x, y = self.main_app.winfo_pointerxy()
            sx, sy = self.sidebar_frame.winfo_rootx(), self.sidebar_frame.winfo_rooty()
            sw, sh = self.sidebar_frame.winfo_width(), self.sidebar_frame.winfo_height()
            return sx <= x <= sx + sw and sy <= y <= sy + sh
        except:
            return False
import customtkinter as ctk
import tkinter as tk
from PIL import Image
from controllers.user_controller import UserController
from tkinter import messagebox
from views.users.register_users import FormularioRegistroEdicion
from utils.canvas import agregar_fondo_decorativo

class BuscarUsuarios(ctk.CTkFrame):
    def __init__(self, parent, username, rol, volver_callback):
        super().__init__(parent)
        self.volver_callback = volver_callback
        self.username = username
        self.rol = rol
        self.user_controller = UserController(current_username=self.username, current_role=self.rol)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        agregar_fondo_decorativo(self)
        self.configure(fg_color="#F5F5F5")
        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))
        
        # ==== Tarjeta principal ====
        self.card = ctk.CTkFrame(self, fg_color="#D9D9D9", corner_radius=10)
        self.card.place(relx=0.52, rely=0.5, anchor="center", relwidth=0.90, relheight=0.75)
        self.card.rowconfigure(0, weight=1)
        self.card.columnconfigure(0, weight=1)
        
        # Widgets de la interfaz
        self.title_label = ctk.CTkLabel(self, text="Gestión de Usuarios", font=("Georgia", 24, "bold"))
        self.title_label.pack(pady=(10, 5))
        
        # Frame para las tarjetas de usuarios
        self.card_frame = ctk.CTkScrollableFrame(self.card, fg_color="transparent")
        self.card_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configurar la cuadrícula para la barra de búsqueda y el botón de crear
        self.card_frame.grid_columnconfigure(0, weight=1)
        self.card_frame.grid_columnconfigure(1, weight=1)
        self.card_frame.grid_columnconfigure(2, weight=1)

        # Botón para crear usuario
        self.create_button = ctk.CTkButton(
            self,
            fg_color="#06A051", 
            hover_color="#048B45", 
            text="Crear Usuario",
            height=40, 
            font=("Georgia", 16),
            text_color="black",
            width=200,
            command=self.crear_usuario
        )
        self.create_button.place(relx=0.6, rely=0.9, anchor="ne")

        self.btn_volver = ctk.CTkButton(
            self,
            image=self.icon_back,
            text="",
            corner_radius=0,
            hover_color="#F3EFEF", 
            width=30,
            height=30,
            command=self.volver_al_panel,
            fg_color="#d2d2d2"
        )
        self.btn_volver.place(relx=0.98, rely=0.02, anchor="ne")
        
        self.cargar_usuarios()
        
    def filtrar_usuarios(self, event=None):
        query = self.search_entry.get().strip().lower()
        for widget in self.card_frame.winfo_children():
            widget.destroy()
        
        usuarios = self.user_controller.obtener_todos()
        
        col = 0
        row = 0
        for usuario in usuarios:
            if query in usuario.username.lower():
                self.crear_tarjeta_usuario(usuario, row, col)
                col += 1
                if col > 2:
                    col = 0
                    row += 1

    def crear_tarjeta_usuario(self, usuario, row, col):
        card = ctk.CTkFrame(self.card_frame, fg_color="#F3EFEF", corner_radius=10)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

        # Usamos grid para organizar mejor la información en la tarjeta
        card.grid_columnconfigure(0, weight=1)

        # Nombre de Usuario
        ctk.CTkLabel(card, text="Nombre de Usuario:", font=("Georgia", 14, "bold"), text_color="black", anchor="w").grid(row=0, column=0, sticky="w", padx=10, pady=(10, 2))
        username_entry = ctk.CTkEntry(card, height=40, fg_color="#D9D9D9", border_width=0)
        username_entry.insert(0, usuario.username)
        username_entry.configure(state="disabled")
        username_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 5))

        # Rol
        ctk.CTkLabel(card, text="Rol:", font=("Georgia", 14, "bold"), text_color="black", anchor="w").grid(row=2, column=0, sticky="w", padx=10, pady=(5, 2))
        rol_entry = ctk.CTkEntry(card, height=40, fg_color="#D9D9D9", border_width=0)
        rol_entry.insert(0, usuario.rol)
        rol_entry.configure(state="disabled")
        rol_entry.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Botones de acción en una fila separada
        button_frame = ctk.CTkFrame(card, fg_color="transparent")
        button_frame.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        
        can_edit = not (self.rol == "aprendiz" and usuario.username != self.username)
        edit_button = ctk.CTkButton(
            button_frame,
            height=40,
            font=("Georgia", 14), 
            fg_color="#06A051", 
            hover_color="#048B45", 
            text_color="black", 
            text="Editar", 
            command=lambda: self.editar_usuario(usuario)
        )
        edit_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        can_delete = self.rol != "aprendiz"
        delete_button = ctk.CTkButton(
            button_frame,
            height=40,
            font=("Georgia", 14), 
            fg_color="#D12B1B", 
            hover_color="#B81D0F", 
            text_color="black", 
            text="Eliminar",
            command=lambda: self.confirmar_eliminacion(usuario.id)
        )
        delete_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")

    def cargar_usuarios(self):
        for widget in self.card_frame.winfo_children():
            widget.destroy()
        usuarios = self.user_controller.obtener_todos()
        col = 0; row = 0
        for usuario in usuarios:
            self.crear_tarjeta_usuario(usuario, row, col)
            col += 1
            if col > 2:
                col = 0; row += 1
            
    def crear_usuario(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
        FormularioRegistroEdicion(
            parent=self.master,
            user_controller=self.user_controller, 
            volver_callback=self.volver_al_panel
        ).pack(fill="both", expand=True)

    def editar_usuario(self, usuario):
        for widget in self.master.winfo_children():
            widget.destroy()

        FormularioRegistroEdicion(
            parent=self.master, 
            user_controller=self.user_controller,
            usuario_a_editar=usuario, 
            volver_callback=self.volver_al_panel
        ).pack(fill="both", expand=True)

    def confirmar_eliminacion(self, user_id):
        if messagebox.askyesno("Confirmar eliminación", "¿Estás seguro de que deseas eliminar este usuario?"):
            try:
                self.user_controller.eliminar(user_id)
                messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
                self.cargar_usuarios()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el usuario: {e}")

    def volver_al_panel(self):
        if self.volver_callback:
            self.destroy()
            self.volver_callback()

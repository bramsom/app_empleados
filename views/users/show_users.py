import customtkinter as ctk
import tkinter as tk
from PIL import Image
from controllers.user_controller import UserController
from tkinter import messagebox

class BuscarUsuarios(ctk.CTkFrame):
    def __init__(self, parent, volver_callback):
        super().__init__(parent)
        self.volver_callback = volver_callback
        self.user_controller = UserController()
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Cargar iconos
        self.icon_add = ctk.CTkImage(Image.open("images/add.png"), size=(20, 20))
        self.icon_search = ctk.CTkImage(Image.open("images/search.png"), size=(20, 20))
        self.icon_edit = ctk.CTkImage(Image.open("images/edit.png"), size=(20, 20))
        self.icon_delete = ctk.CTkImage(Image.open("images/delete.png"), size=(20, 20))
        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))

        # Marco superior para el título y botones de acción
        top_frame = ctk.CTkFrame(self, fg_color="#F2F2F2")
        top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        top_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkButton(
            top_frame,
            image=self.icon_back,
            text="",
            corner_radius=0,
            width=40,
            height=40,
            fg_color="#D2D2D2",
            hover_color="#E0E0E0",
            command=self.volver_callback
        ).grid(row=0, column=0, sticky="w", padx=(15, 0))

        ctk.CTkLabel(
            top_frame,
            text="GESTIÓN DE USUARIOS",
            font=("Georgia", 20, "bold"),
            text_color="#282828"
        ).grid(row=0, column=0, sticky="nsew")

        # Frame para la barra de búsqueda y botón de nuevo usuario
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar usuario...",
            corner_radius=20,
            width=300
        )
        self.search_entry.grid(row=0, column=0, padx=(10, 5), pady=5, sticky="e")

        ctk.CTkButton(
            search_frame,
            text="Buscar",
            image=self.icon_search,
            corner_radius=20,
            command=self.buscar_usuarios
        ).grid(row=0, column=1, padx=(0, 10), pady=5)

        ctk.CTkButton(
            search_frame,
            text="Nuevo Usuario",
            image=self.icon_add,
            corner_radius=20,
            command=self.crear_usuario
        ).grid(row=0, column=2, padx=(0, 10), pady=5)

        # Frame para las tarjetas de usuario
        self.card_frame = ctk.CTkScrollableFrame(self, fg_color="#F2F2F2", corner_radius=10)
        self.card_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        self.card_frame.grid_columnconfigure(0, weight=1)

        self.cargar_usuarios()

    def cargar_usuarios(self):
        # Limpiar tarjetas existentes
        for widget in self.card_frame.winfo_children():
            widget.destroy()

        usuarios = self.user_controller.listar()
        if not usuarios:
            ctk.CTkLabel(self.card_frame, text="No hay usuarios registrados.").pack(pady=20)
            return

        for user in usuarios:
            self.crear_tarjeta_usuario(self.card_frame, user)

    def crear_tarjeta_usuario(self, parent_frame, user):
        card = ctk.CTkFrame(parent_frame, fg_color="#FFFFFF", corner_radius=10, height=120)
        card.pack(fill="x", padx=10, pady=5)
        card.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(card, text=f"Usuario: {user.username}", font=("Arial", 14, "bold"), text_color="#06A051").grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        ctk.CTkLabel(card, text=f"Rol: {user.rol}", font=("Arial", 12), text_color="#555555").grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # Botones de acción en la tarjeta
        btn_frame = ctk.CTkFrame(card, fg_color="transparent")
        btn_frame.grid(row=0, column=2, rowspan=2, padx=10, pady=5, sticky="e")
        
        ctk.CTkButton(
            btn_frame,
            text="Editar",
            image=self.icon_edit,
            fg_color="#06A051",
            hover_color="#088D48",
            command=lambda u=user: self.editar_usuario(u)
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Eliminar",
            image=self.icon_delete,
            fg_color="#D12B1B",
            hover_color="#BB1E10",
            command=lambda u_id=user.id: self.eliminar_usuario(u_id)
        ).pack(side="left", padx=5)

    def buscar_usuarios(self):
        query = self.search_entry.get()
        # Aquí deberías tener una función en el controlador para buscar, similar a la de empleados
        # Por ahora, simplemente recargamos todo
        self.cargar_usuarios()

    def crear_usuario(self):
        self.pack_forget()
        CreateUser(self.master, volver_callback=self.volver_a_gestion).pack(fill="both", expand=True)

    def editar_usuario(self, user):
        self.pack_forget()
        EditUser(self.master, user, volver_callback=self.volver_a_gestion).pack(fill="both", expand=True)
        
    def eliminar_usuario(self, user_id):
        respuesta = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar este usuario?")
        if respuesta:
            exito, mensaje = self.user_controller.eliminar(user_id)
            if exito:
                messagebox.showinfo("Éxito", mensaje)
                self.cargar_usuarios() # Recargar la lista después de la eliminación
            else:
                messagebox.showerror("Error", mensaje)

    def volver_a_gestion(self):
        self.pack(fill="both", expand=True)
        self.cargar_usuarios() # Asegurarse de que los datos estén actualizados al volver

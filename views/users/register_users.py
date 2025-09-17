import customtkinter as ctk
from tkinter import messagebox
from controllers.user_controller import UserController
from PIL import Image
from utils.canvas import agregar_fondo_decorativo

class RegistrarUsuarios(ctk.CTkFrame):
    def __init__(self, parent,username,rol, volver_callback):
        super().__init__(parent)
        self.volver_callback = volver_callback
        self.username = username
        self.rol = rol
        self.user_controller = UserController()
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        agregar_fondo_decorativo(self)
        self.configure(fg_color="#F5F5F5")

        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))
        
        # ==== Tarjeta principal del formulario ====
        self.card = ctk.CTkFrame(self, fg_color="#D9D9D9", corner_radius=10)
        self.card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.45, relheight=0.6)
        
        # Widgets del formulario
        self.title_label = ctk.CTkLabel(self.card, text="Registro de Usuario", font=("Georgia", 24, "bold"))
        self.title_label.pack(pady=(20, 10))

        # Campos de entrada
        self.username_label = ctk.CTkLabel(self.card, text="Nombre de Usuario:", font=("Georgia", 14))
        self.username_label.pack(pady=(5, 0))
        self.username_entry = ctk.CTkEntry(self.card, placeholder_text="Nombre de usuario", width=300)
        self.username_entry.pack(pady=(0, 10))

        self.password_label = ctk.CTkLabel(self.card, text="Contraseña:", font=("Georgia", 14))
        self.password_label.pack(pady=(5, 0))
        self.password_entry = ctk.CTkEntry(self.card, placeholder_text="Contraseña", show="*", width=300)
        self.password_entry.pack(pady=(0, 10))
        
        self.rol_label = ctk.CTkLabel(self.card, text="Rol:", font=("Georgia", 14))
        self.rol_label.pack(pady=(5, 0))
        self.rol_combobox = ctk.CTkComboBox(self.card, values=["aprendiz", "administrador"], width=300)
        self.rol_combobox.pack(pady=(0, 20))
        
        # Botón de guardar
        self.save_button = ctk.CTkButton(self.card, text="Guardar", command=self._save_user, fg_color="#06A051", hover_color="#048B45", text_color="black", font=("Georgia", 16))
        self.save_button.pack(pady=10)
        
        self.btn_volver = ctk.CTkButton(
            self,image=self.icon_back,text="",corner_radius=0,hover_color="#F3EFEF", width=30,height=30,command=self.volver_al_panel,fg_color="#d2d2d2"
        )
        self.btn_volver.place(relx=0.98, rely=0.02, anchor="ne")

    def _save_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        rol = self.rol_combobox.get()
        
        if not username or not password or not rol:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            self.user_controller.crear(username, password, rol)
            messagebox.showinfo("Éxito", "Usuario creado exitosamente.")
            
            # Limpiar los campos después de un registro exitoso
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            self.rol_combobox.set("aprendiz") # Puedes resetear al valor por defecto
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    def volver_al_panel(self):
        if self.volver_callback:
            self.destroy()
            self.volver_callback()

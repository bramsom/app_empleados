import customtkinter as ctk
from tkinter import messagebox
from bd.users import crear_usuario

class CrearUsuario(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.title("Crear Usuario")
        self.geometry("400x400")

        ctk.CTkButton(self, text="Volver al menú principal", command=lambda: self.volver_menu(username, rol)).pack(pady=20)

        # Título
        self.label_title = ctk.CTkLabel(self, text="Crear nuevo usuario", font=("Arial", 20))
        self.label_title.pack(pady=20)

        # Campo de username
        self.entry_username = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.entry_username.pack(pady=10)

        # Campo de contraseña
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_password.pack(pady=10)

        # Campo de rol
        self.option_rol = ctk.CTkOptionMenu(self, values=["aprendiz", "administrador"])
        self.option_rol.pack(pady=10)
        self.option_rol.set("aprendiz")  # Valor por defecto

        # Botón de crear
        self.btn_crear = ctk.CTkButton(self, text="Crear usuario", command=self.crear)
        self.btn_crear.pack(pady=20)

    def crear(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        rol = self.option_rol.get()

        if not username or not password:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        try:
            crear_usuario(username, password, rol)
            messagebox.showinfo("Éxito", "Usuario creado correctamente.")
            self.entry_username.delete(0, 'end')
            self.entry_password.delete(0, 'end')
            self.option_rol.set("aprendiz")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear el usuario.\n{str(e)}")

    def volver_menu(self, username, rol):
        self.destroy()  # Cierra esta ventana
        from views.main_menu import MainMenu
        main_menu = MainMenu(username, rol)
        main_menu.mainloop()
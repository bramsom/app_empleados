import customtkinter as ctk
from tkinter import messagebox
from bd.users import verificar_credenciales
from views.main_menu import MainMenu

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login de Usuarios")
        self.geometry("400x300")

        ctk.set_appearance_mode("dark")  # Opcional: "light", "dark", "system"
        ctk.set_default_color_theme("blue")  # También: "green", "dark-blue"

        # Título
        self.label_title = ctk.CTkLabel(self, text="Inicio de sesión", font=("Arial", 20))
        self.label_title.pack(pady=20)

        # Entrada de usuario
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.username_entry.pack(pady=10)

        # Entrada de contraseña
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.password_entry.pack(pady=10)

        # Botón de login
        self.login_button = ctk.CTkButton(self, text="Iniciar sesión", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        exito, rol = verificar_credenciales(username, password)
        if exito:
            messagebox.showinfo("Bienvenido", f"Has iniciado sesión como {rol}.")
            # Retardo breve para evitar conflicto con animación
            self.after(100, lambda: self.abrir_menu_principal(username, rol))
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def abrir_menu_principal(self, username, rol):
        self.destroy()
        main_menu = MainMenu(username, rol)
        main_menu.mainloop()

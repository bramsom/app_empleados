import customtkinter as ctk
from tkinter import messagebox
from controllers.user_controller import UserController

class CrudUsuarios(ctk.CTkFrame):
    def __init__(self,parent, username, rol):
        super().__init__(parent)
        self.user_ctrl = UserController()
        self.username = username
        self.rol = rol
        self.configure(fg_color="transparent")


        ctk.CTkButton(self, text="Volver al menú principal", command=lambda: self.volver_menu(username, rol)).pack(pady=20)

        # Entradas
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.username_entry.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.password_entry.pack(pady=10)
        self.rol_option = ctk.CTkOptionMenu(self, values=["aprendiz", "administrador"])
        self.rol_option.set("aprendiz")
        self.rol_option.pack(pady=10)

        # Botón crear
        ctk.CTkButton(self, text="Crear", command=self.crear).pack(pady=10)
        ctk.CTkButton(self, text="Actualizar contraseña", command=self.cambiar_contraseña).pack(pady=5)

        # Lista
        self.lista = ctk.CTkOptionMenu(self, values=[], command=self.seleccionar)
        self.lista.pack(pady=10)
        self.cargar_usuarios()

    def cargar_usuarios(self):
        self.usuarios = {f"{u[1]} ({u[2]})": u[0] for u in self.user_ctrl.listar()}
        self.lista.configure(values=list(self.usuarios.keys()))

    def seleccionar(self, clave):
        self.seleccionado = self.usuarios.get(clave)

    def crear(self):
        try:
            self.user_ctrl.crear(self.username_entry.get(), self.password_entry.get(), self.rol_option.get())
            messagebox.showinfo("Éxito", "Usuario creado")
            self.cargar_usuarios()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cambiar_contraseña(self):
        if not hasattr(self, 'seleccionado'):
            messagebox.showwarning("Selecciona", "Selecciona un usuario")
            return
        nueva = self.password_entry.get()
        self.user_ctrl.cambiar_password(self.seleccionado, nueva)
        messagebox.showinfo("Éxito", "Contraseña actualizada")

    #def volver_menu(self, username, rol):
        #self.destroy()  # Cierra esta ventana
        #from views.main_menu import MainMenu
        #main_menu = MainMenu(username, rol)
        #main_menu.mainloop()
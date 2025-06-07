import customtkinter as ctk
from tkinter import messagebox
from bd.users import obtener_usuarios, actualizar_usuario, eliminar_usuario

class GestionUsuarios(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestión de Usuarios")
        self.geometry("500x400")

        self.label = ctk.CTkLabel(self, text="Selecciona un usuario")
        self.label.pack(pady=10)

        self.lista_usuarios = ctk.CTkOptionMenu(self, values=[], command=self.seleccionar_usuario)
        self.lista_usuarios.pack(pady=10)

        self.entry_username = ctk.CTkEntry(self, placeholder_text="Nuevo usuario")
        self.entry_username.pack(pady=10)

        self.option_rol = ctk.CTkOptionMenu(self, values=["aprendiz", "administrador"])
        self.option_rol.pack(pady=10)

        self.btn_actualizar = ctk.CTkButton(self, text="Actualizar", command=self.actualizar)
        self.btn_actualizar.pack(pady=10)

        self.btn_eliminar = ctk.CTkButton(self, text="Eliminar", fg_color="red", command=self.eliminar)
        self.btn_eliminar.pack(pady=10)

        self.usuario_actual = None
        self.cargar_usuarios()

    def cargar_usuarios(self):
        self.usuarios = obtener_usuarios()
        nombres = [f"{u[1]} (id:{u[0]})" for u in self.usuarios]
        self.lista_usuarios.configure(values=nombres)
        if nombres:
            self.lista_usuarios.set(nombres[0])
            self.seleccionar_usuario(nombres[0])

    def seleccionar_usuario(self, seleccionado):
        for u in self.usuarios:
            if f"{u[1]} (id:{u[0]})" == seleccionado:
                self.usuario_actual = u
                self.entry_username.delete(0, 'end')
                self.entry_username.insert(0, u[1])
                self.option_rol.set(u[2])
                break

    def actualizar(self):
        if not self.usuario_actual:
            messagebox.showerror("Error", "No hay usuario seleccionado")
            return
        nuevo_usuario = self.entry_username.get()
        nuevo_rol = self.option_rol.get()
        actualizar_usuario(self.usuario_actual[0], nuevo_usuario, nuevo_rol)
        messagebox.showinfo("Éxito", "Usuario actualizado")
        self.cargar_usuarios()

    def eliminar(self):
        if not self.usuario_actual:
            messagebox.showerror("Error", "No hay usuario seleccionado")
            return
        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este usuario?")
        if confirm:
            eliminar_usuario(self.usuario_actual[0])
            messagebox.showinfo("Éxito", "Usuario eliminado")
            self.cargar_usuarios()

# # Para pruebas individuales
# if __name__ == "__main__":
#     app = GestionUsuarios()
#     app.mainloop()

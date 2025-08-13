import customtkinter as ctk
from views.users.crud_users import CrudUsuarios
from views.employees.crud_employees import CrudEmpleados
from views.contracts.crud_contracts import CrudContratos
from views.afilliations.crud_afiliations import CrudAfiliaciones

class MainMenu(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.username = username
        self.rol = rol
        self.title("Menú Principal")
        self.geometry("400x400")

        ctk.CTkLabel(self, text=f"Bienvenido: {username} ({rol})", font=("Arial", 16)).pack(pady=20)

        ctk.CTkButton(self, text="Gestión de Usuarios", command=self.abrir_crud_usuarios).pack(pady=10)
        ctk.CTkButton(self, text="Gestión de Empleados", command=self.abrir_crud_empleados).pack(pady=10)
        ctk.CTkButton(self, text="Gestión de Contratos", command=self.abrir_crud_contratos).pack(pady=10)
        ctk.CTkButton(self, text="Gestión de Afiliaciones", command=self.abrir_crud_afiliaciones).pack(pady=10)
        ctk.CTkButton(self, text="Salir", command=self.destroy).pack(pady=20)

    def abrir_crud_usuarios(self):
        self.destroy()
        from views.users.crud_users import CrudUsuarios
        app= CrudUsuarios(self.username, self.rol)
        app.mainloop()

    def abrir_crud_empleados(self):
        self.destroy()
        from views.employees.crud_employees import CrudEmpleados
        app = CrudEmpleados(self.username, self.rol)
        app.mainloop()

    def abrir_crud_contratos(self):
        self.destroy()
        from views.contracts.crud_contracts import CrudContratos
        app = CrudContratos(self.username, self.rol)
        app.mainloop()

    def abrir_crud_afiliaciones(self):
        self.destroy()
        from views.afilliations.crud_afiliations import CrudAfiliaciones
        app = CrudAfiliaciones(self.username, self.rol)
        app.mainloop()

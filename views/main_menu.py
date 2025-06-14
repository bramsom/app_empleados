import customtkinter as ctk
from views.create_user import CrearUsuario
from views.crud_employees import CrudEmpleados
from views.crud_contracts import CrudContratos
from views.crud_afiliations import CrudAfiliaciones

class MainMenu(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.title("Menú Principal")
        self.geometry("400x400")

        ctk.CTkLabel(self, text=f"Bienvenido: {username} ({rol})", font=("Arial", 16)).pack(pady=20)

        ctk.CTkButton(self, text="Gestión de Usuarios", command=self.abrir_crud_usuarios).pack(pady=10)
        ctk.CTkButton(self, text="Gestión de Empleados", command=self.abrir_crud_empleados).pack(pady=10)
        ctk.CTkButton(self, text="Gestión de Contratos", command=self.abrir_crud_contratos).pack(pady=10)
        ctk.CTkButton(self, text="Gestión de Afiliaciones", command=self.abrir_crud_afiliaciones).pack(pady=10)
        ctk.CTkButton(self, text="Salir", command=self.destroy).pack(pady=20)

    def abrir_crud_usuarios(self):
        self.withdraw()
        ventana = CrearUsuario()
        ventana.mainloop()
        self.deiconify()

    def abrir_crud_empleados(self):
        self.withdraw()
        ventana = CrudEmpleados()
        ventana.mainloop()
        self.deiconify()

    def abrir_crud_contratos(self):
        self.withdraw()
        ventana = CrudContratos()
        ventana.mainloop()
        self.deiconify()

    def abrir_crud_afiliaciones(self):
        self.withdraw()
        ventana = CrudAfiliaciones()
        ventana.mainloop()
        self.deiconify()

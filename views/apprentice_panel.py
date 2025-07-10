import customtkinter as ctk
from tkinter import Canvas
from PIL import Image
import math
from tkinter import messagebox

class Dashboard(ctk.CTk):
    def __init__(self, username, rol):
        super().__init__()
        self.username = username
        self.rol = rol
        
        # Configuración de la ventana
        self.geometry("1200x800")
        self.title("Dashboard - Sistema de Gestión")
        
        # Crear layout principal
        self.create_layout()
        
    def create_layout(self):
        # Sidebar para navegación
        self.sidebar = ctk.CTkFrame(self, width=200)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        # Área de contenido principal
        self.content_area = ctk.CTkFrame(self,fg_color="#F5F5F5")
        self.content_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Crear menú de navegación
        self.create_menu()
        
        # Mostrar vista por defecto
        self.show_default_view()
        
    def create_menu(self):
        # Título del menú
        menu_title = ctk.CTkLabel(self.sidebar, text="MENÚ", 
                                 font=("Arial", 16, "bold"))
        menu_title.pack(pady=(20, 30))
        
        # Botón para empleados
        empleados_btn = ctk.CTkButton(self.sidebar, text="Empleados",
                                     command=self.show_empleados_view,
                                     width=160, height=40)
        empleados_btn.pack(pady=10, padx=20, fill="x")
        
        # Otros botones del menú
        inventario_btn = ctk.CTkButton(self.sidebar, text="Inventario",
                                      command=self.show_inventario_view,
                                      width=160, height=40)
        inventario_btn.pack(pady=10, padx=20, fill="x")
        
        ventas_btn = ctk.CTkButton(self.sidebar, text="Ventas",
                                  command=self.show_ventas_view,
                                  width=160, height=40)
        ventas_btn.pack(pady=10, padx=20, fill="x")
        
        reportes_btn = ctk.CTkButton(self.sidebar, text="Reportes",
                                    command=self.show_reportes_view,
                                    width=160, height=40)
        reportes_btn.pack(pady=10, padx=20, fill="x")
        
        # Botón de cerrar sesión
        cerrar_btn = ctk.CTkButton(self.sidebar, text="Cerrar Sesión",
                                  command=self.cerrar_sesion,
                                  width=160, height=40,
                                  fg_color="red", hover_color="darkred")
        cerrar_btn.pack(side="bottom", pady=20, padx=20, fill="x")
        
    def clear_content_area(self):
        """Limpia el área de contenido"""
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
    def show_empleados_view(self):
        """Muestra la vista de gestión de empleados"""
        self.clear_content_area()
        
        # Importar la clase CrudEmpleados desde su propio archivo
        from views.crud_employees import CrudEmpleados
        
        # Crear y mostrar el CRUD de empleados
        crud_empleados = CrudEmpleados(self.content_area, self.username, self.rol)
        crud_empleados.pack(fill="both", expand=True, padx=10, pady=10)
        
    def show_inventario_view(self):
        """Muestra la vista de inventario"""
        self.clear_content_area()
        
        # Cuando tengas la vista de inventario, importarla así:
        # from views.crud_inventario import CrudInventario
        # crud_inventario = CrudInventario(self.content_area, self.username, self.rol)
        # crud_inventario.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Por ahora, placeholder
        placeholder = ctk.CTkLabel(self.content_area, text="Gestión de Inventario",
                                  font=("Arial", 24, "bold"))
        placeholder.pack(expand=True)
        
    def show_ventas_view(self):
        """Muestra la vista de ventas"""
        self.clear_content_area()
        
        # Placeholder para ventas
        placeholder = ctk.CTkLabel(self.content_area, text="Gestión de Ventas",
                                  font=("Arial", 24, "bold"))
        placeholder.pack(expand=True)
        
    def show_reportes_view(self):
        """Muestra la vista de reportes"""
        self.clear_content_area()
        
        # Placeholder para reportes
        placeholder = ctk.CTkLabel(self.content_area, text="Reportes y Estadísticas",
                                  font=("Arial", 24, "bold"))
        placeholder.pack(expand=True)
        
    def show_default_view(self):
        """Muestra la vista por defecto"""
        self.clear_content_area()
        
        # Crear un frame para centrar el contenido
        welcome_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        welcome_frame.pack(expand=True, fill="both")
        
        # Etiqueta de bienvenida
        welcome_label = ctk.CTkLabel(welcome_frame, 
                                    text=f"Bienvenido, {self.username}",
                                    font=("Arial", 28, "bold"))
        welcome_label.pack(expand=True)
        
        # Información adicional
        info_label = ctk.CTkLabel(welcome_frame, 
                                 text=f"Rol: {self.rol}",
                                 font=("Arial", 16))
        info_label.pack(pady=(0, 10))
        
        # Instrucciones
        instrucciones = ctk.CTkLabel(welcome_frame, 
                                   text="Selecciona una opción del menú lateral para comenzar",
                                   font=("Arial", 14),
                                   text_color="gray")
        instrucciones.pack(pady=10)
        
    def cerrar_sesion(self):
        """Cierra la sesión actual"""
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas cerrar sesión?"):
            self.destroy()
            # Aquí puedes agregar lógica para volver a la pantalla de login
            # from views.login import LoginView
            # LoginView().mainloop()


# Función para inicializar el dashboard
def inicializar_dashboard(username, rol):
    """Inicializa el dashboard con el usuario y rol especificados"""
    dashboard = Dashboard(username, rol)
    dashboard.mainloop()


# Ejemplo de uso
if __name__ == "__main__":
    # Reemplaza con los valores reales del usuario logueado
    inicializar_dashboard("usuario_ejemplo", "administrador")
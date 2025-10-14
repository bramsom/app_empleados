import customtkinter as ctk
import importlib
from tkinter import messagebox
from controllers.report_controller import obtener_datos_para_excel, obtener_datos_para_pdf
from views.reports.type_reports import ExportarTipoReporte


class ViewManager:
    def __init__(self, content_area, username, rol, volver_callback):
        self.content_area = content_area
        self.username = username
        self.rol = rol
        self.volver_callback = volver_callback
        
        # Este diccionario mapea las claves de vista a sus módulos y clases correspondientes
        self.views = {
            "empleados_registrar": ("views.employees.register_employees", "RegistrarEmpleados"),
            "empleados_buscar": ("views.employees.search_employees", "BuscarEmpleados"),
            "contratos_registrar": ("views.contracts.register_contracts", "RegistrarContrato"),
            "contratos_buscar": ("views.contracts.search_contracts", "BuscarContratos"),
            "afiliaciones_registrar": ("views.afilliations.register_affiliations", "RegistrarAfiliacion"),
            "afiliaciones_buscar": ("views.afilliations.search_affiliations", "BuscarAfiliaciones"),
            "Reportes": ("views.reports.type_reports", "ExportarTipoReporte"),
            "usuarios_registrar": ("views.users.register_users", "FormularioRegistroEdicion"),
            "usuarios_buscar": ("views.users.search_users", "BuscarUsuarios")
        }

    def show_view(self, view_key, extra_args=None):
        """Loads and displays a view by its key."""
        if view_key not in self.views:
            messagebox.showerror("Error", f"View '{view_key}' not found.")
            return
        
        if view_key == "Reportes":
            self._show_exportar()
            return

        self.clear_content_area()

        module_name, class_name = self.views[view_key]
        
        try:
            module = importlib.import_module(module_name)
            view_class = getattr(module, class_name)
            
            # Pasa todos los argumentos necesarios al constructor de la vista
            view_instance = view_class(
                parent=self.content_area,
                username=self.username,
                rol=self.rol,
                volver_callback=self.volver_callback,
                **extra_args if extra_args else {}
            )
            view_instance.pack(fill="both", expand=True)

        except (ImportError, AttributeError, TypeError) as e:
            messagebox.showerror("Error", f"Could not load view '{view_key}': {e}")
    
    def create_view_placeholder(self, title):
        """Creates a placeholder for a view."""
        self.clear_content_area()
        placeholder = ctk.CTkLabel(self.content_area, text=title, font=("Arial", 24, "bold"))
        placeholder.pack(expand=True)
    
    def clear_content_area(self):
        """Clears all widgets from the content area."""
        for widget in self.content_area.winfo_children():
            widget.destroy()
            
    def _show_exportar(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
        ExportarTipoReporte(
            parent=self.content_area,
            username=self.username,
            rol=self.rol,
            obtener_datos_excel_callback=obtener_datos_para_excel,  # Para Excel
            obtener_datos_pdf_callback=obtener_datos_para_pdf,      # Para PDF
            volver_callback=self.volver_callback
        ).pack(fill="both", expand=True)
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image

class ModalSeleccionExcel(ctk.CTkToplevel):
    """
    Ventana modal que permite al usuario seleccionar qué tablas desea exportar a Excel.
    """
    def __init__(self, parent, exportar_callback):
        # Configuración de la ventana Toplevel
        super().__init__(parent)
        self.title("Selección de Datos para Exportar")
        self.geometry("450x350")
        self.transient(parent)  # Mantener el modal encima de la ventana principal
        self.grab_set()         # Bloquea la interacción con la ventana principal
        
        self.exportar_callback = exportar_callback
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.configure(fg_color="#F3EFEF")
        self._init_ui()
        
        # Centrar la ventana en la pantalla (opcional)
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
        self.resizable(False, False)

    def _init_ui(self):
        
        # Título
        ctk.CTkLabel(self, text="¿Qué datos desea incluir en el Excel?", font=("Georgia", 18, "bold"),
                     text_color="#333333").grid(
            row=0, column=0, padx=30, pady=(25, 15), sticky="ew"
        )
        
        # Contenedor de Checkboxes
        self.checkbox_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.checkbox_frame.grid(row=1, column=0, padx=30, pady=10, sticky="ew")
        self.checkbox_frame.columnconfigure(0, weight=1)

        # Variables de control para las selecciones
        self.empleados_var = ctk.StringVar(value="on") # Por defecto, marcamos Empleados
        self.contratos_var = ctk.StringVar(value="on") # Por defecto, marcamos Contratos
        self.afiliaciones_var = ctk.StringVar(value="on") # Por defecto, marcamos Afiliaciones
        
        # Checkbox Empleados
        ctk.CTkCheckBox(self.checkbox_frame, text="Tabla de Empleados", font=("Arial", 14), 
                        variable=self.empleados_var, onvalue="on", offvalue="off").grid(
                            row=0, column=0, sticky="w", pady=5
        )
        
        # Checkbox Contratos
        ctk.CTkCheckBox(self.checkbox_frame, text="Tabla de Contratos", font=("Arial", 14), 
                        variable=self.contratos_var, onvalue="on", offvalue="off").grid(
                            row=1, column=0, sticky="w", pady=5
        )

        # Checkbox Afiliaciones
        ctk.CTkCheckBox(self.checkbox_frame, text="Tabla de Afiliaciones", font=("Arial", 14), 
                        variable=self.afiliaciones_var, onvalue="on", offvalue="off").grid(
                            row=2, column=0, sticky="w", pady=5
        )
        
        # Botón Exportar
        self.export_button = ctk.CTkButton(self, text="Confirmar y Exportar", height=35, font=("Georgia", 15, "bold"), 
                                            command=self._iniciar_exportacion, fg_color="#06A051", hover_color="#048B45")
        self.export_button.grid(row=2, column=0, padx=30, pady=(20, 10), sticky="ew")
        
        # Botón Cancelar
        self.cancel_button = ctk.CTkButton(self, text="Cancelar", height=35, font=("Georgia", 15), 
                                            command=self.destroy, fg_color="#D9D9D9", text_color="#333333", hover_color="#C0C0C0")
        self.cancel_button.grid(row=3, column=0, padx=30, pady=(0, 20), sticky="ew")


    def _iniciar_exportacion(self):
        """Recoge las selecciones y llama al callback de exportación."""
        
        selecciones = {
            "empleados": self.empleados_var.get() == "on",
            "contratos": self.contratos_var.get() == "on",
            "afiliaciones": self.afiliaciones_var.get() == "on",
        }
        
        tablas_a_exportar = [nombre for nombre, seleccionado in selecciones.items() if seleccionado]
        
        if not tablas_a_exportar:
            messagebox.showwarning("Advertencia", "Debe seleccionar al menos una tabla para exportar.")
            return

        # Cierra el modal
        self.destroy()
        
        # Llama a la función de exportación del controlador
        try:
            self.exportar_callback(tablas_a_exportar)
            messagebox.showinfo("Éxito", "Exportación a Excel finalizada correctamente.")
        except Exception as e:
            messagebox.showerror("Error de Exportación", f"Ocurrió un error al exportar: {e}")

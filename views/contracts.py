import customtkinter as ctk
from tkinter import ttk

class ContractManager:
    def __init__(self, root):
        self.root = root
        
        # Frame principal para el contenido (sobre el fondo)
        self.main_content_frame = ctk.CTkFrame(
            root, 
            fg_color="white",
            corner_radius=10,
            width=800,
            height=500
        )
        self.main_content_frame.place(x=50, y=100)  # Ajusta según tu layout
        
        # Frame para contratos (inicialmente oculto)
        self.contracts_frame = None
        
    def show_contracts_view(self):
        # Limpiar contenido actual
        for widget in self.main_content_frame.winfo_children():
            widget.destroy()
            
        # Crear la vista de contratos
        self.create_contracts_table()
        
    def create_contracts_table(self):
        # Título
        title_label = ctk.CTkLabel(
            self.main_content_frame,
            text="CONTRATOS",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame para la tabla
        table_frame = ctk.CTkFrame(self.main_content_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear Treeview para la tabla
        columns = ('nombre', 'fecha_inicio', 'fecha_fin', 'tipo', 'modalidad', 
                  'transporte', 'valor', 'horas', 'estado', 'persona')
        
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar encabezados
        headers = {
            'nombre': 'Nombre o razón social',
            'fecha_inicio': 'Fecha inicio',
            'fecha_fin': 'Fecha fin',
            'tipo': 'Tipo de contrato',
            'modalidad': 'Modalidad',
            'transporte': 'Transporte',
            'valor': 'Valor hora',
            'horas': 'Horas',
            'estado': 'Estado',
            'persona': 'Persona que lo contrató'
        }
        
        for col in columns:
            tree.heading(col, text=headers[col])
            tree.column(col, width=100)
        
        # Datos de ejemplo
        contracts_data = [
            ('Huyen mental violin anterior', '03/04/2025', '03/10/2025', 'Contrato de aprendizaje', '$100000.00', '30', 'Activo', 'Edgar Alfonso Paez Flor'),
            ('Huyen mental violin anterior', '03/04/2025', '03/10/2025', 'Contrato de aprendizaje', '$100000.00', '30', 'Activo', 'Edgar Alfonso Paez Flor'),
            # ... más datos
        ]
        
        for contract in contracts_data:
            tree.insert('', 'end', values=contract)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botones de acción
        button_frame = ctk.CTkFrame(self.main_content_frame)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        edit_btn = ctk.CTkButton(button_frame, text="Editar", width=100)
        edit_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(button_frame, text="Eliminar", width=100)
        delete_btn.pack(side="left", padx=5)
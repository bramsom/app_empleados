import customtkinter as ctk
from tkinter import Canvas
from tkinter import messagebox
from controllers import employee_controller
from models.employee import Empleado

class CrudEmpleados(ctk.CTkFrame):
    def __init__(self, parent, username, rol):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.controller = employee_controller

        # Configuración del contenedor principal
        self.configure(fg_color="#F5F5F5")

        canvas = Canvas(self, bg="#F5F5F5", highlightthickness=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        

        # Polígonos decorativos
        canvas.create_polygon(860, 0, 990, 0, 1320, 330, 1255, 395, fill="#D2D2D2", outline="")
        canvas.create_polygon(1079, 122, 1140, 60, 1360, 280, 1360, 402, fill="#888888", outline="")
        canvas.create_polygon(1240, 0, 1360, 0, 1360, 120, 1360, 120, fill="#D2D2D2", outline="")
        canvas.create_polygon(1060, 0, 1210, 0, 1340, 130, 1265, 205, fill="#D12B1B", outline="")
        canvas.create_polygon(930, 0, 935, 0, 1195, 259, 1190, 260, fill="#FCFCFC", outline="")
        canvas.create_polygon(1130, 0, 1135, 0, 1260, 125, 1260, 130, fill="#FCFCFC", outline="")
        canvas.create_polygon(355, 640, 505, 640, 105, 241, 30, 315, fill="#D2D2D2", outline="")
        canvas.create_polygon(0, 240, 0, 370, 150, 520, 215, 455, fill="#888888", outline="")
        canvas.create_polygon(300, 640, 160, 640, 10, 490, 81, 420, fill="#D12B1B", outline="")
        canvas.create_polygon(225, 640, 230, 640, 70, 480, 68, 483, fill="#FCFCFC", outline="")
        canvas.create_polygon(425, 640, 430, 640, 180, 390, 178, 395, fill="#FCFCFC", outline="")

        # Tarjeta principal encima del fondo
        self.card = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        self.card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)
        self.card.lift()
        
        # Crear el layout principal
        self.create_layout()
        
    def create_layout(self):
        # Título
        title_label = ctk.CTkLabel(self, text="Gestión de Empleados", 
                                  font=("Georgia", 24, "bold"))
        title_label.pack(pady=(0, 20))

        # Frame principal que contendrá todo
        main_frame = ctk.CTkFrame(self.card, fg_color="#F5F5F5")
        main_frame.pack(fill="both", expand=True, padx=60, pady=0)

        # Frame para la lista de empleados (parte superior)
        list_frame = ctk.CTkFrame(main_frame,fg_color="#F5F5F5")
        list_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(list_frame, text="Seleccionar Empleado:", 
                    font=("Georgia", 14, "bold")).pack(pady=5)
        
        self.lista = ctk.CTkOptionMenu(list_frame, values=[], 
                                      command=self.cargar_empleado,
                                      width=400)
        self.lista.pack(pady=5)

        # Frame scrollable para los campos de entrada
        self.scroll_frame = ctk.CTkScrollableFrame(main_frame, width=580, height=400, fg_color="#F5F5F5")
        self.scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Crear campos de entrada
        self.create_input_fields()
        
        # Crear botones de acción
        self.create_action_buttons()
        
        # Inicializar datos
        self.selected_id = None
        self.cargar_lista()

    def create_input_fields(self):
        """Crea los campos de entrada para los datos del empleado"""
        campos = [
            ("nombre", "Nombre"),
            ("apellido", "Apellido"),
            ("tipo_doc", "Tipo de Documento"),
            ("n_doc", "N° de Documento"),
            ("expedicion", "Lugar de Expedición"),
            ("nacimiento", "Fecha de Nacimiento"),
            ("telefono", "Teléfono"),
            ("direccion", "Dirección"),
            ("rut", "RUT"),
            ("email", "Email"),
            ("cargo", "Cargo")
        ]
        
        self.entries = {}
        for key, label in campos:
            # Frame para cada campo
            field_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#F5F5F5")
            field_frame.pack(fill="x", pady=5)
            
            # Etiqueta
            label_widget = ctk.CTkLabel(field_frame, text=label, 
                                       font=("Georgia", 12, "bold"),
                                       width=150)
            label_widget.pack(side="left", padx=(0, 10))
            
            # Campo de entrada
            entry = ctk.CTkEntry(field_frame, width=400)
            entry.pack(side="left", fill="x", expand=True)
            
            self.entries[key] = entry

    def create_action_buttons(self):
        """Crea los botones de acción"""
        button_frame = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=20)
        
        # Primera fila de botones
        row1 = ctk.CTkFrame(button_frame, fg_color="transparent")
        row1.pack(fill="x", pady=5)
        
        guardar_btn = ctk.CTkButton(row1, text="Guardar", 
                                   command=self.guardar,
                                   width=140, height=35,
                                   fg_color="green", hover_color="darkgreen")
        guardar_btn.pack(side="left", padx=5)
        
        actualizar_btn = ctk.CTkButton(row1, text="Actualizar", 
                                      command=self.actualizar,
                                      width=140, height=35,
                                      fg_color="blue", hover_color="darkblue")
        actualizar_btn.pack(side="left", padx=5)
        
        # Segunda fila de botones
        row2 = ctk.CTkFrame(button_frame, fg_color="transparent")
        row2.pack(fill="x", pady=5)
        
        eliminar_btn = ctk.CTkButton(row2, text="Eliminar", 
                                    command=self.eliminar,
                                    width=140, height=35,
                                    fg_color="red", hover_color="darkred")
        eliminar_btn.pack(side="left", padx=5)
        
        limpiar_btn = ctk.CTkButton(row2, text="Limpiar", 
                                   command=self.limpiar,
                                   width=140, height=35,
                                   fg_color="gray", hover_color="darkgray")
        limpiar_btn.pack(side="left", padx=5)

    def cargar_lista(self):
        """Carga la lista de empleados en el dropdown"""
        try:
            empleados = self.controller.listar_empleados()
            self.empleados = {f"{e.name} {e.last_name} ({e.document_number})": e.id for e in empleados}
            if self.empleados:
                self.lista.configure(values=list(self.empleados.keys()))
                self.lista.set(list(self.empleados.keys())[0])
                self.cargar_empleado(list(self.empleados.keys())[0])
            else:
                self.lista.configure(values=["(sin empleados)"])
                self.lista.set("(sin empleados)")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar empleados: {str(e)}")

    def cargar_empleado(self, seleccion):
        """Carga los datos del empleado seleccionado"""
        if seleccion == "(sin empleados)":
            return
            
        emp_id = self.empleados.get(seleccion)
        if not emp_id:
            return
            
        try:
            datos = self.controller.consultar_empleado(emp_id)
            if not datos:
                return

            # Limpiar campos
            self.limpiar()
            
            # Cargar datos (ahora usando las claves sin puntos ni caracteres especiales)
            self.entries["nombre"].insert(0, datos.name or "")
            self.entries["apellido"].insert(0, datos.last_name or "")
            self.entries["tipo_doc"].insert(0, datos.document_type or "")
            self.entries["n_doc"].insert(0, datos.document_number or "")
            self.entries["expedicion"].insert(0, datos.document_issuance or "")
            self.entries["nacimiento"].insert(0, datos.birthdate or "")
            self.entries["telefono"].insert(0, datos.phone_number or "")
            self.entries["direccion"].insert(0, datos.residence_address or "")
            self.entries["rut"].insert(0, datos.RUT or "")
            self.entries["email"].insert(0, datos.email or "")
            self.entries["cargo"].insert(0, datos.position or "")

            self.selected_id = emp_id
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar empleado: {str(e)}")

    def guardar(self):
        """Guarda un nuevo empleado"""
        try:
            datos = Empleado(
                name=self.entries["nombre"].get(),
                last_name=self.entries["apellido"].get(),
                document_type=self.entries["tipo_doc"].get(),
                document_number=self.entries["n_doc"].get(),
                document_issuance=self.entries["expedicion"].get(),
                birthdate=self.entries["nacimiento"].get(),
                phone_number=self.entries["telefono"].get(),
                residence_address=self.entries["direccion"].get(),
                RUT=self.entries["rut"].get(),
                email=self.entries["email"].get(),
                position=self.entries["cargo"].get()
            )
            
            self.controller.registrar_empleado(datos)
            messagebox.showinfo("Éxito", "Empleado registrado correctamente.")
            self.limpiar()
            self.cargar_lista()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar empleado: {str(e)}")

    def actualizar(self):
        """Actualiza un empleado existente"""
        if not self.selected_id:
            messagebox.showwarning("Advertencia", "Selecciona un empleado primero.")
            return
            
        try:
            datos = Empleado(
                name=self.entries["nombre"].get(),
                last_name=self.entries["apellido"].get(),
                document_type=self.entries["tipo_doc"].get(),
                document_number=self.entries["n_doc"].get(),
                document_issuance=self.entries["expedicion"].get(),
                birthdate=self.entries["nacimiento"].get(),
                phone_number=self.entries["telefono"].get(),
                residence_address=self.entries["direccion"].get(),
                RUT=self.entries["rut"].get(),
                email=self.entries["email"].get(),
                position=self.entries["cargo"].get()
            )
            
            self.controller.actualizar_empleado(self.selected_id, datos)
            messagebox.showinfo("Éxito", "Empleado actualizado correctamente.")
            self.cargar_lista()
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar empleado: {str(e)}")

    def eliminar(self):
        """Elimina un empleado"""
        if not self.selected_id:
            messagebox.showwarning("Advertencia", "Selecciona un empleado primero.")
            return
            
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas eliminar este empleado?"):
            try:
                self.controller.eliminar_empleado(self.selected_id)
                messagebox.showinfo("Éxito", "Empleado eliminado correctamente.")
                self.limpiar()
                self.cargar_lista()
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar empleado: {str(e)}")

    def limpiar(self):
        """Limpia todos los campos de entrada"""
        for campo in self.entries.values():
            campo.delete(0, 'end')
        self.selected_id = None

    # Método eliminado ya que no se necesita para el dashboard
    # def volver_menu(self, username, rol):
    #     from views.main_menu import MainMenu
    #     MainMenu(username, rol).deiconify()
import customtkinter as ctk
from tkinter import messagebox
from controllers.user_controller import UserController
from PIL import Image
from utils.canvas import agregar_fondo_decorativo

class FormularioRegistroEdicion(ctk.CTkFrame):
    def __init__(self, parent, user_controller=None, usuario_a_editar=None,username=None, rol=None, volver_callback=None):
        super().__init__(parent)
        self.username = username
        self.rol = rol
        self.user_controller = user_controller
        self.usuario_a_editar = usuario_a_editar
        self.volver_callback = volver_callback
        
        self.icon_show_pass = ctk.CTkImage(Image.open("images/read.png"), size=(20, 20))
        self.icon_hide_pass = ctk.CTkImage(Image.open("images/hide.png"), size=(20, 20))
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        agregar_fondo_decorativo(self)
        self.configure(fg_color="#F5F5F5")
        
        self.icon_back = ctk.CTkImage(Image.open("images/arrow.png"), size=(30, 30))
        
        self.card = ctk.CTkFrame(self, fg_color="#F3EFEF", corner_radius=10)
        self.card.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.45, relheight=0.85)

        self.form_frame = ctk.CTkFrame(self.card, fg_color="transparent")
        self.form_frame.pack(fill="both", expand=True, padx=20, pady=20)
        self.form_frame.grid_columnconfigure(0, weight=1)
        
        if self.usuario_a_editar:
            title_text = "Editar Usuario"
        else:
            title_text = "Registrar Usuario"

        self.title_label = ctk.CTkLabel(self.form_frame, text=title_text, font=("Georgia", 24, "bold"))
        self.title_label.grid(row=0, column=0, pady=(0, 20), sticky="ew")

        ctk.CTkLabel(self.form_frame, text="Nombre de Usuario", font=("Georgia", 14,"bold"), anchor="w").grid(row=1, column=0, sticky="ew", pady=(5, 0))
        self.username_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Nombre de usuario", height=40, fg_color="#D9D9D9", border_width=0, corner_radius=5)
        self.username_entry.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        opciones_tipo_rol = ["", "ADMINISTRADOR", "APRENDIZ"]
        ctk.CTkLabel(self.form_frame, text="Rol", font=("Georgia", 14,"bold"), anchor="w").grid(row=3, column=0, sticky="ew", pady=(5, 0))
        self.role_combobox = ctk.CTkOptionMenu(self.form_frame, height=40, fg_color="#D9D9D9", dropdown_fg_color="#F3EFEF", button_color="#06A051", button_hover_color="#048B45", values=opciones_tipo_rol, font=("Georgia", 14), text_color="black")
        self.role_combobox.grid(row=4, column=0, sticky="ew", pady=(0, 10))

        self.password_label = ctk.CTkLabel(self.form_frame, text="Contraseña", font=("Georgia", 14,"bold"), anchor="w")
        self.password_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Digite su contraseña", height=40, show="*", fg_color="#D9D9D9", border_width=0, corner_radius=5)
        self.password_toggle_button = ctk.CTkButton(self.form_frame, image=self.icon_show_pass, text="", width=30, height=30, fg_color="transparent", hover_color="#D9D9D9", command=self._toggle_password_visibility)
        
        self.verify_password_label = ctk.CTkLabel(self.form_frame, text="Verificar Contraseña", font=("Georgia", 14,"bold"), anchor="w")
        self.verify_password_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Verifique su contraseña", height=40, show="*", fg_color="#D9D9D9", border_width=0, corner_radius=5)
        self.verify_password_toggle_button = ctk.CTkButton(self.form_frame, image=self.icon_show_pass, text="", width=30, height=30, fg_color="transparent", hover_color="#D9D9D9", command=self._toggle_verify_password_visibility)

        self.btn_volver = ctk.CTkButton(
            self, text="", image=self.icon_back, width=40,
            height=40, fg_color="#D3D3D3", hover_color="#F3EFEF",corner_radius=0 ,
            command=self._volver
        )
        self.btn_volver.place(relx=0.98, rely=0.02, anchor="ne")
        
        if self.usuario_a_editar:
            self.username_entry.insert(0, self.usuario_a_editar.username)
            self.role_combobox.set(self.usuario_a_editar.rol)
            
            self.change_password_checkbox = ctk.CTkCheckBox(self.form_frame, text="Cambiar Contraseña", font=("Georgia", 14), command=self._toggle_password_fields)
            self.change_password_checkbox.grid(row=5, column=0, sticky="ew", pady=(10, 5))
            
            self.password_label.grid_forget()
            self.password_entry.grid_forget()
            self.password_toggle_button.grid_forget()
            self.verify_password_label.grid_forget()
            self.verify_password_entry.grid_forget()
            self.verify_password_toggle_button.grid_forget()
        else:
            self.password_label.grid(row=5, column=0, sticky="ew", pady=(5, 0))
            self.password_entry.grid(row=6, column=0, sticky="ew", pady=(0, 5))
            self.password_toggle_button.grid(row=6, column=0, sticky="e", padx=(0, 5))
            
            self.verify_password_label.grid(row=7, column=0, sticky="ew", pady=(5, 0))
            self.verify_password_entry.grid(row=8, column=0, sticky="ew", pady=(0, 5))
            self.verify_password_toggle_button.grid(row=8, column=0, sticky="e", padx=(0, 5))

        self.botones_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.botones_frame.columnconfigure((0, 1), weight=1)
        
        if self.usuario_a_editar:
            self.save_button = ctk.CTkButton(self.botones_frame, text="Guardar Cambios", height=50, font=("Georgia", 14), command=self._save_user, fg_color="#06A051", hover_color="#048B45", text_color="black")
            self.save_button.grid(row=0, column=0, sticky="ew", padx=(10, 10))
            self.cancel_button = ctk.CTkButton(self.botones_frame, text="Cancelar", height=50, font=("Georgia", 14), command=self._volver, fg_color="#D12B1B", hover_color="#B81D0F", text_color="black")
            self.cancel_button.grid(row=0, column=1, sticky="ew", padx=(0, 10))
            self.botones_frame.grid(row=6, column=0, sticky="ew", pady=(20, 10))
        else:
            self.save_button = ctk.CTkButton(self.botones_frame, text="Registrar", height=50, font=("Georgia", 14), command=self._save_user, fg_color="#06A051", hover_color="#048B45", text_color="black")
            self.save_button.grid(row=0, column=0, sticky="ew", padx=(10, 10))
            self.cancel_button = ctk.CTkButton(self.botones_frame, text="Cancelar", height=50, font=("Georgia", 14), command=self._volver, fg_color="#D12B1B", hover_color="#B81D0F", text_color="black")
            self.cancel_button.grid(row=0, column=1, sticky="ew", padx=(0, 10))
            self.botones_frame.grid(row=9, column=0, sticky="ew", pady=(20, 10))
        
    def _toggle_password_visibility(self):
        current_show = self.password_entry.cget("show")
        if current_show == "*":
            self.password_entry.configure(show="")
            self.password_toggle_button.configure(image=self.icon_hide_pass)
        else:
            self.password_entry.configure(show="*")
            self.password_toggle_button.configure(image=self.icon_show_pass)
            
    def _toggle_verify_password_visibility(self):
        current_show = self.verify_password_entry.cget("show")
        if current_show == "*":
            self.verify_password_entry.configure(show="")
            self.verify_password_toggle_button.configure(image=self.icon_hide_pass)
        else:
            self.verify_password_entry.configure(show="*")
            self.verify_password_toggle_button.configure(image=self.icon_show_pass)

    def _toggle_password_fields(self):
        if self.change_password_checkbox.get():
            self.password_label.grid(row=6, column=0, sticky="ew", pady=(5, 0))
            self.password_entry.grid(row=7, column=0, sticky="ew", pady=(0, 5))
            self.password_toggle_button.grid(row=7, column=0, sticky="e", padx=(0, 5))
            
            self.verify_password_label.grid(row=8, column=0, sticky="ew", pady=(5, 0))
            self.verify_password_entry.grid(row=9, column=0, sticky="ew", pady=(0, 5))
            self.verify_password_toggle_button.grid(row=9, column=0, sticky="e", padx=(0, 5))
            
            self.botones_frame.grid(row=10, column=0, sticky="ew", pady=(20, 10))
        else:
            self.password_label.grid_forget()
            self.password_entry.grid_forget()
            self.password_toggle_button.grid_forget()
            self.verify_password_label.grid_forget()
            self.verify_password_entry.grid_forget()
            self.verify_password_toggle_button.grid_forget()
            self.botones_frame.grid(row=6, column=0, sticky="ew", pady=(20, 10))
            
    def _save_user(self):
        username = self.username_entry.get()
        rol = self.role_combobox.get()
        
        if not username or not rol:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not self.usuario_a_editar:
            password = self.password_entry.get()
            verify_password = self.verify_password_entry.get()

            if not password:
                messagebox.showerror("Error", "La contraseña es obligatoria para un nuevo usuario.")
                return

            if password != verify_password:
                messagebox.showerror("Error", "Las contraseñas no coinciden.")
                return

            try:
                self.user_controller.registrar(username, password, rol)
                messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
                if self.volver_callback:
                    self.volver_callback()
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar usuario: {e}")

        else:
            password_to_update = None
            if self.change_password_checkbox.get():
                password_to_update = self.password_entry.get()
                verify_password = self.verify_password_entry.get()
                
                if not password_to_update:
                    messagebox.showerror("Error", "La nueva contraseña es obligatoria para actualizar.")
                    return
                
                if password_to_update != verify_password:
                    messagebox.showerror("Error", "Las contraseñas no coinciden.")
                    return

            try:
                self.user_controller.modificar(
                    self.usuario_a_editar.id, 
                    username, 
                    password_to_update, 
                    rol
                )
                messagebox.showinfo("Éxito", "Usuario actualizado exitosamente.")
                if self.volver_callback:
                    self.volver_callback()
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar usuario: {e}")
            
    def _volver(self):
        if self.volver_callback:
            self.destroy()
            self.volver_callback()




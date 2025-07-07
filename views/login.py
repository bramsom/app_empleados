import customtkinter as ctk
from tkinter import Canvas
from PIL import Image
from tkinter import messagebox
from bd.users import verificar_credenciales
from views.main_menu import MainMenu  # <-- Ajusta este import según tu estructura

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.resizable(False, False)
        self.title("Inicio de sesión")

        # === Frame Izquierdo con decoraciones ===
        frame_izquierdo = ctk.CTkFrame(self, width=300, corner_radius=0)
        frame_izquierdo.pack(side="left", fill="y")

        canvas = Canvas(frame_izquierdo, width=300, height=500, bg="#FFEFEF", highlightthickness=0)
        canvas.pack()

        # Polígonos decorativos
        canvas.create_polygon(80, 0, 140, 0, 260, 120, 230, 150, fill="#D2D2D2", outline="")
        canvas.create_polygon(200, 80, 240, 40, 300, 100, 300, 180, fill="#888888", outline="")
        canvas.create_polygon(240, 0, 300, 0, 300, 60, 300, 60, fill="#D2D2D2", outline="")
        canvas.create_polygon(233, 0, 164, 0, 255, 92, 290, 57, fill="#D12B1B", outline="")
        canvas.create_polygon(200, 0, 201, 0, 260, 60, 260, 60, fill="#FCFCFC", outline="")
        canvas.create_polygon(109, 0, 109, 0, 169, 60, 170, 60, fill="#FCFCFC", outline="")
        canvas.create_polygon(220, 500, 280, 500, 80, 300, 50, 330, fill="#D2D2D2", outline="")
        canvas.create_polygon(0, 250, 0, 330, 90, 420, 130, 380, fill="#888888", outline="")
        canvas.create_polygon(190, 500, 110, 500, 20, 410, 60, 370, fill="#D12B1B", outline="")
        canvas.create_polygon(151, 500, 150, 500, 50, 400, 50, 400, fill="#FCFCFC", outline="")
        canvas.create_polygon(250, 500, 251, 500, 150, 400, 150, 400, fill="#FCFCFC", outline="")

        logo_img = ctk.CTkImage(Image.open("C:/Users/Usuario/Documents/proyectos python/app_empleados/images/logo.png"), size=(140, 150))
        logo_label = ctk.CTkLabel(frame_izquierdo, image=logo_img, text="", fg_color=frame_izquierdo.cget("fg_color"))
        logo_label.place(relx=0.55, rely=0.45, anchor="center")

        # === Frame Derecho (formulario) ===
        frame_derecho = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color="white")
        frame_derecho.pack(side="left", fill="both", expand=True)

        titulo = ctk.CTkLabel(frame_derecho, text="Bienvenido", font=("Georgia", 32))
        titulo.pack(pady=(40, 5))

        subtitulo = ctk.CTkLabel(frame_derecho, text="Inicia sesión para continuar", font=("Georgia", 16))
        subtitulo.pack(pady=(0, 30))

        label_usuario = ctk.CTkLabel(frame_derecho, text="Usuario", anchor="w", font=("Georgia", 20))
        label_usuario.pack(fill="x", padx=40)
        self.username_entry = ctk.CTkEntry(frame_derecho, width=220, height=40, corner_radius=20, fg_color="#CFCFCF", border_color="gray", border_width=1)
        self.username_entry.pack(pady=(5, 20), padx=40)

        label_contrasena = ctk.CTkLabel(frame_derecho, text="Contraseña", anchor="w", font=("Georgia", 20))
        label_contrasena.pack(fill="x", padx=40)
        self.password_entry = ctk.CTkEntry(frame_derecho, width=220, height=40, corner_radius=20, show="*", fg_color="#CFCFCF", border_color="gray", border_width=1)
        self.password_entry.pack(pady=(5, 30), padx=40)

        self.login_button = ctk.CTkButton(
            frame_derecho,
            text="Iniciar sesión",
            font=("Georgia", 18),
            width=182,
            height=60,
            corner_radius=10,
            fg_color="#019137",
            hover_color="#017a2e",
            cursor="hand2",
            command=self.login
        )
        self.login_button.pack(pady=(0, 20))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        exito, rol = verificar_credenciales(username, password)
        if exito:
            messagebox.showinfo("Bienvenido", f"Has iniciado sesión como {rol}.")
            self.after(100, lambda: self.abrir_menu_principal(username, rol))
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def abrir_menu_principal(self, username, rol):
        self.destroy()
        main_menu = MainMenu(username, rol)
        main_menu.mainloop()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()

# vistas/login.py
import tkinter as tk
from tkinter import messagebox

def iniciar_app():
    print("Ejecutando iniciar_app()")
    root = tk.Tk()
    root.title("Login")

    tk.Label(root, text="Usuario:").pack()
    entrada_usuario = tk.Entry(root)
    entrada_usuario.pack()

    tk.Label(root, text="Contraseña:").pack()
    entrada_contraseña = tk.Entry(root, show="*")
    entrada_contraseña.pack()

    def login():
        usuario = entrada_usuario.get()
        contrasena = entrada_contraseña.get()
        if usuario == "admin" and contrasena == "admin":
            messagebox.showinfo("Login", "Bienvenido, administrador")
        else:
            messagebox.showerror("Login", "Credenciales inválidas")

    tk.Button(root, text="Iniciar sesión", command=login).pack(pady=10)
    root.mainloop()

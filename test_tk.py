import tkinter as tk

root = tk.Tk()
root.title("Ventana de prueba")
root.geometry("300x100")
tk.Label(root, text="¿Ves esta ventana?").pack(pady=20)
root.mainloop()
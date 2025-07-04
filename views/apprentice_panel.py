import customtkinter as ctk
from tkinter import Canvas
from PIL import Image

ventana = ctk.CTk()
ventana.geometry("600x500")
ventana.resizable(False, False)

# Frame Izquierdo
frame_izquierdo = ctk.CTkFrame(ventana, width=300, corner_radius=0)
frame_izquierdo.pack(side="left", fill="y")

# Canvas para dibujar decoraciones
canvas = Canvas(frame_izquierdo, width=300, height=500, bg="#FFEFEF", highlightthickness=0)
canvas.pack()


canvas.create_polygon(80, 0, 140, 0, 260, 120, 230, 150, fill="#D2D2D2", outline="")# Dibujar bloques (líneas o rectángulos inclinados)
canvas.create_polygon(200, 80, 240, 40, 300, 100, 300, 180, fill="#888888", outline="")
canvas.create_polygon(240, 0, 300, 0, 300, 60, 300, 60, fill="#D2D2D2", outline="")
canvas.create_polygon(233, 0, 164, 0, 255, 92, 290, 57, fill="#D12B1B", outline="")
canvas.create_polygon(200, 0, 201, 0, 260, 60, 260, 60, fill="#FCFCFC", outline="")
canvas.create_polygon(109, 0, 109, 0, 169, 60, 170, 60, fill="#FCFCFC", outline="")


canvas.create_polygon(220, 500, 280, 500, 80, 300, 50, 330, fill="#D2D2D2", outline="")# Dibujar bloques (líneas o rectángulos inclinados)
canvas.create_polygon(0, 250, 0, 330, 90, 420, 130, 380, fill="#888888", outline="")
canvas.create_polygon(190, 500, 110, 500, 20, 410, 60, 370, fill="#D12B1B", outline="")
canvas.create_polygon(151, 500, 150, 500, 50, 400, 50, 400, fill="#FCFCFC", outline="")
canvas.create_polygon(250,500, 251,500, 150, 400, 150, 400, fill="#FCFCFC", outline="")


# Logo encima
logo_img = ctk.CTkImage(Image.open("C:/Users/Usuario/Documents/proyectos python/app_empleados/images/logo.png"), size=(140, 150))
logo_label = ctk.CTkLabel(frame_izquierdo, image=logo_img, text="")
logo_label.place(relx=0.55, rely=0.45, anchor="center")

ventana.mainloop()



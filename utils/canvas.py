from tkinter import Canvas

def agregar_fondo_decorativo(parent, bg_color="#F5F5F5"):
    canvas = Canvas(parent, bg=bg_color, highlightthickness=0)
    canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Polígonos decorativos (los mismos que usabas)
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

    return canvas
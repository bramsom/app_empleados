import customtkinter as ctk

def crear_autocompletado(entry, lista_frame, callback_seleccion):
    empleados_dict = entry.empleados_dict

    def mostrar_sugerencias(event):
        texto = entry.get().lower()

        # Limpiar sugerencias anteriores
        for widget in lista_frame.winfo_children():
            widget.destroy()

        if not texto:
            lista_frame.lower()
            return

        # Buscar coincidencias
        coincidencias = [nombre for nombre in empleados_dict if texto in nombre.lower()]
        if not coincidencias:
            lista_frame.lower()
            return

        # Limitar a 6 sugerencias visibles
        max_visible = 6
        coincidencias = coincidencias[:max_visible]

        # Crear botones de sugerencia
        for nombre in coincidencias:
            btn = ctk.CTkButton(
                lista_frame, text=nombre, anchor="w",
                text_color="black", fg_color="white", hover_color="#E0E0E0",
                command=lambda n=nombre: callback_seleccion(n), height=30
            )
            btn.pack(fill="x")

        # Posicionar la lista justo debajo del campo
        entry.update_idletasks()
        x = entry.winfo_x()
        y = entry.winfo_y() + entry.winfo_height()
        width = entry.winfo_width()
        height = 30 * len(coincidencias)

        lista_frame.place(x=x, y=y)
        lista_frame.configure(width=width, height=height)
        lista_frame.lift()

    return mostrar_sugerencias






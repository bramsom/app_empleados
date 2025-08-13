import customtkinter as ctk
from tkcalendar import Calendar, DateEntry
from tkinter import Toplevel, messagebox

def crear_combobox(parent, values, width, callback=None):
    combobox = ctk.CTkComboBox(
        parent,
        values=values,
        width=width,
        state="readonly",
        command=callback if callback else lambda _: None
    )
    combobox.set(values[0])
    combobox.pack(side="left", padx=5)
    return combobox

def crear_filtro_fecha(parent, label_text, limpiar_callback, actualizar_callback):
    frame = ctk.CTkFrame(parent, fg_color="transparent")
    frame.pack(side="left", padx=5)
    ctk.CTkLabel(frame, text=label_text, font=("Arial", 11)).pack(side="left")
    date_entry = ctk.CTkEntry(frame, width=100)
    date_entry.pack(side="left", padx=2)
    ctk.CTkButton(frame, text="X", width=20, command=limpiar_callback).pack(side="left")
    date_entry.bind("<FocusOut>", lambda e: actualizar_callback())
    return date_entry, frame

def abrir_calendario_avanzado(self, fecha_inicio_cal, fecha_corte_cal, actualizar_lista):
    ventana_cal = Toplevel(self)
    ventana_cal.title("Seleccionar Rango de Fechas")
    ventana_cal.geometry("800x500")
    ventana_cal.resizable(False, False)
    ventana_cal.transient(self)
    ventana_cal.grab_set()
    ventana_cal.update_idletasks()
    x = (ventana_cal.winfo_screenwidth() // 2) - (800 // 2)
    y = (ventana_cal.winfo_screenheight() // 2) - (500 // 2)
    ventana_cal.geometry(f"800x500+{x}+{y}")

    main_frame = ctk.CTkFrame(ventana_cal)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(main_frame, text="Seleccionar Rango de Fechas", font=("Georgia", 18, "bold")).pack(pady=10)

    cal_frame = ctk.CTkFrame(main_frame)
    cal_frame.pack(fill="both", expand=True, padx=20, pady=10)

    frame_inicio = ctk.CTkFrame(cal_frame)
    frame_inicio.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    ctk.CTkLabel(frame_inicio, text="Fecha Inicio", font=("Arial", 14, "bold")).pack(pady=5)
    cal_inicio = Calendar(frame_inicio, selectmode='day', date_pattern='dd/mm/yyyy')
    cal_inicio.pack(pady=10)

    frame_fin = ctk.CTkFrame(cal_frame)
    frame_fin.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    ctk.CTkLabel(frame_fin, text="Fecha Fin", font=("Arial", 14, "bold")).pack(pady=5)
    cal_fin = Calendar(frame_fin, selectmode='day', date_pattern='dd/mm/yyyy')
    cal_fin.pack(pady=10)

    btn_frame = ctk.CTkFrame(main_frame)
    btn_frame.pack(fill="x", padx=20, pady=10)

    def aplicar_fechas():
        fecha_inicio = cal_inicio.get_date()
        fecha_fin = cal_fin.get_date()
        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha de inicio debe ser anterior a la fecha fin")
            return
        fecha_inicio_cal.delete(0, "end")
        fecha_inicio_cal.insert(0, fecha_inicio)
        fecha_corte_cal.delete(0, "end")
        fecha_corte_cal.insert(0, fecha_fin)
        ventana_cal.destroy()
        actualizar_lista()

    def limpiar_fechas():
        fecha_inicio_cal.delete(0, "end")
        fecha_corte_cal.delete(0, "end")
        ventana_cal.destroy()
        actualizar_lista()
        
    ctk.CTkButton(btn_frame, text="Aplicar", command=aplicar_fechas, fg_color="#4CAF50", hover_color="#45a049").pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Limpiar Filtros", command=limpiar_fechas, fg_color="#FF6B6B", hover_color="#FF5252").pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Cancelar", command=ventana_cal.destroy, fg_color="#9E9E9E", hover_color="#757575").pack(side="right", padx=10)

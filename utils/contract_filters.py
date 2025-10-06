import customtkinter as ctk
from tkcalendar import Calendar, DateEntry
from tkinter import Toplevel, messagebox
from datetime import datetime

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

    min_date = datetime(2000, 1, 1).date()
    max_date = datetime(2050, 12, 31).date()

    main_frame = ctk.CTkFrame(ventana_cal)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(main_frame, text="Seleccionar Rango de Fechas", font=("Georgia", 18, "bold")).pack(pady=10)

    cal_frame = ctk.CTkFrame(main_frame)
    cal_frame.pack(fill="both", expand=True, padx=20, pady=10)

    frame_inicio = ctk.CTkFrame(cal_frame)
    frame_inicio.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    ctk.CTkLabel(frame_inicio, text="Fecha Inicio", font=("Arial", 14, "bold")).pack(pady=5)
    # Pasa mindate y maxdate a la inicialización del calendario
    cal_inicio = Calendar(frame_inicio, selectmode='day', date_pattern='dd/mm/yyyy', mindate=min_date, maxdate=max_date)
    cal_inicio.pack(pady=10)
    frame_fin = ctk.CTkFrame(cal_frame)
    frame_fin.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    ctk.CTkLabel(frame_fin, text="Fecha Fin", font=("Arial", 14, "bold")).pack(pady=5)
    # Pasa mindate y maxdate a la inicialización del calendario
    cal_fin = Calendar(frame_fin, selectmode='day', date_pattern='dd/mm/yyyy', mindate=min_date, maxdate=max_date)
    cal_fin.pack(pady=10)

    btn_frame = ctk.CTkFrame(main_frame)
    btn_frame.pack(fill="x", padx=20, pady=10)

    def aplicar_fechas():
        # Get the date strings from the Calendar widgets
        fecha_inicio_str = cal_inicio.get_date()
        fecha_fin_str = cal_fin.get_date()

        # Convert the date strings to datetime.date objects for comparison
        fecha_inicio_seleccionada = datetime.strptime(fecha_inicio_str, '%d/%m/%Y').date()
        fecha_fin_seleccionada = datetime.strptime(fecha_fin_str, '%d/%m/%Y').date()
        
        if fecha_inicio_seleccionada > fecha_fin_seleccionada:
            messagebox.showerror("Error", "La fecha de inicio debe ser anterior a la fecha fin")
            return
        
        # Now, update the main window's Entry widgets with the formatted date strings.
        fecha_inicio_cal.delete(0, "end")
        fecha_inicio_cal.insert(0, fecha_inicio_str) # Use the string directly from the calendar
        
        fecha_corte_cal.delete(0, "end")
        fecha_corte_cal.insert(0, fecha_fin_str) # Use the string directly from the calendar
        
        # Now that the widgets have been updated, you can destroy the window.
        ventana_cal.destroy()
        
        # Finally, call the function to update the contract list.
        actualizar_lista()

    def limpiar_fechas():
        # Lógica para limpiar las fechas
        fecha_inicio_cal.delete(0, "end")
        fecha_corte_cal.delete(0, "end")
        
        # Destroy the window and then update the list.
        ventana_cal.destroy()
        actualizar_lista()

        
    ctk.CTkButton(btn_frame, text="Aplicar", command=aplicar_fechas, fg_color="#4CAF50", hover_color="#45a049").pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Limpiar Filtros", command=limpiar_fechas, fg_color="#FF6B6B", hover_color="#FF5252").pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Cancelar", command=ventana_cal.destroy, fg_color="#9E9E9E", hover_color="#757575").pack(side="right", padx=10)

def filtrar_contratos(contratos, barra_busqueda, tipo_filtro, estado_filtro, fecha_inicio_cal, fecha_corte_cal):
    """Aplica todos los filtros a la lista de contratos y retorna una lista filtrada."""
    
    contratos_filtrados = []
    
    # Obtener fechas de filtro
    fecha_inicio_filtro = None
    fecha_corte_filtro = None
    if fecha_inicio_cal:
        try:
            fecha_inicio_filtro = datetime.strptime(fecha_inicio_cal, "%d/%m/%Y").date()
        except Exception:
            pass
    if fecha_corte_cal:
        try:
            fecha_corte_filtro = datetime.strptime(fecha_corte_cal, "%d/%m/%Y").date()
        except Exception:
            pass

    for contrato in contratos:
        # Filtro por nombre
        if barra_busqueda and barra_busqueda.lower() not in contrato["empleado"].lower():
            continue

        # Filtro por tipo
        if tipo_filtro != "Todos" and tipo_filtro.lower() not in contrato["tipo"].lower():
            continue

        # Filtro por estado
        if estado_filtro != "Todos" and contrato["estado"] != estado_filtro:
            continue
        
        # Filtro por fecha
        if fecha_inicio_filtro or fecha_corte_filtro:
            try:
                fecha_inicio_contrato = datetime.strptime(contrato["inicio"], '%Y-%m-%d').date()
                fecha_corte_contrato = datetime.strptime(contrato["corte"], '%Y-%m-%d').date()

                
                if fecha_inicio_filtro and fecha_inicio_contrato < fecha_inicio_filtro:
                    continue
                
                
                if fecha_corte_filtro and fecha_corte_contrato > fecha_corte_filtro:
                    continue
            except ValueError:
                
                continue
                
        contratos_filtrados.append(contrato)
        
    return contratos_filtrados
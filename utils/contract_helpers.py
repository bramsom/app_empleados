# utils/contract_helpers.py
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
from tkinter import messagebox

def fill_entry_field(entry_widget, value):
    """Helper para rellenar un campo de entrada."""
    entry_widget.delete(0, "end")
    entry_widget.insert(0, value or "")

def format_date_for_entry(date_str):
    """Formatea una cadena de fecha de YYYY-MM-DD a DD/MM/YYYY."""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        return date_str or ""

def format_money_for_entry(value):
    """Formatea un número con signo de peso y separador de miles para entry."""
    if value is None:
        return ""
    try:
        return f"$ {float(value):,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return str(value)

def parse_money_from_entry(formatted_string):
    """Convierte una cadena formateada ($ 1.000.000) a un número flotante."""
    if not formatted_string:
        return 0.0
    try:
        cleaned_string = formatted_string.replace("$", "").replace(" ", "").replace(".", "")
        return float(cleaned_string.replace(",", "."))
    except (ValueError, TypeError):
        messagebox.showerror("Error de Formato", f"El valor '{formatted_string}' no es un número válido.")
        return None

def abrir_calendario(parent, entry_widget):
    """Abre un widget de calendario para seleccionar una fecha."""
    top = tk.Toplevel(parent)
    top.title("Seleccionar fecha")
    top.geometry("+500+300")

    cal = Calendar(top, selectmode="day", date_pattern="dd/mm/yyyy",
                   mindate=datetime(2000, 1, 1).date(), maxdate=datetime(2050, 12, 31).date())
    cal.pack(padx=10, pady=10)

    def seleccionar_fecha():
        fecha = cal.get_date()
        fill_entry_field(entry_widget, fecha)
        top.destroy()

    tk.Button(top, text="Seleccionar", command=seleccionar_fecha).pack(pady=10)
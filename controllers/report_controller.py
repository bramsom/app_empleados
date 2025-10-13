from services.pdf_generator import obtener_periodo_laborado, calcular_tiempo_laborado
from tkinter import filedialog, messagebox
from services.excel_generator import obtener_datos_contratos, obtener_datos_empleados, obtener_datos_afiliaciones

def obtener_datos_para_excel(tablas=None):
    tablas = tablas or []
    sheets = []

    if "contratos" in tablas:
        # pedir al servicio que devuelva todas las filas normalizadas (no tocar BD aquí)
        rows = obtener_datos_contratos(include_all=True)
        columns = [
            ("id", "ID"),
            ("empleado", "Empleado"),
            ("tipo", "Tipo"),
            ("inicio", "Inicio"),
            ("corte", "Fin"),
            ("valor_estimado", "Valor estimado")
        ]
        widths = {"id":6, "empleado":36, "tipo":28, "inicio":14, "corte":14, "valor_estimado":16}
        sheets.append({"name":"Contratos", "rows":rows, "columns":columns, "column_widths":widths})

    if "empleados" in tablas:
        rows = obtener_datos_empleados()
        columns = [("id","ID"), ("document","Documento"), ("name","Nombre"), ("email","Email")]
        widths = {"id":6, "document":16, "name":30, "email":28}
        sheets.append({"name":"Empleados", "rows":rows, "columns":columns, "column_widths":widths})

    if "afiliaciones" in tablas:
        rows = obtener_datos_afiliaciones()
        columns = [("id","ID"), ("employee_id","Empleado"), ("tipo","Tipo"), ("inicio","Inicio")]
        widths = {"id":6, "employee_id":18, "tipo":20, "inicio":14}
        sheets.append({"name":"Afiliaciones", "rows":rows, "columns":columns, "column_widths":widths})

    return sheets

def exportar_a_excel(tablas=None):
    path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel","*.xlsx")])
    if not path:
        return
    sheets = obtener_datos_para_excel(tablas)

    # debug: mostrar contenido de sheets (útil para ver por qué no se crean hojas)
    try:
        # limitar tamaño del texto para el messagebox
        txt = repr(sheets)
        if len(txt) > 1500:
            txt = txt[:1500] + "\n... (truncado)"
        messagebox.showinfo("DEBUG - sheets", txt)
    except Exception:
        pass

    if not sheets:
        messagebox.showinfo("Exportar Excel", "No hay datos para exportar.")
        return

    try:
        from services.excel_generator import export_sheets_to_excel
        export_sheets_to_excel(path, sheets)
        messagebox.showinfo("Exportar Excel", f"Archivo guardado:\n{path}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar: {e}")

def obtener_datos_para_pdf():
    from services.employee_service import obtener_empleados
    return obtener_empleados()

class ReportController:
    @staticmethod
    def buscar_empleado_por_nombre_o_documento(empleados, texto):
        texto = texto.strip().lower()
        return [
            e for e in empleados
            if texto in e.name.lower() or texto in str(e.document_number).lower()
        ]

    @staticmethod
    def generar_info_laboral(empleado_id):
        fecha_inicio, fecha_fin = obtener_periodo_laborado(empleado_id)
        tiempo_laborado = calcular_tiempo_laborado(fecha_inicio, fecha_fin)
        return fecha_inicio, fecha_fin, tiempo_laborado
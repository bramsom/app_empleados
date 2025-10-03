from services.pdf_generator import obtener_periodo_laborado, calcular_tiempo_laborado

def obtener_datos_para_excel(tablas=None):
    # Importa las funciones necesarias
    from services.excel_generator import (
        obtener_datos_contratos,
        obtener_datos_empleados,
        obtener_datos_afiliaciones
    )
    datos = {}
    if not tablas or "contratos" in tablas:
        datos["contratos"] = obtener_datos_contratos()
    if not tablas or "empleados" in tablas:
        datos["empleados"] = obtener_datos_empleados()
    if not tablas or "afiliaciones" in tablas:
        datos["afiliaciones"] = obtener_datos_afiliaciones()
    return datos

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
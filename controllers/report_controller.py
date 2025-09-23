from services.excel_generator import obtener_datos_contratos

def obtener_datos_para_excel():
    """
    Devuelve una lista de diccionarios con los datos a exportar.
    """
    return obtener_datos_contratos()
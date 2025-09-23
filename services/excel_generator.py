from controllers.contract_controller import listar_contratos

def obtener_datos_contratos():
    """
    Devuelve una lista de diccionarios con los datos de los contratos.
    """
    contratos = listar_contratos()
    return contratos
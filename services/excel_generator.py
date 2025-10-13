from controllers.contract_controller import listar_contratos
from controllers.employee_controller import listar_empleados
from controllers.affiliation_controller import listar_afiliaciones

def obtener_datos_contratos():
    """
    Devuelve una lista de diccionarios con los datos de los contratos.
    """
    contratos = listar_contratos()
    return contratos

def obtener_datos_empleados():
    empleados = listar_empleados()
    # Convierte cada objeto a dict con todos sus campos
    return [emp.__dict__ for emp in empleados]

def obtener_datos_afiliaciones():
    """
    Devuelve una lista de diccionarios con los datos de las afiliaciones.
    """
    afiliaciones = listar_afiliaciones()
    return afiliaciones


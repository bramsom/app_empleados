from models.affiliation import Afiliacion
from services.affiliation_service import *

def registrar_afiliacion(datos_tuple):
    afiliacion = Afiliacion(    
        employee_id=datos_tuple[0],
        eps=datos_tuple[1],
        arl=datos_tuple[2],
        afp=datos_tuple[3],
        bank=datos_tuple[4],
        account_number=datos_tuple[5],
        account_type=datos_tuple[6]
    )
    crear_afiliacion(afiliacion)

def listar_afiliaciones():
    resultados = obtener_afiliaciones()
    return [Afiliacion(*r) for r in resultados]

def consultar_afiliacion(afiliacion_id):
    datos = obtener_afiliacion_por_id(afiliacion_id)
    if datos:
        return Afiliacion(*datos)
    return None

def consultar_afiliaciones_por_empleado(employee_id):
    resultados = obtener_afiliaciones_por_empleado(employee_id)
    return [Afiliacion(*r) for r in resultados]

def modificar_afiliacion(afiliacion_id, datos_tuple):
    afiliacion = Afiliacion(     
        employee_id=datos_tuple[0],
        eps=datos_tuple[1],
        arl=datos_tuple[2],
        afp=datos_tuple[3],
        bank=datos_tuple[4],
        account_number=datos_tuple[5],
        account_type=datos_tuple[6]
    )
    actualizar_afiliacion(afiliacion_id, afiliacion)

def borrar_afiliacion(afiliacion_id):
    eliminar_afiliacion(afiliacion_id)
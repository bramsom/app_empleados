from models.affiliation import Afiliacion
from services.affiliation_service import *

def registrar_afiliacion(datos_tuple):
    afiliacion = Afiliacion(*datos_tuple)
    crear_afiliacion(afiliacion)

def listar_afiliaciones():
    return obtener_afiliaciones()

def consultar_afiliacion(afiliacion_id):
    datos = obtener_afiliacion_por_id(afiliacion_id)
    if datos:
        return Afiliacion(*datos)
    return None

def modificar_afiliacion(afiliacion_id, datos_tuple):
    afiliacion = Afiliacion(*datos_tuple)
    actualizar_afiliacion(afiliacion_id, afiliacion)

def borrar_afiliacion(afiliacion_id):
    eliminar_afiliacion(afiliacion_id)
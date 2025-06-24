from models.contract import Contrato
from services.contract_service import *

def registrar_contrato(datos_tuple):
    contrato = Contrato(*datos_tuple)
    crear_contrato(contrato)

def listar_contratos():
    return obtener_contratos()

def consultar_contrato(contrato_id):
    datos = obtener_contrato_por_id(contrato_id)
    if datos:
        return Contrato(*datos)
    return None

def modificar_contrato(contrato_id, datos_tuple):
    contrato = Contrato(*datos_tuple)
    actualizar_contrato(contrato_id, contrato)

def borrar_contrato(contrato_id):
    eliminar_contrato(contrato_id)
from models.contract import Contrato
from services.contract_service import *

def registrar_contrato(datos_tuple):
    contrato = Contrato(employee_id=datos_tuple[0],
        type_contract=datos_tuple[1],
        start_date=datos_tuple[2],
        end_date=datos_tuple[3],
        value_hour=datos_tuple[4],
        number_hour=datos_tuple[5],
        monthly_payment=datos_tuple[6],
        transport=datos_tuple[7],
        state=datos_tuple[8],
        contractor=datos_tuple[9])
    crear_contrato(contrato)

def listar_contratos():
    return obtener_contratos()

def consultar_contratos_por_empleado(employee_id):
    resultados = obtener_contratos_por_empleado(employee_id)
    return [Contrato(*r) for r in resultados]

def consultar_contrato(contrato_id):
    datos = obtener_contrato_por_id(contrato_id)
    if datos:
        return Contrato(*datos)
    return None

def modificar_contrato(contrato_id, datos_tuple):
    contrato = Contrato(id=contrato_id,
        employee_id=datos_tuple[0],
        type_contract=datos_tuple[1],
        start_date=datos_tuple[2],
        end_date=datos_tuple[3],
        value_hour=datos_tuple[4],
        number_hour=datos_tuple[5],
        monthly_payment=datos_tuple[6],
        transport=datos_tuple[7],
        state=datos_tuple[8],
        contractor=datos_tuple[9])
    actualizar_contrato(contrato_id, contrato)

def borrar_contrato(contrato_id):
    eliminar_contrato(contrato_id)
from models.contract import Contrato
from services.contract_service import *

def registrar_contrato(datos_tuple):
    """Registra un nuevo contrato"""
    try:
        contrato = Contrato(
            employee_id=datos_tuple[0],
            type_contract=datos_tuple[1],
            start_date=datos_tuple[2],
            end_date=datos_tuple[3],
            value_hour=datos_tuple[4],
            number_hour=datos_tuple[5],
            monthly_payment=datos_tuple[6],
            transport=datos_tuple[7],
            state=datos_tuple[8],
            contractor=datos_tuple[9]
        )
        crear_contrato(contrato)
        return True
    except Exception as e:
        print(f"Error al registrar contrato: {e}")
        return False

def listar_contratos():
    """Lista todos los contratos - el servicio ya maneja el formato de fechas"""
    try:
        return obtener_contratos()
    except Exception as e:
        print(f"Error al listar contratos: {e}")
        return []

def consultar_contratos_por_empleado(employee_id):
    """Consulta contratos por empleado"""
    try:
        resultados = obtener_contratos_por_empleado(employee_id)
        return [Contrato(*r) for r in resultados]
    except Exception as e:
        print(f"Error al consultar contratos por empleado: {e}")
        return []

def consultar_contrato(contrato_id):
    """Consulta un contrato específico"""
    try:
        datos = obtener_contrato_por_id(contrato_id)
        if datos:
            return Contrato(*datos)
        return None
    except Exception as e:
        print(f"Error al consultar contrato: {e}")
        return None

def modificar_contrato(contrato_id, datos_tuple):
    """Modifica un contrato existente"""
    try:
        contrato = Contrato(
            id=contrato_id,
            employee_id=datos_tuple[0],
            type_contract=datos_tuple[1],
            start_date=datos_tuple[2],
            end_date=datos_tuple[3],
            value_hour=datos_tuple[4],
            number_hour=datos_tuple[5],
            monthly_payment=datos_tuple[6],
            transport=datos_tuple[7],
            state=datos_tuple[8],
            contractor=datos_tuple[9]
        )
        actualizar_contrato(contrato_id, contrato)
        return True
    except Exception as e:
        print(f"Error al modificar contrato: {e}")
        return False

def borrar_contrato(contrato_id):
    """Elimina un contrato"""
    try:
        eliminar_contrato(contrato_id)
        return True
    except Exception as e:
        print(f"Error al eliminar contrato: {e}")
        return False
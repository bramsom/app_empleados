from models.contract import Contrato
from services.contract_service import *
from utils.date_utils import to_db, to_display

def registrar_contrato(datos_contrato_dict):
    """
    Registra un nuevo contrato y sus detalles de pago.
    Recibe los datos en un solo diccionario.
    """
    try:
        contrato_obj = Contrato(
            id=None,
            employee_id=datos_contrato_dict.get('employee_id'),
            type_contract=datos_contrato_dict.get('type_contract'),
            # normalizar fechas a formato de DB
            start_date=to_db(datos_contrato_dict.get('start_date')),
            end_date=to_db(datos_contrato_dict.get('end_date')),
            state=datos_contrato_dict.get('state'),
            contractor=datos_contrato_dict.get('contractor'),
            total_payment=datos_contrato_dict.get('total_payment'),
            payment_frequency=datos_contrato_dict.get('payment_frequency'),
            monthly_payment=datos_contrato_dict.get('monthly_payment'),
            transport=datos_contrato_dict.get('transport'),
            value_hour=datos_contrato_dict.get('value_hour'),
            number_hour=datos_contrato_dict.get('number_hour'),
        )
        return crear_contrato(contrato_obj)
    except Exception as e:
        print(f"Error en el controlador al registrar contrato: {e}")
        return False


def listar_contratos():
    """Lista todos los contratos - el servicio ya maneja el formato de fechas"""
    try:
        return obtener_contratos()
    except Exception as e:
        print(f"Error al listar contratos: {e}")
        return []

def consultar_contrato(contrato_id):
    """Consulta un contrato específico"""
    try:
        datos = obtener_contrato_por_id(contrato_id)
        # El servicio ya retorna un objeto completo, no es necesario construirlo aquí
        return datos
    except Exception as e:
        print(f"Error al consultar contrato: {e}")
        return None


def modificar_contrato(contrato_id, datos_contrato_dict):
    """Modifica los datos principales de un contrato existente"""
    try:
        contrato = Contrato(
            employee_id=datos_contrato_dict.get('employee_id'),
            type_contract=datos_contrato_dict.get('type_contract'),
            # normalizar; si el campo viene vacío o None, enviar None y el servicio conservará lo original
            start_date=to_db(datos_contrato_dict.get('start_date')) if datos_contrato_dict.get('start_date') is not None else None,
            end_date=to_db(datos_contrato_dict.get('end_date')) if datos_contrato_dict.get('end_date') is not None else None,
            state=datos_contrato_dict.get('state'),
            contractor=datos_contrato_dict.get('contractor'),
            total_payment=datos_contrato_dict.get('total_payment'),
            payment_frequency=datos_contrato_dict.get('payment_frequency')
        )
        actualizar_contrato(contrato_id, contrato)
        return True
    except Exception as e:
        print(f"Error al modificar contrato: {e}")
        return False
def consultar_contratos_por_empleado(employee_id):
    """
    Consulta y devuelve una lista de contratos para un empleado específico.
    Esta es la función que la vista de detalle del empleado necesita.
    """
    try:
        return obtener_contratos_por_empleado(employee_id)
    except Exception as e:
        print(f"Error en el controlador al obtener contratos por empleado: {e}")
        return []
    
def modificar_pago_contrato(contrato_id, datos_pago_dict, fecha_efectiva):
    """Registra un cambio de pago en el historial del contrato"""
    try:
        # normalizar fecha efectiva
        fecha_norm = to_db(fecha_efectiva)
        actualizar_pago_contrato(contrato_id, datos_pago_dict, fecha_norm)
        return True
    except Exception as e:
        print(f"Error al modificar pago del contrato: {e}")
        return False

def borrar_contrato(contrato_id):
    """Elimina un contrato"""
    try:
        eliminar_contrato(contrato_id)
        return True
    except Exception as e:
        print(f"Error al eliminar contrato: {e}")
        return False

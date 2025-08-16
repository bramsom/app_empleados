from models.contract import Contrato
from services.contract_service import *

def registrar_contrato(datos_contrato_dict, datos_pago_dict):
    """
    Registra un nuevo contrato y sus detalles de pago.
    Recibe los datos en dos diccionarios separados.
    """
    try:
        # Creamos el objeto Contrato solo con los datos principales
        contrato = Contrato(
            employee_id=datos_contrato_dict.get('employee_id'),
            type_contract=datos_contrato_dict.get('type_contract'),
            start_date=datos_contrato_dict.get('start_date'),
            end_date=datos_contrato_dict.get('end_date'),
            state=datos_contrato_dict.get('state'),
            contractor=datos_contrato_dict.get('contractor'),
            total_payment=datos_contrato_dict.get('total_payment'),
            payment_frequency=datos_contrato_dict.get('payment_frequency')
        )
        # Llamamos al servicio con ambos diccionarios para manejar la lógica
        crear_contrato(contrato, datos_pago_dict)
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
        # Aquí solo se actualizan los datos del contrato principal
        contrato = Contrato(
            employee_id=datos_contrato_dict.get('employee_id'),
            type_contract=datos_contrato_dict.get('type_contract'),
            start_date=datos_contrato_dict.get('start_date'),
            end_date=datos_contrato_dict.get('end_date'),
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

def modificar_pago_contrato(contrato_id, datos_pago_dict, fecha_efectiva):
    """Registra un cambio de pago en el historial del contrato"""
    try:
        actualizar_pago_contrato(contrato_id, datos_pago_dict, fecha_efectiva)
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
from models.contract import Contrato
from services.contract_service import *
from utils.date_utils import to_db, to_display
from typing import List, Dict, Any, Tuple
from services import contract_service
from datetime import datetime
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
            position=datos_contrato_dict.get('position')  # <-- agregado
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
        return datos
    except Exception as e:
        print(f"Error al consultar contrato: {e}")
        return None


def modificar_contrato(contrato_id, datos_contrato_dict):
    """
    Modifica los datos principales de un contrato existente.
    Si el diccionario incluye 'applied_date' / 'effective_date' / 'fecha_efectiva'
    se usa como fecha de efectividad para los historiales (normalizada con to_db).
    Los campos que no estén en el diccionario o sean None no sobrescriben los originales.
    """
    try:
        # normalizar fecha de efectividad si viene
        fecha_raw = datos_contrato_dict.get('applied_date') or datos_contrato_dict.get('effective_date') or datos_contrato_dict.get('fecha_efectiva')
        fecha_norm = to_db(fecha_raw) if fecha_raw is not None else None

        contrato = Contrato(
            # enviar None para campos no provistos (servicio no los sobrescribe)
            employee_id=datos_contrato_dict.get('employee_id'),
            type_contract=datos_contrato_dict.get('type_contract'),
            start_date=to_db(datos_contrato_dict.get('start_date')) if datos_contrato_dict.get('start_date') is not None else None,
            end_date=to_db(datos_contrato_dict.get('end_date')) if datos_contrato_dict.get('end_date') is not None else None,
            state=datos_contrato_dict.get('state'),
            contractor=datos_contrato_dict.get('contractor'),
            total_payment=datos_contrato_dict.get('total_payment'),
            payment_frequency=datos_contrato_dict.get('payment_frequency'),
            monthly_payment=datos_contrato_dict.get('monthly_payment'),
            transport=datos_contrato_dict.get('transport'),
            value_hour=datos_contrato_dict.get('value_hour'),
            number_hour=datos_contrato_dict.get('number_hour'),
            position=datos_contrato_dict.get('position')  # <-- agregado
        )

        actualizar_contrato(contrato_id, contrato, applied_date=fecha_norm)
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
    """
    Registra un cambio de pago en el historial del contrato.
    Construye un Contrato mínimo (solo campos de pago) y delega en actualizar_contrato.
    fecha_efectiva puede venir en formatos que to_db normaliza.
    """
    try:
        # normalizar fecha efectiva (si es None -> None, servicio usará hoy)
        fecha_norm = to_db(fecha_efectiva) if fecha_efectiva is not None else None

        contrato_actual = obtener_contrato_por_id(contrato_id)
        if not contrato_actual:
            raise ValueError("Contrato no encontrado.")

        type_contract = contrato_actual[3]  # índice según obtener_contrato_por_id

        contrato_obj = Contrato(
            id=contrato_id,
            employee_id=contrato_actual[1],
            type_contract=type_contract
        )

        if type_contract in ['CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO',
                             'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO',
                             'CONTRATO APRENDIZAJE SENA']:
            contrato_obj.monthly_payment = datos_pago_dict.get('monthly_payment')
            contrato_obj.transport = datos_pago_dict.get('transport')

        elif type_contract == 'CONTRATO SERVICIO HORA CATEDRA':
            contrato_obj.value_hour = datos_pago_dict.get('value_hour')
            contrato_obj.number_hour = datos_pago_dict.get('number_hour')

        elif type_contract == 'ORDEN PRESTACION DE SERVICIOS':
            contrato_obj.total_payment = datos_pago_dict.get('new_total_payment') if datos_pago_dict.get('new_total_payment') is not None else datos_pago_dict.get('total_payment')
            contrato_obj.payment_frequency = datos_pago_dict.get('new_payment_frequency') if datos_pago_dict.get('new_payment_frequency') is not None else datos_pago_dict.get('payment_frequency')

        else:
            raise ValueError("Tipo de contrato no soportado para modificar pago.")

        actualizar_contrato(contrato_id, contrato_obj, applied_date=fecha_norm)
        return True
    except Exception as e:
        print(f"Error al modificar pago del contrato: {e}")
        return False

def _fmt_date(d):
    if not d:
        return ""
    try:
        # aceptar YYYY-MM-DD o datetime
        if isinstance(d, datetime):
            return d.strftime("%d/%m/%Y")
        return datetime.strptime(str(d), "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return str(d)

def obtener_historial_por_contrato(contract_id: int, type_contract: str) -> Dict[str, Any]:
    """
    Devuelve {'headers': [...], 'rows': [[...], ...]}
    Las filas están formateadas para mostrar en la UI.
    """
    # Contratos por salario
    if type_contract in [
        "CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO",
        "CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO",
        "CONTRATO APRENDIZAJE SENA"
    ]:
        raw = contract_service.obtener_historial_salario(contract_id)
        headers = ["Fecha efectividad", "Salario mensual", "Transporte"]
        rows = [
            [_fmt_date(r.get("effective_date")), r.get("monthly_payment") or "", r.get("transport") or ""]
            for r in raw
        ]
        return {"headers": headers, "rows": rows}

    # Contratos por horas
    if type_contract == "CONTRATO SERVICIO HORA CATEDRA":
        raw = contract_service.obtener_historial_horas(contract_id)
        headers = ["Fecha efectividad", "Valor hora", "Número horas"]
        rows = [
            [_fmt_date(r.get("effective_date")), r.get("value_hour") or "", r.get("number_hour") or ""]
            for r in raw
        ]
        return {"headers": headers, "rows": rows}

    # Orden de prestación de servicios
    if type_contract == "ORDEN PRESTACION DE SERVICIOS":
        raw = contract_service.obtener_historial_ordenes(contract_id)
        headers = ["Fecha efectividad", "Antiguo total", "Nuevo total", "Ant. frecuencia", "Nueva frecuencia"]
        rows = [
            [
                _fmt_date(r.get("effective_date")),
                r.get("old_total_payment") or "",
                r.get("new_total_payment") or "",
                r.get("old_payment_frequency") or "",
                r.get("new_payment_frequency") or ""
            ]
            for r in raw
        ]
        return {"headers": headers, "rows": rows}

    return {"headers": [], "rows": []}

def borrar_contrato(contrato_id):
    """Elimina un contrato"""
    try:
        eliminar_contrato(contrato_id)
        return True
    except Exception as e:
        print(f"Error al eliminar contrato: {e}")
        return False

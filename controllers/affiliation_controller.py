from models.affiliation import Afiliacion
from services import affiliation_service
def registrar_afiliacion(datos_tuple):
    # Ya está optimizado.
    afiliacion = Afiliacion(
        employee_id=datos_tuple[0],
        eps=datos_tuple[1],
        arl=datos_tuple[2],
        risk_level=datos_tuple[3],
        afp=datos_tuple[4],
        compensation_box=datos_tuple[5],
        bank=datos_tuple[6],
        account_number=datos_tuple[7],
        account_type=datos_tuple[8]
    )
    affiliation_service.crear_afiliacion(afiliacion)

def listar_afiliaciones():
    # The service now returns EmpleadoAfiliacion objects, so the controller is clean
    return affiliation_service.obtener_afiliaciones()

def consultar_afiliacion(afiliacion_id):
    # El servicio ya retorna un objeto (o None), así que se simplifica la llamada.
    return affiliation_service.obtener_afiliacion_por_id(afiliacion_id)

def consultar_afiliaciones_por_empleado(employee_id):
    # El servicio ya retorna una lista de objetos, así que se simplifica la llamada.
    return affiliation_service.obtener_afiliaciones_por_empleado(employee_id)

def consultar_afiliaciones_con_nombre(employee_id):
    # Este ya está bien porque el servicio devuelve los objetos directamente.
    return affiliation_service.obtener_afiliacion_con_nombre_por_id(employee_id)

def modificar_afiliacion(afiliacion_id, datos_tuple):
    # Ya está optimizado.
    afiliacion = Afiliacion(
        employee_id=datos_tuple[0],
        eps=datos_tuple[1],
        arl=datos_tuple[2],
        risk_level=datos_tuple[3],
        afp=datos_tuple[4],
        compensation_box=datos_tuple[5],
        bank=datos_tuple[6],
        account_number=datos_tuple[7],
        account_type=datos_tuple[8]
    )
    affiliation_service.actualizar_afiliacion(afiliacion_id, afiliacion)

def borrar_afiliacion(afiliacion_id):
    # Ya está optimizado.
    affiliation_service.eliminar_afiliacion(afiliacion_id)
import services.employee_service as employee_service
from models.employee import Empleado
import sqlite3

def registrar_empleado(empleado: Empleado):
    """Registra un nuevo empleado en la base de datos."""
    try:
        employee_service.crear_empleado(empleado)
        return True
    except sqlite3.IntegrityError:
        # Este error es específico de duplicado de ID, es bueno manejarlo
        raise ValueError("El número de documento ya está registrado.")
    except Exception as e:
        print(f"Error al registrar empleado: {e}")
        return False

def listar_empleados():
    """Consulta y devuelve una lista de todos los empleados."""
    try:
        # El servicio ahora retorna directamente la lista de objetos Empleado
        return employee_service.obtener_empleados()
    except Exception as e:
        print(f"Error al listar empleados: {e}")
        return []

def consultar_empleado_por_id(employee_id):
    """Consulta y devuelve un empleado por su ID."""
    try:
        # El servicio ya retorna el objeto Empleado o None
        return employee_service.obtener_empleado_por_id(employee_id)
    except Exception as e:
        print(f"Error al consultar empleado: {e}")
        return None

def agregar_empleado(datos_empleado):
    """Agrega un nuevo empleado a la base de datos."""
    try:
        # El servicio ya espera un objeto Empleado, no un diccionario
        empleado = Empleado(
            id_=datos_empleado.get('id'),
            name=datos_empleado.get('name'),
            last_name=datos_empleado.get('last_name'),
            document_type=datos_empleado.get('document_type'),
            document_number=datos_empleado.get('document_number'),
            document_issuance=datos_empleado.get('document_issuance'),
            birthdate=datos_empleado.get('birthdate'),
            phone_number=datos_empleado.get('phone_number'),
            residence_address=datos_empleado.get('residence_address'),
            RUT=datos_empleado.get('RUT'),
            email=datos_empleado.get('email')
            # NOTA: no pasar 'position' aquí — ahora viene desde contracts
        )
        employee_service.crear_empleado(empleado)
        return True
    except Exception as e:
        print(f"Error al agregar empleado: {e}")
        return False
    
def modificar_empleado(empleado_id, datos_empleado):
    """Modifica un empleado existente por su ID."""
    try:
        employee_service.actualizar_empleado(empleado_id, datos_empleado)
        return True
    except Exception as e:
        print(f"Error al modificar empleado: {e}")
        return False

def eliminar_empleado(empleado_id):
    """Elimina un empleado por su ID."""
    try:
        employee_service.eliminar_empleado(empleado_id)
        return True
    except Exception as e:
        print(f"Error al eliminar empleado: {e}")
        return False

def buscar_empleados(query):
    """Busca empleados por nombre, apellido, cargo o cédula."""
    try:
        return employee_service.buscar_empleados_por_criterio(query)
    except Exception as e:
        print(f"Error al buscar empleados: {e}")
        return []
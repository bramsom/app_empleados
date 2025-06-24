from models.employee import Empleado
from services.employee_service import *
from services.employee_service import actualizar_empleado as actualizar_empleado_bd
from services.employee_service import eliminar_empleado as eliminar_empleado_service

def registrar_empleado(empleado: Empleado):
    crear_empleado(empleado)

def listar_empleados():
    datos = obtener_empleados()
    return [Empleado(*fila) for fila in datos]

def consultar_empleado(id):
    datos = obtener_empleado_por_id(id)
    if datos:
        return Empleado(*datos)
    return None

def actualizar_empleado(id, empleado: Empleado):
    actualizar_empleado_bd(id, empleado)

def eliminar_empleado(id):
    eliminar_empleado_service(id)

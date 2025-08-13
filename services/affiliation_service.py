import sqlite3
from bd.connection import conectar
from models.affiliation import Afiliacion , EmpleadoAfiliacion

def crear_afiliacion(afiliacion: Afiliacion):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO affiliations (
            employee_id, eps, arl, risk_level, afp,
            compensation_box, bank, account_number, account_type
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, afiliacion.to_tuple())
    conn.commit()
    conn.close()

def obtener_afiliaciones():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            affiliations.id,
            employees.name || ' ' || employees.last_name AS empleado,
            affiliations.eps,
            affiliations.arl,
            affiliations.risk_level,
            affiliations.afp,
            affiliations.compensation_box,
            affiliations.bank,
            affiliations.account_number,
            affiliations.account_type
        FROM affiliations
        JOIN employees ON employees.id = affiliations.employee_id
    """)
    resultados_tuplas = cursor.fetchall()
    conn.close()
    
    return [EmpleadoAfiliacion(*tupla) for tupla in resultados_tuplas]

def obtener_afiliacion_con_nombre_por_id(afiliacion_id):
    """
    Obtiene una afiliación por su ID, incluyendo el nombre completo del empleado.
    """
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT affiliations.id,
               employees.name || ' ' || employees.last_name AS empleado,
               affiliations.eps,
               affiliations.arl,
               affiliations.risk_level,
               affiliations.afp,
               affiliations.compensation_box,
               affiliations.bank,
               affiliations.account_number,
               affiliations.account_type
        FROM affiliations
        JOIN employees ON employees.id = affiliations.employee_id
        WHERE affiliations.id = ?
    """, (afiliacion_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        # Retorna un único objeto EmpleadoAfiliacion
        return EmpleadoAfiliacion(*row)
    return None

def obtener_afiliacion_por_id(afiliacion_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, employee_id, eps, arl, risk_level, afp, compensation_box, bank, account_number, account_type
        FROM affiliations
        WHERE id=?
    """, (afiliacion_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Afiliacion(*row)
    return None

def obtener_afiliaciones_por_empleado(employee_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, eps, arl, risk_level, afp, compensation_box, bank, account_number, account_type
        FROM affiliations
        WHERE employee_id = ?
    """, (employee_id,))

    resultados_tuplas = cursor.fetchall()
    conexion.close()

    return [Afiliacion(*tupla) for tupla in resultados_tuplas]

def actualizar_afiliacion(afiliacion_id, afiliacion: Afiliacion):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE affiliations SET
        employee_id=?, eps=?, arl=?, risk_level=?, afp=?, compensation_box=?, bank=?, account_number=?, account_type=?
        WHERE id=?
    """, afiliacion.to_tuple()+(afiliacion_id,))
    conn.commit()
    conn.close()

def eliminar_afiliacion(afiliacion_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM affiliations WHERE id=?", (afiliacion_id,))
    conn.commit()
    conn.close()
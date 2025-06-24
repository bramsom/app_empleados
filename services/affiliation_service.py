import sqlite3
from bd.connection import conectar

def crear_afiliacion(afiliacion):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO affiliations (employee_id, affiliation_type, name, bank, account_number, account_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """,afiliacion.to_tuple())
    conn.commit()
    conn.close()

def obtener_afiliaciones():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT affiliations.id, employees.name || ' ' || employees.last_name AS empleado, affiliation_type, affiliations.name AS nombre_afiliacion
        FROM affiliations
        JOIN employees ON employees.id = affiliations.employee_id
    """)
    afiliaciones = cursor.fetchall()
    conn.close()
    return afiliaciones

def obtener_afiliacion_por_id(afiliacion_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM affiliations WHERE id=?",(afiliacion_id,))
    afiliacion = cursor.fetchone()
    conn.close()
    return afiliacion

def actualizar_afiliacion(afiliacion_id, afiliacion):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE affiliations SET
        employee_id=?, affiliation_type=?, name=?, bank=?, account_number=?, account_type=?
        WHERE id=?
    """, afiliacion.to_tuple()+(afiliacion_id))
    conn.commit()
    conn.close()

def eliminar_afiliacion(afiliacion_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM affiliations WHERE id=?",(afiliacion_id,))
    conn.commit()
    conn.close
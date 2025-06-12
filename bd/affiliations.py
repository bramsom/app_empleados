import sqlite3
from .connection import conectar

def crear_afiliacion(datos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO affiliations (employee_id, affiliation_type, name, bank, account_number, account_type)
        VALUES (?, ?, ?, ?, ?, ?)
    """, datos)
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
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_afiliacion_por_id(af_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM affiliations WHERE id=?", (af_id,))
    datos = cursor.fetchone()
    conn.close()
    return datos

def actualizar_afiliacion(af_id, datos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE affiliations SET
        employee_id=?, affiliation_type=?, name=?, bank=?, account_number=?, account_type=?
        WHERE id=?
    """, (*datos, af_id))
    conn.commit()
    conn.close()

def eliminar_afiliacion(af_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM affiliations WHERE id=?", (af_id,))
    conn.commit()
    conn.close()

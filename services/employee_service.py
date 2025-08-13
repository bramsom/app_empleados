import sqlite3
from bd.connection import conectar
from models.employee import Empleado  # ¡Asegúrate de importar tu clase Empleado!


def crear_empleado(empleado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO employees 
        (name, last_name, document_type, document_number, document_issuance,
        birthdate, phone_number, residence_address, RUT, email, position)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, empleado.to_tuple())
    conn.commit()
    conn.close()

def obtener_empleados():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_empleado_por_id(emp_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT id, name, last_name, document_type, document_number, document_issuance,birthdate,
                phone_number, residence_address, RUT, email, position
                FROM employees 
                WHERE id = ?""", (emp_id,))
    emp_tuple = cursor.fetchone()
    conn.close()

    if emp_tuple:
        return Empleado(*emp_tuple)
    return None

def actualizar_empleado(emp_id, empleado):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employees SET 
        name=?, last_name=?, document_type=?, document_number=?, document_issuance=?,
        birthdate=?, phone_number=?, residence_address=?, RUT=?, email=?, position=?
        WHERE id=?
    """, empleado.to_tuple() + (emp_id,))
    conn.commit()
    conn.close()

def eliminar_empleado(emp_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    conn.commit()
    conn.close()

def obtener_empleados_para_combobox():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name || ' ' || last_name FROM employees")
    empleados = cursor.fetchall()
    conn.close()
    return empleados

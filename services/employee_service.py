import sqlite3
from bd.connection import conectar

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
    cursor.execute("SELECT id, name, last_name, document_number, email FROM employees")
    datos = cursor.fetchall()
    conn.close()
    return datos

def obtener_empleado_por_id(emp_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
    emp = cursor.fetchone()
    conn.close()
    return emp

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

import sqlite3
from .connection import conectar

def crear_empleado(data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO employees 
        (name, last_name, document_type, document_number, document_issuance,
         birthdate, phone_number, residence_address, RUT, email, position)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def obtener_empleados():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, last_name, document_number, email FROM employees")
    empleados = cursor.fetchall()
    conn.close()
    return empleados

def obtener_empleado_por_id(emp_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id = ?", (emp_id,))
    emp = cursor.fetchone()
    conn.close()
    return emp

def actualizar_empleado(emp_id, data):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employees SET 
        name = ?, last_name = ?, document_type = ?, document_number = ?, 
        document_issuance = ?, birthdate = ?, phone_number = ?, 
        residence_address = ?, RUT = ?, email = ?, position = ?
        WHERE id = ?
    """, data + (emp_id,))
    conn.commit()
    conn.close()

def eliminar_empleado(emp_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
    conn.commit()
    conn.close()

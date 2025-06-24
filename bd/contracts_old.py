import sqlite3
from .connection import conectar

def crear_contrato(datos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contracts (employee_id, type_contract, start_date, end_date, value_hour, number_hour, monthly_payment, transport, state, contractor)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, datos)
    conn.commit()
    conn.close()
    
def obtener_contratos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT contracts.id, employees.name || ' ' || employees.last_name AS empleado, type_contract, start_date, end_date, state
        FROM contracts
        JOIN employees ON employees.id = contracts.employee_id
    """)
    contratos = cursor.fetchall()
    conn.close()
    return contratos

def obtener_contrato_por_id(contrato_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contracts WHERE id = ?", (contrato_id,))
    contrato = cursor.fetchone()
    conn.close()
    return contrato

def actualizar_contrato(contrato_id, datos):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE contracts SET 
        employee_id=?, type_contract=?, start_date=?, end_date=?, 
        value_hour=?, number_hour=?, monthly_payment=?, transport=?, 
        state=?, contractor=? 
        WHERE id=?
    """, (*datos, contrato_id))
    conn.commit()
    conn.close()

def eliminar_contrato(contrato_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contracts WHERE id=?", (contrato_id,))
    conn.commit()
    conn.close()
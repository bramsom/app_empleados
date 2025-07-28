import sqlite3
from bd.connection import conectar

def  crear_contrato(contrato):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contracts 
        (employee_id, type_contract, start_date, end_date, value_hour, number_hour, monthly_payment, transport, state, contractor)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,contrato.to_tuple())
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
    conn =conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contracts WHERE id = ?", (contrato_id,))
    contrato =cursor.fetchone()
    conn.close()
    return contrato

def obtener_contratos_por_empleado(employee_id):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, employee_id, type_contract, start_date, end_date, value_hour, number_hour,monthly_payment,transport,state,contractor
        FROM contracts
        WHERE employee_id = ?
    """, (employee_id,))
    
    resultados = cursor.fetchall()
    conexion.close()
    return resultados

def actualizar_contrato(contrato_id, contrato):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE contracts SET 
            employee_id=?, type_contract=?, start_date=?, end_date=?, 
            value_hour=?, number_hour=?, monthly_payment=?, transport=?, 
            state=?, contractor=? 
            WHERE id=?
        """,contrato.to_tuple()+ (contrato_id,))
        conn.commit()
    except Exception as e: 
        print("error al actualizar el contrato:", e)
        raise
    finally:
        conn.close()

def eliminar_contrato(contrato_id):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contracts WHERE id=?", (contrato_id,)) 
        conn.commit()
    except Exception as e:
        print("Error al eliminar contrato:", e)
        raise
    finally:
        conn.close() 
    
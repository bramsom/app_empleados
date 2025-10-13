import sqlite3
from bd.connection import conectar
from models.employee import Empleado

def crear_empleado(empleado):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO employees 
            (name, last_name, document_type, document_number, document_issuance,
            birthdate, phone_number, residence_address, RUT, email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            empleado.name, empleado.last_name, empleado.document_type,
            empleado.document_number, empleado.document_issuance,
            empleado.birthdate, empleado.phone_number, empleado.residence_address,
            empleado.RUT, empleado.email
        ))
        conn.commit()
    except Exception as e:
        print(f"Error al crear empleado: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def obtener_empleados():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT
                id, name, last_name, document_type, document_number, document_issuance,
                birthdate, phone_number, residence_address, RUT, email
            FROM employees
        """)
        datos = cursor.fetchall()
        
        lista_empleados = []
        for fila in datos:
            lista_empleados.append(Empleado(*fila))
        return lista_empleados
    except Exception as e:
        print(f"Error al obtener empleados: {e}")
        return []
    finally:
        conn.close()

def obtener_empleado_por_id(employee_id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT
                id, name, last_name, document_type, document_number, document_issuance,
                birthdate, phone_number, residence_address, RUT, email
            FROM employees
            WHERE id = ?
        """, (employee_id,))
        emp_tuple = cursor.fetchone()
        
        if emp_tuple:
            return Empleado(*emp_tuple)
        return None
    except Exception as e:
        print(f"Error al obtener empleado por ID: {e}")
        return None
    finally:
        conn.close()

def actualizar_empleado(empleado_id, datos_empleado):
    conn = conectar()
    cursor = conn.cursor()
    try:
        # Se verifica si el empleado existe antes de actualizar
        if not obtener_empleado_por_id(empleado_id):
            raise ValueError("Empleado no encontrado.")

        cursor.execute("""
            UPDATE employees SET 
            name=?, last_name=?, document_type=?, document_number=?, document_issuance=?,
            birthdate=?, phone_number=?, residence_address=?, RUT=?, email=?
            WHERE id=?
        """, (
            datos_empleado.name, datos_empleado.last_name, datos_empleado.document_type,
            datos_empleado.document_number, datos_empleado.document_issuance,
            datos_empleado.birthdate, datos_empleado.phone_number, datos_empleado.residence_address,
            datos_empleado.RUT, datos_empleado.email,
            empleado_id
        ))
        conn.commit()
    except Exception as e:
        print(f"Error al actualizar empleado: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

def eliminar_empleado(employee_id):
    """
    Elimina un empleado; las filas relacionadas deben eliminarse por ON DELETE CASCADE.
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
        if cursor.rowcount == 0:
            conn.rollback()
            return False
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise
    finally:
        conn.close()

def buscar_empleados_por_criterio(query):
    conn = conectar()
    cursor = conn.cursor()
    try:
        search_query = f"%{query}%"
        cursor.execute("""
            SELECT
                id, name, last_name, document_type, document_number, document_issuance,
                birthdate, phone_number, residence_address, RUT, email
            FROM employees
            WHERE name LIKE ? OR last_name LIKE ? OR document_number LIKE ? OR email LIKE ?
        """, (search_query, search_query, search_query, search_query))
        
        datos = cursor.fetchall()
        
        lista_empleados = []
        for fila in datos:
            lista_empleados.append(Empleado(*fila))
        return lista_empleados
    except Exception as e:
        print(f"Error al buscar empleados: {e}")
        return []
    finally:
        conn.close()

def obtener_empleados_para_combobox():
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name || ' ' || last_name FROM employees")
        empleados = cursor.fetchall()
        return empleados
    except Exception as e:
        print(f"Error al obtener empleados para combobox: {e}")
        return []
    finally:
        conn.close()

def obtener_cargo_actual(employee_id):
    """
    Retorna el 'position' del contrato más reciente (por start_date) para el empleado,
    o None si no existe o la posición es NULL.
    """
    conn = conectar()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT position FROM contracts
            WHERE employee_id = ?
              AND start_date IS NOT NULL
            ORDER BY date(start_date) DESC
            LIMIT 1
        """, (employee_id,))
        row = cur.fetchone()
        return row[0] if row and row[0] is not None else None
    finally:
        conn.close()
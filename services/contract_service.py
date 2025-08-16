import sqlite3
from bd.connection import conectar
from datetime import datetime

def crear_contrato(contrato):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN TRANSACTION;")

        # Paso 1: Insertar en la tabla principal de contratos
        cursor.execute("""
            INSERT INTO contracts 
            (employee_id, type_contract, start_date, end_date, state, contractor, total_payment, payment_frequency)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            contrato.employee_id, contrato.type_contract, contrato.start_date, 
            contrato.end_date, contrato.state, contrato.contractor, contrato.total_payment, contrato.payment_frequency
        ))
        
        contrato_id = cursor.lastrowid

        # Paso 2: Insertar en la tabla de historial de pagos según el tipo de contrato
        if contrato.type_contract in ['CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO',
                                      'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO',
                                      'CONTRATO APRENDIZAJE SENA']:
            cursor.execute("""
                INSERT INTO salary_history 
                (contract_id, monthly_payment, transport, effective_date)
                VALUES (?, ?, ?, ?)
            """, (contrato_id, contrato.monthly_payment, contrato.transport, contrato.start_date))

        elif contrato.type_contract == 'CONTRATO SERVICIO HORA CATEDRA':
            cursor.execute("""
                INSERT INTO hourly_history 
                (contract_id, value_hour, number_hour, effective_date)
                VALUES (?, ?, ?, ?)
            """, (contrato_id, contrato.value_hour, contrato.number_hour, contrato.start_date))

        elif contrato.type_contract == 'ORDEN PRESTACION DE SERVICIOS':
            cursor.execute("""
                INSERT INTO service_order_history
                (contract_id, old_total_payment, new_total_payment, old_payment_frequency, new_payment_frequency, effective_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (contrato_id, None, contrato.total_payment, None, contrato.payment_frequency, contrato.start_date))

        
        conn.commit()
        return True # Devuelve True en caso de éxito
    except Exception as e:
        print("Error al crear el contrato:", e)
        conn.rollback()
        raise
    finally:
        conn.close()
def obtener_contratos():
    conn = conectar() 
    cursor = conn.cursor()
    
    # Se agrega el JOIN para service_order_history
    cursor.execute("""
        SELECT
            c.id,
            e.name || ' ' || e.last_name AS empleado,
            c.type_contract,
            c.start_date,
            c.end_date,
            sh.monthly_payment,
            sh.transport,
            hh.value_hour,
            hh.number_hour,
            soh.new_total_payment,
            soh.new_payment_frequency,
            c.state,
            c.contractor
        FROM contracts c
        JOIN employees e ON e.id = c.employee_id
        LEFT JOIN salary_history sh ON sh.contract_id = c.id
        LEFT JOIN hourly_history hh ON hh.contract_id = c.id
        LEFT JOIN service_order_history soh ON soh.contract_id = c.id
        GROUP BY c.id;
    """)
    contratos_raw = cursor.fetchall()
    conn.close()
    
    contratos = []
    for row in contratos_raw:
        # Se actualizan las variables para reflejar el nuevo JOIN
        (
            id_, empleado, tipo, inicio, corte, mensualidad, transporte,
            valor_hora, num_horas, pago_total, frecuencia_pago, estado, contratante
        ) = row

        # La lógica para el valor estimado se actualiza
        if tipo == 'CONTRATO SERVICIO HORA CATEDRA':
            valor_estimado = valor_hora * num_horas if valor_hora and num_horas else 0
        elif tipo == 'ORDEN PRESTACION DE SERVICIOS':
            # El valor estimado es el pago total, no la mensualidad
            valor_estimado = pago_total or 0
        else: # Contratos fijos, indefinidos y de aprendizaje
            valor_estimado = mensualidad or 0

        contratos.append({
            "id": id_,
            "empleado": empleado,
            "tipo": tipo,
            "inicio": inicio,
            "corte": corte,
            "valor_estimado": valor_estimado,
            "salario_mensual": mensualidad,
            "transporte": transporte,
            "valor_hora": valor_hora,
            "num_horas": num_horas,
            "estado": estado,
            "contratante": contratante,
            "pago_total": pago_total,
            "frecuencia_pago": frecuencia_pago,
        })
    return contratos

def obtener_contrato_por_id(contrato_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            c.id, c.employee_id, c.type_contract, c.start_date, c.end_date,
            sh.monthly_payment, sh.transport, hh.value_hour, hh.number_hour, c.total_payment, c.payment_frequency,
            c.state, c.contractor
        FROM contracts c
        LEFT JOIN salary_history sh ON sh.contract_id = c.id
        LEFT JOIN hourly_history hh ON hh.contract_id = c.id
        WHERE c.id = ?
    """, (contrato_id,))
    contrato = cursor.fetchone()
    conn.close()
    return contrato

# Esta función solo actualiza los campos principales del contrato.
def actualizar_contrato(contrato_id, contrato):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE contracts SET 
            employee_id=?, type_contract=?, start_date=?, end_date=?, 
            state=?, contractor=?, total_payment=?, payment_frequency=?
            WHERE id=?
        """, (
            contrato.employee_id, contrato.type_contract, contrato.start_date, 
            contrato.end_date, contrato.state, contrato.contractor, contrato.total_payment, contrato.payment_frequency, contrato_id
        ))
        conn.commit()
    except Exception as e:
        print("Error al actualizar el contrato:", e)
        raise
    finally:
        conn.close()

# Nueva función para actualizar salarios, creando un nuevo registro en el historial.
def actualizar_pago_contrato(contrato_id, nuevo_pago, nueva_fecha_efectiva):
    conn = conectar()
    try:
        cursor = conn.cursor()
        # Primero, verificamos el tipo de contrato y los valores antiguos
        cursor.execute("SELECT type_contract, total_payment, payment_frequency FROM contracts WHERE id=?", (contrato_id,))
        tipo_contrato, old_total_payment, old_payment_frequency = cursor.fetchone()

        if tipo_contrato in ['CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO', 'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO', 'CONTRATO APRENDIZAJE SENA']:
            cursor.execute("""
                INSERT INTO salary_history (contract_id, monthly_payment, transport, effective_date)
                VALUES (?, ?, ?, ?)
            """, (contrato_id, nuevo_pago.monthly_payment, nuevo_pago.transport, nueva_fecha_efectiva))
        elif tipo_contrato == 'CONTRATO SERVICIO HORA CATEDRA':
            cursor.execute("""
                INSERT INTO hourly_history (contract_id, value_hour, number_hour, effective_date)
                VALUES (?, ?, ?, ?)
            """, (contrato_id, nuevo_pago.value_hour, nuevo_pago.number_hour, nueva_fecha_efectiva))
        elif tipo_contrato == 'ORDEN PRESTACION DE SERVICIOS':
            cursor.execute("""
                INSERT INTO service_order_history (contract_id, old_total_payment, new_total_payment, old_payment_frequency, new_payment_frequency, effective_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (contrato_id, old_total_payment, nuevo_pago.total_payment, old_payment_frequency, nuevo_pago.payment_frequency, nueva_fecha_efectiva))

        # Finalmente, actualiza los campos principales en la tabla 'contracts'
        # para que reflejen el cambio.
        cursor.execute("""
            UPDATE contracts SET total_payment = ?, payment_frequency = ? WHERE id = ?
        """, (nuevo_pago.total_payment, nuevo_pago.payment_frequency, contrato_id))
        
        conn.commit()
    except Exception as e:
        print("Error al actualizar el pago del contrato:", e)
        conn.rollback()
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
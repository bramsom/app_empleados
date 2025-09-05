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
    
    # 1. Usar subconsultas para obtener los registros de historial más recientes
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
        
        -- Subconsulta para el historial de salario más reciente
        LEFT JOIN salary_history sh ON sh.contract_id = c.id
        AND sh.effective_date = (
            SELECT MAX(effective_date)
            FROM salary_history
            WHERE contract_id = sh.contract_id
        )
        
        -- Subconsulta para el historial de horas más reciente
        LEFT JOIN hourly_history hh ON hh.contract_id = c.id
        AND hh.effective_date = (
            SELECT MAX(effective_date)
            FROM hourly_history
            WHERE contract_id = hh.contract_id
        )
        
        -- Subconsulta para el historial de orden de servicio más reciente
        LEFT JOIN service_order_history soh ON soh.contract_id = c.id
        AND soh.effective_date = (
            SELECT MAX(effective_date)
            FROM service_order_history
            WHERE contract_id = soh.contract_id
        );
    """)
    
    contratos_raw = cursor.fetchall()
    conn.close()
    
    contratos = []
    for row in contratos_raw:
        # Aquí la lógica de procesamiento de los datos es la misma, no necesitas cambiarla.
        (
            id_, empleado, tipo, inicio, corte, mensualidad, transporte,
            valor_hora, num_horas, pago_total, frecuencia_pago, estado, contratante
        ) = row

        if tipo == 'CONTRATO SERVICIO HORA CATEDRA':
            valor_estimado = valor_hora * num_horas if valor_hora and num_horas else 0
        elif tipo == 'ORDEN PRESTACION DE SERVICIOS':
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

# En services/contract_service.py

def obtener_contrato_por_id(contrato_id):
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Start a single SELECT statement
    cursor.execute("""
        SELECT
            c.id,
            e.id,
            e.name || ' ' || e.last_name AS empleado,
            c.type_contract,
            c.start_date,
            c.end_date,
            c.state,
            c.contractor,
            c.total_payment,
            c.payment_frequency,
            sh.monthly_payment,
            sh.transport,
            hh.value_hour,
            hh.number_hour,
            soh.new_total_payment,
            soh.new_payment_frequency
        FROM contracts c
        LEFT JOIN employees e ON e.id = c.employee_id
        
        -- Subconsulta para el historial de salario más reciente
        LEFT JOIN (
            SELECT 
                contract_id, 
                monthly_payment, 
                transport
            FROM salary_history
            WHERE effective_date = (
                SELECT MAX(effective_date) 
                FROM salary_history 
                WHERE contract_id = salary_history.contract_id
            )
        ) sh ON sh.contract_id = c.id
        
        -- Subconsulta para el historial de horas más reciente
        LEFT JOIN (
            SELECT 
                contract_id, 
                value_hour, 
                number_hour
            FROM hourly_history
            WHERE effective_date = (
                SELECT MAX(effective_date) 
                FROM hourly_history 
                WHERE contract_id = hourly_history.contract_id
            )
        ) hh ON hh.contract_id = c.id
        
        -- Subconsulta para el historial de orden de servicio más reciente
        LEFT JOIN (
            SELECT 
                contract_id, 
                new_total_payment, 
                new_payment_frequency
            FROM service_order_history
            WHERE effective_date = (
                SELECT MAX(effective_date) 
                FROM service_order_history 
                WHERE contract_id = service_order_history.contract_id
            )
        ) soh ON soh.contract_id = c.id

        WHERE c.id = ?
        GROUP BY c.id
    """, (contrato_id,))
    
    contrato = cursor.fetchone()
    conn.close()
    
    return contrato


def actualizar_contrato(contrato_id, contrato_data):
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Obtener los datos originales del contrato para compararlos
    # Se usa la misma funcion que la vista detalle
    contrato_original = obtener_contrato_por_id(contrato_id)
    if not contrato_original:
        conn.close()
        raise ValueError("Contrato no encontrado.")
    
    # Se desempaquetan los datos originales
    (
        id_, emp_id_original, empleado_nombre, type_contract_original, start_date_original, end_date_original, state_original,
        contractor_original, total_payment_original, payment_frequency_original, monthly_payment_original, transport_original,
        value_hour_original, number_hour_original, new_total_payment_original, new_payment_frequency_original
    ) = contrato_original
    
    try:
        # 2. Actualizar los campos principales de la tabla 'contracts'
        cursor.execute("""
            UPDATE contracts SET
                employee_id = ?,
                type_contract = ?,
                start_date = ?,
                end_date = ?,
                state = ?,
                contractor = ?,
                total_payment = ?,
                payment_frequency = ?
            WHERE id = ?
        """, (
            contrato_data.employee_id,
            contrato_data.type_contract,
            contrato_data.start_date,
            contrato_data.end_date,
            contrato_data.state,
            contrato_data.contractor,
            contrato_data.total_payment,
            contrato_data.payment_frequency,
            contrato_id
        ))
        
        # 3. Insertar nuevos registros en las tablas de historial si los valores cambian
        if contrato_data.type_contract in ['CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO', 'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO', 'CONTRATO APRENDIZAJE SENA']:
            if contrato_data.monthly_payment != monthly_payment_original or contrato_data.transport != transport_original:
                cursor.execute("""
                    INSERT INTO salary_history (contract_id, monthly_payment, transport, effective_date)
                    VALUES (?, ?, ?, ?)
                """, (contrato_id, contrato_data.monthly_payment, contrato_data.transport, datetime.now().strftime('%Y-%m-%d')))
        
        elif contrato_data.type_contract == 'CONTRATO SERVICIO HORA CATEDRA':
            if contrato_data.value_hour != value_hour_original or contrato_data.number_hour != number_hour_original:
                cursor.execute("""
                    INSERT INTO hourly_history (contract_id, value_hour, number_hour, effective_date)
                    VALUES (?, ?, ?, ?)
                """, (contrato_id, contrato_data.value_hour, contrato_data.number_hour, datetime.now().strftime('%Y-%m-%d')))
        
        elif contrato_data.type_contract == 'ORDEN PRESTACION DE SERVICIOS':
            if contrato_data.total_payment != new_total_payment_original or contrato_data.payment_frequency != new_payment_frequency_original:
                cursor.execute("""
                    INSERT INTO service_order_history (contract_id, new_total_payment, new_payment_frequency, effective_date)
                    VALUES (?, ?, ?, ?)
                """, (contrato_id, contrato_data.total_payment, contrato_data.payment_frequency, datetime.now().strftime('%Y-%m-%d')))

        # 4. Confirmar la transacción
        conn.commit()
        
    except sqlite3.Error as e:
        conn.rollback()
        raise e
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
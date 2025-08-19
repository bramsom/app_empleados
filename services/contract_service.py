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
            c.id,
            e.id,
            e.name || ' ' || e.last_name AS empleado,  -- <-- Agrega el nombre completo del empleado aquí c.type_contract, c.start_date, c.end_date,
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
            hh.number_hour
        FROM contracts c
        LEFT JOIN employees e ON e.id = c.employee_id
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
    cursor = conn.cursor()
    try:
        # Iniciar la transacción para asegurar la coherencia de los datos
        conn.execute("BEGIN TRANSACTION")

        # 1. Obtener los datos del contrato original para comparar y registrar cambios
        cursor.execute("SELECT type_contract, total_payment, payment_frequency FROM contracts WHERE id=?", (contrato_id,))
        tipo_contrato_antiguo, pago_antiguo, frecuencia_antigua = cursor.fetchone()

        # 2. Actualizar la tabla principal 'contracts' con los nuevos datos
        cursor.execute("""
            UPDATE contracts SET 
            employee_id=?, type_contract=?, start_date=?, end_date=?, 
            state=?, contractor=?, total_payment=?, payment_frequency=?
            WHERE id=?
        """, (
            contrato.employee_id, contrato.type_contract, contrato.start_date, 
            contrato.end_date, contrato.state, contrato.contractor, contrato.total_payment, 
            contrato.payment_frequency, contrato_id
        ))

        # 3. Registrar los cambios en las tablas de historial si los valores de pago cambiaron
        # Comparamos el nuevo total_payment con el antiguo para saber si hubo un cambio
        if contrato.total_payment != pago_antiguo or contrato.payment_frequency != frecuencia_antigua:
            
            nueva_fecha_efectiva = datetime.now().strftime('%Y-%m-%d')

            if contrato.type_contract in ['CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO', 'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO', 'CONTRATO APRENDIZAJE SENA']:
                cursor.execute("""
                    INSERT INTO salary_history (contract_id, monthly_payment, transport, effective_date)
                    VALUES (?, ?, ?, ?)
                """, (contrato_id, contrato.monthly_payment, contrato.transport, nueva_fecha_efectiva))

            elif contrato.type_contract == 'CONTRATO SERVICIO HORA CATEDRA':
                cursor.execute("""
                    INSERT INTO hourly_history (contract_id, value_hour, number_hour, effective_date)
                    VALUES (?, ?, ?, ?)
                """, (contrato_id, contrato.value_hour, contrato.number_hour, nueva_fecha_efectiva))
                
            elif contrato.type_contract == 'ORDEN PRESTACION DE SERVICIOS':
                 cursor.execute("""
                    INSERT INTO service_order_history (contract_id, old_total_payment, new_total_payment, old_payment_frequency, new_payment_frequency, effective_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (contrato_id, pago_antiguo, contrato.total_payment, frecuencia_antigua, contrato.payment_frequency, nueva_fecha_efectiva))

        # 4. Confirmar la transacción para guardar todos los cambios
        conn.commit()

    except Exception as e:
        # Si algo sale mal, se revierte todo
        conn.rollback()
        print("Error al actualizar el contrato:", e)
        raise
    finally:
        # Cerrar la conexión
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
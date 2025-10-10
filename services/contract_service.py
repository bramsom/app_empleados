import sqlite3
from bd.connection import conectar
from datetime import datetime
from models.contract import Contrato

def crear_contrato(contrato):
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN TRANSACTION;")

        # Evitar crear duplicados (mismo empleado y misma fecha de inicio)
        cursor.execute("SELECT id FROM contracts WHERE employee_id = ? AND start_date = ? LIMIT 1",
                       (contrato.employee_id, contrato.start_date))
        exists = cursor.fetchone()
        if exists:
            raise ValueError("Ya existe un contrato con el mismo empleado y fecha de inicio. Si quiere modificar, use la edición.")

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
        conn.rollback()
        raise
    finally:
        conn.close()
def obtener_contratos():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            e.name || ' ' || e.last_name AS empleado,
            c.type_contract,
            c.start_date,
            c.end_date,
            -- obtener último salario y transporte como subconsultas (evita duplicados)
            (SELECT monthly_payment FROM salary_history sh WHERE sh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS monthly_payment,
            (SELECT transport FROM salary_history sh WHERE sh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS transport,
            (SELECT value_hour FROM hourly_history hh WHERE hh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS value_hour,
            (SELECT number_hour FROM hourly_history hh WHERE hh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS number_hour,
            (SELECT new_total_payment FROM service_order_history soh WHERE soh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS new_total_payment,
            (SELECT new_payment_frequency FROM service_order_history soh WHERE soh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS new_payment_frequency,
            c.state,
            c.contractor
        FROM contracts c
        JOIN employees e ON e.id = c.employee_id;
    """)
    contratos_raw = cursor.fetchall()
    conn.close()

    contratos = []
    for row in contratos_raw:
        (
            id_, empleado, tipo, inicio, corte, mensualidad, transporte,
            valor_hora, num_horas, pago_total, frecuencia_pago, estado, contratante
        ) = row

        if tipo == 'CONTRATO SERVICIO HORA CATEDRA':
            valor_estimado = valor_hora * num_horas if valor_hora and num_horas else 0
        elif tipo == 'ORDEN PRESTACION DE SERVICIOS':
            valor_estimado = pago_total or 0
        else:
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

    cursor.execute("""
        SELECT
            c.id,
            c.employee_id,
            e.name || ' ' || e.last_name AS empleado,
            c.type_contract,
            c.start_date,
            c.end_date,
            c.state,
            c.contractor,
            c.total_payment,
            c.payment_frequency,
            (SELECT monthly_payment FROM salary_history sh WHERE sh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS monthly_payment,
            (SELECT transport FROM salary_history sh WHERE sh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS transport,
            (SELECT value_hour FROM hourly_history hh WHERE hh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS value_hour,
            (SELECT number_hour FROM hourly_history hh WHERE hh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS number_hour,
            (SELECT new_total_payment FROM service_order_history soh WHERE soh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS new_total_payment,
            (SELECT new_payment_frequency FROM service_order_history soh WHERE soh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS new_payment_frequency
        FROM contracts c
        LEFT JOIN employees e ON e.id = c.employee_id
        WHERE c.id = ?
    """, (contrato_id,))

    contrato = cursor.fetchone()
    conn.close()

    return contrato

def obtener_contratos_por_empleado(employee_id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.id,
            c.employee_id,
            c.type_contract,
            c.start_date,
            c.end_date,
            c.state,
            c.contractor,
            (SELECT monthly_payment FROM salary_history sh WHERE sh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS monthly_payment,
            (SELECT transport FROM salary_history sh WHERE sh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS transport,
            (SELECT value_hour FROM hourly_history hh WHERE hh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS value_hour,
            (SELECT number_hour FROM hourly_history hh WHERE hh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS number_hour,
            (SELECT new_total_payment FROM service_order_history soh WHERE soh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS new_total_payment,
            (SELECT new_payment_frequency FROM service_order_history soh WHERE soh.contract_id = c.id ORDER BY effective_date DESC LIMIT 1) AS new_payment_frequency
        FROM contracts c
        WHERE c.employee_id = ?
        ORDER BY c.start_date DESC
    """, (employee_id,))

    contratos_raw = cursor.fetchall()
    conn.close()

    contratos = []
    for row in contratos_raw:
        contratos.append(
            Contrato(
                id=row[0],
                employee_id=row[1],
                type_contract=row[2],
                start_date=row[3],
                end_date=row[4],
                state=row[5],
                contractor=row[6],
                monthly_payment=row[7],
                transport=row[8],
                value_hour=row[9],
                number_hour=row[10],
                total_payment=row[11],
                payment_frequency=row[12],
            )
        )
    return contratos

def actualizar_contrato(contrato_id, contrato_data, applied_date=None):
    """
    Actualiza campos principales sólo si vienen presentes en contrato_data (no sobrescribe con None).
    Inserta registros de historial sólo si hay cambio respecto al último registro.
    applied_date: string ya normalizado (YYYY-MM-DD) o None -> hoy.
    """
    conn = conectar()
    cursor = conn.cursor()

    contrato_original = obtener_contrato_por_id(contrato_id)
    if not contrato_original:
        conn.close()
        raise ValueError("Contrato no encontrado.")

    try:
        cursor.execute("BEGIN TRANSACTION;")

        # Construir UPDATE dinámico sólo con campos no-None
        set_clauses = []
        params = []
        fields = [
            ('employee_id', contrato_data.employee_id),
            ('type_contract', contrato_data.type_contract),
            ('start_date', contrato_data.start_date),
            ('end_date', contrato_data.end_date),
            ('state', contrato_data.state),
            ('contractor', contrato_data.contractor),
            ('total_payment', contrato_data.total_payment),
            ('payment_frequency', contrato_data.payment_frequency),
        ]
        for col, value in fields:
            if value is not None:
                set_clauses.append(f"{col} = ?")
                params.append(value)

        if set_clauses:
            sql = "UPDATE contracts SET " + ", ".join(set_clauses) + " WHERE id = ?"
            params.append(contrato_id)
            cursor.execute(sql, tuple(params))

        # obtener últimos historiales actuales
        cursor.execute("SELECT monthly_payment, transport FROM salary_history WHERE contract_id = ? ORDER BY effective_date DESC LIMIT 1", (contrato_id,))
        last_salary = cursor.fetchone() or (None, None)
        last_monthly, last_transport = last_salary[0], last_salary[1]

        cursor.execute("SELECT value_hour, number_hour FROM hourly_history WHERE contract_id = ? ORDER BY effective_date DESC LIMIT 1", (contrato_id,))
        last_hourly = cursor.fetchone() or (None, None)
        last_value_hour, last_number_hour = last_hourly[0], last_hourly[1]

        cursor.execute("SELECT old_total_payment, new_total_payment, old_payment_frequency, new_payment_frequency FROM service_order_history WHERE contract_id = ? ORDER BY effective_date DESC LIMIT 1", (contrato_id,))
        last_soh = cursor.fetchone() or (None, None, None, None)
        _, last_new_total, _, last_new_freq = last_soh

        # fecha efectiva
        eff_str = applied_date if applied_date else datetime.now().strftime('%Y-%m-%d')

        # insertar historiales sólo si hay cambios explícitos en contrato_data (y no son None)
        if contrato_data.type_contract in ['CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO',
                                           'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO',
                                           'CONTRATO APRENDIZAJE SENA']:
            if (hasattr(contrato_data, 'monthly_payment') and contrato_data.monthly_payment is not None and contrato_data.monthly_payment != last_monthly) or \
               (hasattr(contrato_data, 'transport') and contrato_data.transport is not None and contrato_data.transport != last_transport):
                cursor.execute("""
                    INSERT INTO salary_history (contract_id, monthly_payment, transport, effective_date)
                    VALUES (?, ?, ?, ?)
                """, (contrato_id, contrato_data.monthly_payment, contrato_data.transport, eff_str))

        elif contrato_data.type_contract == 'CONTRATO SERVICIO HORA CATEDRA':
            if (hasattr(contrato_data, 'value_hour') and contrato_data.value_hour is not None and contrato_data.value_hour != last_value_hour) or \
               (hasattr(contrato_data, 'number_hour') and contrato_data.number_hour is not None and contrato_data.number_hour != last_number_hour):
                cursor.execute("""
                    INSERT INTO hourly_history (contract_id, value_hour, number_hour, effective_date)
                    VALUES (?, ?, ?, ?)
                """, (contrato_id, contrato_data.value_hour, contrato_data.number_hour, eff_str))

        elif contrato_data.type_contract == 'ORDEN PRESTACION DE SERVICIOS':
            # Normalizar y comparar como strings para evitar diferencias de tipo
            new_total = getattr(contrato_data, 'total_payment', None)
            new_freq = getattr(contrato_data, 'payment_frequency', None)

            last_new_total_str = "" if last_new_total is None else str(last_new_total)
            last_new_freq_str = "" if last_new_freq is None else str(last_new_freq)
            new_total_str = "" if new_total is None else str(new_total)
            new_freq_str = "" if new_freq is None else str(new_freq)

            if (new_total is not None and new_total_str != last_new_total_str) or \
               (new_freq is not None and new_freq_str != last_new_freq_str):
                old_total = last_new_total if last_new_total is not None else contrato_original[8]
                old_freq = last_new_freq if last_new_freq is not None else contrato_original[9]
                cursor.execute("""
                    INSERT INTO service_order_history (contract_id, old_total_payment, new_total_payment, old_payment_frequency, new_payment_frequency, effective_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (contrato_id, old_total, new_total, old_freq, new_freq, eff_str))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
def actualizar_pago_contrato(contrato_id, datos_pago_dict, fecha_efectiva):
    """
    Wrapper para compatibilidad: construye un objeto Contrato con los campos de pago
    y delega en actualizar_contrato(...) usando fecha_efectiva como applied_date.
    Devuelve True si la operación se ejecutó sin errores.
    """
    contrato = obtener_contrato_por_id(contrato_id)
    if not contrato:
        raise ValueError("Contrato no encontrado.")

    type_contract = contrato[3]  # índice según obtener_contrato_por_id

    # Construir Contrato mínimo con sólo campos relevantes
    contrato_obj = Contrato(
        id=contrato_id,
        employee_id=contrato[1],
        type_contract=type_contract,
        # dejar otros campos como None por defecto
    )

    if type_contract in ['CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO',
                         'CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO',
                         'CONTRATO APRENDIZAJE SENA']:
        contrato_obj.monthly_payment = datos_pago_dict.get('monthly_payment')
        contrato_obj.transport = datos_pago_dict.get('transport')

    elif type_contract == 'CONTRATO SERVICIO HORA CATEDRA':
        contrato_obj.value_hour = datos_pago_dict.get('value_hour')
        contrato_obj.number_hour = datos_pago_dict.get('number_hour')

    elif type_contract == 'ORDEN PRESTACION DE SERVICIOS':
        # aceptar ambas claves
        contrato_obj.total_payment = datos_pago_dict.get('new_total_payment') if datos_pago_dict.get('new_total_payment') is not None else datos_pago_dict.get('total_payment')
        contrato_obj.payment_frequency = datos_pago_dict.get('new_payment_frequency') if datos_pago_dict.get('new_payment_frequency') is not None else datos_pago_dict.get('payment_frequency')

    else:
        raise ValueError("Tipo de contrato no soportado para modificar pago.")

    # fecha_efectiva ya normalizada por la vista según dijiste
    actualizar_contrato(contrato_id, contrato_obj, applied_date=fecha_efectiva)
    return True

def obtener_historial_pagos(contrato_id):
    conn = conectar()
    cursor = conn.cursor()
    result = {}
    cursor.execute("SELECT monthly_payment, transport, effective_date FROM salary_history WHERE contract_id = ? ORDER BY effective_date DESC", (contrato_id,))
    rows = cursor.fetchall()
    result['salary_history'] = [{'monthly_payment': r[0], 'transport': r[1], 'effective_date': r[2]} for r in rows]

    cursor.execute("SELECT value_hour, number_hour, effective_date FROM hourly_history WHERE contract_id = ? ORDER BY effective_date DESC", (contrato_id,))
    rows = cursor.fetchall()
    result['hourly_history'] = [{'value_hour': r[0], 'number_hour': r[1], 'effective_date': r[2]} for r in rows]

    cursor.execute("SELECT old_total_payment, new_total_payment, old_payment_frequency, new_payment_frequency, effective_date FROM service_order_history WHERE contract_id = ? ORDER BY effective_date DESC", (contrato_id,))
    rows = cursor.fetchall()
    result['service_order_history'] = [{'old_total_payment': r[0], 'new_total_payment': r[1], 'old_payment_frequency': r[2], 'new_payment_frequency': r[3], 'effective_date': r[4]} for r in rows]

    conn.close()
    return result
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
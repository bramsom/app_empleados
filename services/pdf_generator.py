import sqlite3
from bd.connection import conectar
from datetime import datetime

def obtener_periodo_laborado(employee_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MIN(start_date), MAX(end_date)
        FROM contracts
        WHERE employee_id = ?
    """, (employee_id,))
    resultado = cursor.fetchone()
    conn.close()
    fecha_inicio, fecha_fin = resultado
    if fecha_fin is None:
        fecha_fin = datetime.today().strftime("%Y-%m-%d")
    return fecha_inicio, fecha_fin

def calcular_tiempo_laborado(fecha_inicio, fecha_fin):
    # Detecta el formato de fecha automáticamente
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            inicio = datetime.strptime(fecha_inicio, fmt)
            fin = datetime.strptime(fecha_fin, fmt)
            break
        except ValueError:
            continue
    else:
        raise ValueError("Formato de fecha no soportado.")
    diferencia = fin - inicio
    años = diferencia.days // 365
    meses = (diferencia.days % 365) // 30
    dias = (diferencia.days % 365) % 30
    return f"{años} años, {meses} meses, {dias} días"
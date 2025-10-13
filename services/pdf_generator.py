import sqlite3
from bd.connection import conectar
from datetime import datetime
import os
from utils.pdf_layout import CertPDF, _safe_text, prepare_header_info

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
    """
    Calcula una representación 'X años, Y meses, Z días' entre fecha_inicio y fecha_fin.
    Acepta strings en varios formatos o objetos datetime. Si fecha_fin es None usa hoy.
    Si no puede parsear fecha_inicio devuelve '0 años, 0 meses, 0 días' (no lanza excepción).
    """
    inicio = _parse_date(fecha_inicio)
    fin = _parse_date(fecha_fin) or datetime.today()

    if inicio is None:
        return "0 años, 0 meses, 0 días"

    diferencia = fin - inicio
    años = diferencia.days // 365
    meses = (diferencia.days % 365) // 30
    dias = (diferencia.days % 365) % 30
    return f"{años} años, {meses} meses, {dias} días"

def _parse_date(val):
    if val is None:
        return None
    if isinstance(val, datetime):
        return val
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(val, fmt)
        except Exception:
            continue
    try:
        return datetime.fromisoformat(val)
    except Exception:
        return None

def _format_date_for_print(val):
    d = _parse_date(val)
    return d.strftime("%d/%m/%Y") if d else ""

def _format_money(val):
    try:
        v = float(val)
        s = f"{v:,.0f}"
        return "$ " + s.replace(",", ".")
    except Exception:
        return ""

def _format_fecha_spanish(val):
    """
    Acepta datetime u object convertible a fecha (usa _parse_date).
    Devuelve '13 de octubre de 2025' (mes en español, en minúscula).
    """
    d = val if isinstance(val, datetime) else _parse_date(val)
    if not d:
        return ""
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
             "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    return f"{d.day} de {meses[d.month - 1]} de {d.year}"

# Añadir clase con footer personalizado y header configurable
def generar_certificado_contratos(emp, contratos, ruta_salida,
                                  entidad_nombre="COLEGIO CIUDAD DE PIENDAMÓ",
                                  nit="NIT.817001256-7",
                                  representante="EDGAR ALFONSO PAJA FLOR",
                                  fecha_expedicion=None):
    """
    Genera un PDF con el enunciado que menciona las labores del último contrato
    y a continuación una tabla listando todos los contratos del empleado.
    emp: dict o objeto con al menos name, last_name, document_number, position, id
    contratos: lista de dicts/objetos/tuplas con start_date, end_date, monthly_payment, type_contract, position (opcional)
    ruta_salida: ruta .pdf donde guardar
    """
    if fecha_expedicion is None:
        fecha_expedicion = _format_fecha_spanish(datetime.now())

    def to_dict(c):
        if isinstance(c, dict):
            return c
        if hasattr(c, "__dict__"):
            return {k: v for k, v in c.__dict__.items() if not k.startswith("_")}
        if isinstance(c, (list, tuple)):
            # No hay metadatos de columnas: intentar mapear posiciones comunes
            keys = ["id","employee_id","type_contract","start_date","end_date","state",
                    "contractor","total_payment","payment_frequency","monthly_payment",
                    "transport","value_hour","number_hour","position"]
            return {keys[i]: c[i] for i in range(min(len(c), len(keys)))}
        return dict(c)

    contratos_norm = [to_dict(c) for c in contratos]
    for c in contratos_norm:
        c["_start_parsed"] = _parse_date(c.get("start_date") or c.get("start") or c.get("start_date"))
    contratos_norm.sort(key=lambda x: x.get("_start_parsed") or datetime.min, reverse=True)
    ultimo = contratos_norm[0] if contratos_norm else {}

    if isinstance(emp, dict):
        nombre_completo = f"{emp.get('name','').strip()} {emp.get('last_name','').strip()}".strip()
        documento = emp.get("document_number","")
        posicion_emp = emp.get("position","")
    else:
        nombre_completo = f"{getattr(emp,'name','').strip()} {getattr(emp,'last_name','').strip()}".strip()
        documento = getattr(emp, "document_number", "")
        posicion_emp = getattr(emp, "position", "")

    labores = ultimo.get("position") or ultimo.get("cargo") or posicion_emp or ""

    # reunir todos los cargos de los contratos (preservando orden y eliminando duplicados)
    cargos_raw = []
    for c in contratos_norm:
        pos = (c.get("position") or c.get("cargo") or "").strip()
        if pos:
            cargos_raw.append(pos)
    # añadir cargo actual/registro del empleado como fallback (al final)
    if posicion_emp and posicion_emp.strip() and posicion_emp.strip() not in cargos_raw:
        cargos_raw.append(posicion_emp.strip())

    # eliminar duplicados preservando orden
    seen = set()
    cargos = []
    for p in cargos_raw:
        if p and p not in seen:
            seen.add(p)
            cargos.append(p)

    # construir texto legible para el párrafo
    if not cargos:
        labores_text = ""
    elif len(cargos) == 1:
        labores_text = f"como {cargos[0]}"
    else:
        # juntar con comas y "y" antes del último
        if len(cargos) <= 3:
            joined = ", ".join(cargos[:-1]) + " y " + cargos[-1]
        else:
            # si hay muchos, mostrar los primeros 3 y "etc."
            joined = ", ".join(cargos[:3]) + ", etc."
        labores_text = f"desempeñando los cargos de {joined}"

    # usar la clase con footer
    # resolver ruta del proyecto
    script_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    # márgenes (ejemplo) -> definir antes de usarlos
    left_margin = 20
    right_margin = 20
    top_margin = 20

    # crear PDF en tamaño Letter (8.5"x11")
    pdf = CertPDF(orientation='P', unit='mm', format='letter')

    # preparar header_info (prepare_header_info debe devolver las claves esperadas)
    pdf.header_info = prepare_header_info(
        project_root,
        entidad_nombre=entidad_nombre,
        nit=" ",
        contacto="Web: www.ccp.com.co - Email: colecipi@hotmail.com - Tel: 3146233137 - Cll. 2 No. 4-80 Barrio San Cayetano",
        logo_left_name="logo_institucional.png",
        logo_right_name="logo_fundacion.png",
        watermark_name="watermark.png",
        watermark_opacity=0.12,
        watermark_scale=0.95,
        separator_name="separator.png",
        separator_scale=0.95
    )
    # pasar project_root dentro de header_info por si lo necesita el header/footer
    pdf.header_info["_project_root"] = project_root

    # aplicar márgenes al PDF (ahora que están definidos)
    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)
    pdf.set_top_margin(top_margin)

    # calcular ancho util y forzar el ancho del separador (header + footer)
    util_width = pdf.w - pdf.l_margin - pdf.r_margin
    pdf.header_info["separator_width_mm"] = util_width * 0.95  # 95% del ancho util
    pdf.header_info["separator_scale"] = 0.95

    # añadir la primera página (ejecuta header)
    pdf.add_page()
    # si prepare_header_info no expone project_root, pasarlo manualmente para resolver ruta interna
    pdf.header_info["_project_root"] = project_root

    # Debug temporal eliminado: se quitaron los prints que mostraban rutas y metadatos de imagen.
    
    # Márgenes: ajustar según prefieras (en mm). Aquí 20mm a izquierda/derecha/arriba.
    left_margin = 20
    right_margin = 20
    top_margin = 20
    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)
    pdf.set_top_margin(top_margin)
    # No volver a llamar add_page con 'format' — ya se añadió la página antes para ejecutar header()
    # pdf.add_page(format='letter')  # añade página Letter (opcional)
    # Auto page break mantiene el margen inferior (15 por defecto) o puedes ajustarlo:
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 6, _safe_text(entidad_nombre), ln=True, align="C")
    pdf.set_font("Arial","B", size=10)
    pdf.cell(0, 6, _safe_text(nit), ln=True, align="C")
    pdf.ln(8)

  # Centrar el texto del representante, NIT y el título "CERTIFICA"
    pdf.multi_cell(0, 6, _safe_text("El Representante Legal del " + entidad_nombre + ","), align="C")
    pdf.ln(2)
    pdf.set_font("Arial","B", size=10)
    pdf.ln(4)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, _safe_text("C E R T I F I C A:"), ln=True, align="C")
    pdf.ln(6)
    pdf.set_font("Arial", size=11)

    # construir intro de forma segura (usar concatenación explícita)
    intro = (
        f"Que, {nombre_completo}, titular de la cédula de ciudadanía número {documento}, "
        + (f"prestó sus servicios {labores_text} " if labores_text else "prestó sus servicios ")
        + "en los siguientes períodos y bajo los siguientes contratos:"
    )
    pdf.multi_cell(0, 6, _safe_text(intro))
    pdf.ln(6)

    pdf.set_font("Arial", "B", 10)
    # Ajustes: tamaños y espaciado más compactos
    base_col_w = [30, 30, 40, 30, 60]  # anchos base (última columna más ancha para CARGO)
    # ancho interior de la página (considera márgenes ya definidos)
    page_inner_width = pdf.w - pdf.l_margin - pdf.r_margin
    table_width = sum(base_col_w)
    scale = min(1.0, page_inner_width / table_width)
    col_w = [w * scale for w in base_col_w]

    # Centrar la tabla horizontalmente
    start_x = pdf.l_margin + max(0, (page_inner_width - sum(col_w)) / 2)

    # Cabecera compacta
    pdf.set_font("Arial", "B", 8)
    headers = ["FECHA INICIO", "FECHA FINAL", "SAL. MENSUAL", "TIPO CONT.", "CARGO"]
    pdf.set_x(start_x)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 6, h, border=0, align="C")
    pdf.ln(6)
    # Reducir tamaño de fuente y alto de fila para las filas de contratos
    pdf.set_font("Arial", size=8)
    row_h = 5

    # mapa de siglas/meanings (mismo que en type_reports.py)
    contract_type_map = {
        "CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO": ("C.I.T.T.F", "Contrato Individual de Trabajo a Término Fijo"),
        "CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO": ("C.I.T.T.I", "Contrato Individual de Trabajo a Término Indefinido"),
        "CONTRATO SERVICIO HORA CATEDRA": ("C.S.H.C", "Contrato de Prestación de Servicios - Hora Cátedra"),
        "CONTRATO APRENDIZAJE SENA": ("C.A.S", "Contrato de Aprendizaje SENA"),
        "ORDEN PRESTACION DE SERVICIOS": ("O.P.S", "Orden de Prestación de Servicios")
    }

    # crear lista de siglas usadas
    siglas_usadas = {}
    for c in contratos_norm:
        full = c.get("type_contract") or c.get("type") or ""
        sig, meaning = contract_type_map.get(full, (full, ""))
        c["_type_sigla"] = sig
        if sig and sig not in siglas_usadas:
            siglas_usadas[sig] = meaning

    # fecha a usar cuando un contrato no tiene end_date o es indefinido
    fecha_actual_dt = _parse_date(fecha_expedicion) or datetime.today()

    # Filas compactas, usando start_x para mantener centrado
    for c in reversed(contratos_norm):
        start = _format_date_for_print(c.get("start_date") or c.get("start") or c.get("_start_parsed"))
        # determinar fecha final: si no existe o el contrato es indefinido usar fecha_actual_dt
        raw_end = c.get("end_date") or c.get("end")
        tipo_full = (c.get("type_contract") or c.get("type") or "").upper()
        is_indefinido = "INDEFINIDO" in tipo_full  # detecta contratos indefinidos por palabra clave
        end_val = raw_end if raw_end and not is_indefinido else fecha_actual_dt
        end = _format_date_for_print(end_val)
        sal = _format_money(c.get("monthly_payment") or c.get("monthly") or c.get("total_payment"))
        tipo = str(c.get("_type_sigla") or "")
        # Fallback: usar cargo del empleado si no está en el contrato
        cargo = (
            c.get("position")
            or c.get("cargo")
            or (emp.get("position") if isinstance(emp, dict) else getattr(emp, "position", ""))
            or ""
        )
        pdf.set_x(start_x)
        pdf.cell(col_w[0], row_h, start, border=0, align="C")
        pdf.cell(col_w[1], row_h, end, border=0, align="C")
        # Alineación de salario: derecha o centrada según prefieras ("R" o "C")
        pdf.cell(col_w[2], row_h, sal, border=0, align="C")
        pdf.cell(col_w[3], row_h, tipo[:20], border=0, align="C")
        # Ajustar cargo (recorta si es demasiado largo)
        # usar get_string_width si quieres recortar inteligentemente, aquí recortamos por caracteres
        max_chars = max(10, int(col_w[4] / 2))
        pdf.cell(col_w[4], row_h, cargo[:max_chars], border=0, align="C")
        pdf.ln(row_h)

    pdf.ln(8)

    # Imprimir leyenda: siglas y significado en cursiva y entre paréntesis
    if siglas_usadas:
        pdf.set_font("Arial", "I", 8)
        leyenda_line_h = 4
        for sig, meaning in siglas_usadas.items():
            line = f"({sig}) {meaning}" if meaning else f"({sig})"
            pdf.multi_cell(0, leyenda_line_h, _safe_text(line), align="L")
        pdf.ln(4)
        pdf.set_font("Arial", size=11)

    pdf.multi_cell(0, 6, _safe_text(f"Se expide a solicitud de la persona interesada.\nDado en Piendamó Cauca, el día {fecha_expedicion}."))
    pdf.ln(20)
    
    pdf.ln(12)
    # Usar fuente en negrilla para firma y título, centrados
    pdf.set_font("Arial", "B", 11)
    # cell width 0 con align='C' centra en el ancho util (considera los márgenes)
    pdf.cell(0, 6, _safe_text(representante), ln=True, align="C")
    pdf.ln(4)
    pdf.cell(0, 6, _safe_text("Representante Legal"), ln=True, align="C")
    # volver a fuente normal si se necesita más texto después
    pdf.set_font("Arial", size=11)

    pdf.output(ruta_salida)
    return ruta_salida
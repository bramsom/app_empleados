import sqlite3
from bd.connection import conectar
from datetime import datetime
from fpdf import FPDF

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

# Añadir clase con footer personalizado
class CertPDF(FPDF):
    def footer(self):
        # posición a 15mm del final
        self.set_y(-15)
        # línea separadora opcional
        # self.set_draw_color(200,200,200)
        # self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        # Pie de página: texto pequeño, cursiva ligera y centrado
        self.set_font("Arial", "I", 8)
        self.set_text_color(100, 100, 100)
        footer_text = "Web: www.ccp.com.co - Email: colecipi@hotmail.com – Teléfono: 3146233137 - Dirección: Cll. 2 No. 4-80 Barrio San Cayetano"
        # cell ancho 0 para usar el ancho util y centrar
        self.cell(0, 6, footer_text, ln=0, align="C")

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
        fecha_expedicion = datetime.now().strftime("%d de %B %Y")

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

    # usar la clase con footer
    pdf = CertPDF()
    # Márgenes: ajustar según prefieras (en mm). Aquí 20mm a izquierda/derecha/arriba.
    left_margin = 20
    right_margin = 20
    top_margin = 20
    pdf.set_left_margin(left_margin)
    pdf.set_right_margin(right_margin)
    pdf.set_top_margin(top_margin)
    pdf.add_page()
    # Auto page break mantiene el margen inferior (15 por defecto) o puedes ajustarlo:
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 6, entidad_nombre, ln=True, align="C")
    pdf.set_font("Arial","B", size=10)
    pdf.cell(0, 6, nit, ln=True, align="C")
    pdf.ln(8)

  # Centrar el texto del representante, NIT y el título "CERTIFICA"
    pdf.multi_cell(0, 6, "El Representante Legal del " + entidad_nombre + ",", align="C")
    pdf.ln(2)
    pdf.set_font("Arial","B", size=10)
    pdf.ln(4)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, "C E R T I F I C A:", ln=True, align="C")
    pdf.ln(6)
    pdf.set_font("Arial", size=11)

    intro = (
        f"Que, {nombre_completo}, identificada con la cédula de ciudadanía número "
        f"{documento}, prestó sus servicios como {labores} en los siguientes períodos y bajo los siguientes contratos:"
    )
    pdf.multi_cell(0, 6, intro)
    pdf.ln(6)

    pdf.set_font("Arial", "B", 10)
    # Ajustes: tamaños y espaciado más compactos
    base_col_w = [30, 30, 40, 30, 50]  # anchos base (última columna más ancha para CARGO)
    # ancho interior de la página (considera márgenes ya definidos)
    page_inner_width = pdf.w - pdf.l_margin - pdf.r_margin
    table_width = sum(base_col_w)
    scale = min(1.0, page_inner_width / table_width)
    col_w = [w * scale for w in base_col_w]

    # Centrar la tabla horizontalmente
    start_x = pdf.l_margin + max(0, (page_inner_width - sum(col_w)) / 2)

    # Cabecera compacta
    pdf.set_font("Arial", "B", 9)
    headers = ["FECHA INIC", "FECHA FINAL", "SAL. MENSUAL", "TIPO CONT.", "CARGO"]
    pdf.set_x(start_x)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 6, h, border=0, align="C")
    pdf.ln(6)
    pdf.set_font("Arial", size=9)

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
        pdf.cell(col_w[0], 6, start, border=0, align="C")
        pdf.cell(col_w[1], 6, end, border=0, align="C")
        # Alineación de salario: derecha o centrada según prefieras ("R" o "C")
        pdf.cell(col_w[2], 6, sal, border=0, align="C")
        pdf.cell(col_w[3], 6, tipo[:20], border=0, align="C")
        # Ajustar cargo (recorta si es demasiado largo)
        pdf.cell(col_w[4], 6, cargo[: int(col_w[4] / 2)], border=0, align="C")
        pdf.ln(6)

    pdf.ln(8)

    # Imprimir leyenda: siglas y significado en cursiva y entre paréntesis
    if siglas_usadas:
        pdf.set_font("Arial", "I", 10)
        for sig, meaning in siglas_usadas.items():
            line = f"({sig}) {meaning}" if meaning else f"({sig})"
            pdf.multi_cell(0, 6, line)
        pdf.ln(6)
        pdf.set_font("Arial", size=11)

    pdf.multi_cell(0, 6, f"Se expide a solicitud de la persona interesada.\nDado en Piendamó Cauca,el dia {fecha_expedicion}.")
    pdf.ln(20)

    # reemplazar bloque de firma actual por uno centrado y en negrilla
    #    pdf.cell(0, 6, representante, ln=True)
    #    pdf.cell(0, 6, "Representante Legal", ln=True)
    # Espacio antes de la firma
    pdf.ln(12)
    # Usar fuente en negrilla para firma y título, centrados
    pdf.set_font("Arial", "B", 11)
    # cell width 0 con align='C' centra en el ancho util (considera los márgenes)
    pdf.cell(0, 6, representante, ln=True, align="C")
    pdf.ln(4)
    pdf.cell(0, 6, "Representante Legal", ln=True, align="C")
    # volver a fuente normal si se necesita más texto después
    pdf.set_font("Arial", size=11)

    pdf.output(ruta_salida)
    return ruta_salida
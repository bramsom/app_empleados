import sqlite3
from bd.connection import conectar
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
import os

# usar los helpers centralizados
from utils.pdf_helpers import (
    _parse_date,
    _format_date_for_print,
    _format_money,
    _to_dict,
    normalize_contracts,
    periodo_y_tipos,
    construir_labores_text,
)

from utils.pdf_layout import CertPDF, _safe_text, prepare_header_info

# Funciones reexportadas usadas por controllers/report_controller.py
def obtener_periodo_laborado(employee_id):
    """Devuelve (fecha_inicio, fecha_fin). Si no hay fecha_fin devuelve hoy como string."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT MIN(start_date), MAX(end_date)
        FROM contracts
        WHERE employee_id = ?
    """, (employee_id,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        fecha_inicio, fecha_fin = resultado
    else:
        fecha_inicio, fecha_fin = (None, None)
    if fecha_fin is None:
        fecha_fin = datetime.today().strftime("%Y-%m-%d")
    return fecha_inicio, fecha_fin

def calcular_tiempo_laborado(fecha_inicio, fecha_fin):
    inicio = _parse_date(fecha_inicio)
    fin = _parse_date(fecha_fin) or datetime.today()
    if inicio is None:
        return "0 años, 0 meses, 0 días"
    diferencia = fin - inicio
    años = diferencia.days // 365
    meses = (diferencia.days % 365) // 30
    dias = (diferencia.days % 365) % 30
    return f"{años} años, {meses} meses, {dias} días"

# ---------- Impresores de secciones ----------
def _imprimir_intro(pdf: CertPDF, nombre_completo: str, documento: str, labores_text: str,
                    fecha_inicio_str: str, fecha_fin_str: str, tipos_text: str, show_table: bool):
    if show_table:
        intro = (
            f"Que, {nombre_completo}, titular de la cédula de ciudadanía número {documento}, "
            + (f"prestó sus servicios {labores_text} " if labores_text else "prestó sus servicios ")
            + "en los siguientes períodos y bajo los siguientes contratos:"
        )
    else:
        tipo_fragment = f" bajo contrato(s) de tipo {tipos_text}" if tipos_text else ""
        periodo_fragment = ""
        if fecha_inicio_str or fecha_fin_str:
            periodo_fragment = f" desde {fecha_inicio_str} hasta {fecha_fin_str}"
        intro = (
            f"Que, {nombre_completo}, titular de la cédula de ciudadanía número {documento}, "
            f"prestó sus servicios{periodo_fragment}{tipo_fragment}, realizando las siguientes labores:"
        )
    pdf.multi_cell(0, 6, _safe_text(intro))
    pdf.ln(6)

def _print_labores_descripcion(pdf: CertPDF, labores_descripcion: Optional[str]):
    if labores_descripcion:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, _safe_text("Descripción de las labores realizadas:"), ln=True)
        pdf.set_font("Arial", "", 10)
        for line in str(labores_descripcion).splitlines():
            pdf.multi_cell(0, 5, _safe_text(line))
        pdf.ln(4)

def _prepare_table_layout(pdf: CertPDF, include_pago: bool) -> Tuple[List[float], List[str], float]:
    if include_pago:
        base_col_w = [30, 30, 40, 30, 60]
        headers = ["FECHA INICIO", "FECHA FINAL", "SAL. MENSUAL", "TIPO CONT.", "CARGO"]
    else:
        base_col_w = [30, 40, 30, 60]
        headers = ["FECHA INICIO", "FECHA FINAL", "TIPO CONT.", "CARGO"]
    page_inner_width = pdf.w - pdf.l_margin - pdf.r_margin
    table_width = sum(base_col_w)
    scale = min(1.0, page_inner_width / table_width)
    col_w = [w * scale for w in base_col_w]
    start_x = pdf.l_margin + max(0, (page_inner_width - sum(col_w)) / 2)
    return col_w, headers, start_x

def _print_table_header(pdf: CertPDF, headers: List[str], col_w: List[float], start_x: float):
    pdf.set_font("Arial", "B", 8)
    pdf.set_x(start_x)
    for i, h in enumerate(headers):
        pdf.cell(col_w[i], 6, h, border=0, align="C")
    pdf.ln(6)
    pdf.set_font("Arial", size=8)

def _print_table_rows(pdf: CertPDF, contratos_norm: List[Dict[str, Any]], emp: Dict[str, Any],
                      col_w: List[float], start_x: float, include_pago: bool):
    row_h = 5
    for c in reversed(contratos_norm):
        start = _format_date_for_print(c.get("start_date") or c.get("start") or c.get("_start_parsed"))
        raw_end = c.get("end_date") or c.get("end")
        tipo_full = (c.get("type_contract") or c.get("type") or "").upper()
        is_indefinido = "INDEFINIDO" in tipo_full
        fecha_actual_dt = datetime.today()
        end_val = raw_end if raw_end and not is_indefinido else fecha_actual_dt
        end = _format_date_for_print(end_val)
        sal = _format_money(c.get("monthly_payment") or c.get("monthly") or c.get("total_payment"))
        tipo = str(c.get("_type_sigla") or "")
        cargo = (
            c.get("position")
            or c.get("cargo")
            or (emp.get("position") if isinstance(emp, dict) else getattr(emp, "position", ""))
            or ""
        )
        pdf.set_x(start_x)
        if include_pago:
            cells = [start, end, sal, tipo[:20], cargo[:max(10, int(col_w[-1] / 2))]]
        else:
            cells = [start, end, tipo[:20], cargo[:max(10, int(col_w[-1] / 2))]]
        for text, w in zip(cells, col_w):
            pdf.cell(w, row_h, _safe_text(text), border=0, align="C")
        pdf.ln(row_h)

# ---------- Función principal (más limpia) ----------
def generar_certificado_contratos(emp: Any, contratos: List[Any], ruta_salida: str,
                                  entidad_nombre: str = "COLEGIO CIUDAD DE PIENDAMÓ",
                                  nit: str = "NIT.817001256-7",
                                  representante: str = "EDGAR ALFONSO PAJA FLOR",
                                  representante_titulo: str = "Representante Legal",
                                   fecha_expedicion: Optional[str] = None,
                                   include_pago: bool = True,
                                   labores_descripcion: Optional[str] = None,
                                   show_table: bool = True) -> str:
    if fecha_expedicion is None:
        fecha_expedicion = _format_date_for_print(datetime.now())

    contratos_norm = normalize_contracts(contratos)
    ultimo = contratos_norm[0] if contratos_norm else {}

    if isinstance(emp, dict):
        nombre_completo = f"{emp.get('name','').strip()} {emp.get('last_name','').strip()}".strip()
        documento = emp.get("document_number","")
        posicion_emp = emp.get("position","")
    else:
        nombre_completo = f"{getattr(emp,'name','').strip()} {getattr(emp,'last_name','').strip()}".strip()
        documento = getattr(emp, "document_number", "")
        posicion_emp = getattr(emp, "position", "")

    labores_text = construir_labores_text(posicion_emp, contratos_norm)

    # periodo y tipos para el modo "solo descripción"
    fecha_inicio_dt, fecha_fin_dt, tipos_text = periodo_y_tipos(contratos_norm)
    fecha_inicio_str = _format_date_for_print(fecha_inicio_dt) if fecha_inicio_dt else ""
    fecha_fin_str = _format_date_for_print(fecha_fin_dt) if fecha_fin_dt else ""

    # preparar PDF y header
    script_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    pdf = CertPDF(orientation='P', unit='mm', format='letter')
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
    pdf.header_info["_project_root"] = project_root
    pdf.set_left_margin(20); pdf.set_right_margin(20); pdf.set_top_margin(20)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 6, _safe_text(entidad_nombre), ln=True, align="C")
    pdf.set_font("Arial","B", size=10)
    pdf.cell(0, 6, _safe_text(nit), ln=True, align="C")
    pdf.ln(8)
    pdf.multi_cell(0, 6, _safe_text("El Representante Legal del " + entidad_nombre + ","), align="C")
    pdf.ln(4)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, _safe_text("C E R T I F I C A:"), ln=True, align="C")
    pdf.ln(6)
    pdf.set_font("Arial", size=11)

    # intro y descripción
    _imprimir_intro(pdf, nombre_completo, documento, labores_text, fecha_inicio_str, fecha_fin_str, tipos_text, show_table)
    _print_labores_descripcion(pdf, labores_descripcion)

    # si no hay tabla, imprimir footer y terminar
    if not show_table:
        pdf.ln(8)
        pdf.multi_cell(0, 6, _safe_text(f"Se expide a solicitud de la persona interesada.\nDado en Piendamó Cauca, el día {fecha_expedicion}."))
        pdf.ln(20)
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, _safe_text(representante), ln=True, align="C")
        pdf.ln(4)
        pdf.cell(0, 6, _safe_text(representante_titulo), ln=True, align="C")
        pdf.set_font("Arial", size=11)
        pdf.output(ruta_salida)
        return ruta_salida

    # preparar y escribir tabla (solo si show_table True)
    col_w, headers, start_x = _prepare_table_layout(pdf, include_pago)
    _print_table_header(pdf, headers, col_w, start_x)

    # preparar siglas
    contract_type_map = {
        "CONTRATO INDIVIDUAL DE TRABAJO TERMINO FIJO": ("C.I.T.T.F", "Contrato Individual de Trabajo a Término Fijo"),
        "CONTRATO INDIVIDUAL DE TRABAJO TERMINO INDEFINIDO": ("C.I.T.T.I", "Contrato Individual de Trabajo a Término Indefinido"),
        "CONTRATO SERVICIO HORA CATEDRA": ("C.S.H.C", "Contrato de Prestación de Servicios - Hora Cátedra"),
        "CONTRATO APRENDIZAJE SENA": ("C.A.S", "Contrato de Aprendizaje SENA"),
        "ORDEN PRESTACION DE SERVICIOS": ("O.P.S", "Orden de Prestación de Servicios")
    }
    siglas_usadas = {}
    for c in contratos_norm:
        full = c.get("type_contract") or c.get("type") or ""
        sig, meaning = contract_type_map.get(full, (full, ""))
        c["_type_sigla"] = sig
        if sig and sig not in siglas_usadas:
            siglas_usadas[sig] = meaning

    _print_table_rows(pdf, contratos_norm, emp if isinstance(emp, dict) else {}, col_w, start_x, include_pago)

    if siglas_usadas:
        pdf.set_font("Arial", "I", 8)
        for sig, meaning in siglas_usadas.items():
            line = f"({sig}) {meaning}" if meaning else f"({sig})"
            pdf.multi_cell(0, 4, _safe_text(line), align="L")
        pdf.ln(4)
        pdf.set_font("Arial", size=11)

    # footer / firma (usar representante_titulo en vez de cadena fija)
    pdf.multi_cell(0, 6, _safe_text(f"Se expide a solicitud de la persona interesada.\nDado en Piendamó Cauca, el día {fecha_expedicion}."))
    pdf.ln(20)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, _safe_text(representante), ln=True, align="C")
    pdf.ln(4)
    pdf.cell(0, 6, _safe_text(representante_titulo), ln=True, align="C")
    pdf.set_font("Arial", size=11)

    pdf.output(ruta_salida)
    return ruta_salida
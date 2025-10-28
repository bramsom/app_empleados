from datetime import datetime
from typing import Any, List, Dict, Optional, Tuple

def _parse_date(val: Any) -> Optional[datetime]:
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

def format_date_for_print(val: Any) -> str:
    d = _parse_date(val)
    return d.strftime("%d/%m/%Y") if d else ""

def _format_date_for_print(val: Any) -> str:
    # alias interno para compatibilidad con nombre anterior
    return format_date_for_print(val)

def _format_money(val: Any) -> str:
    try:
        v = float(val)
        s = f"{v:,.0f}"
        return "$ " + s.replace(",", ".")
    except Exception:
        return ""

def _to_dict(c: Any) -> Dict[str, Any]:
    if isinstance(c, dict):
        return c
    if hasattr(c, "__dict__"):
        return {k: v for k, v in c.__dict__.items() if not k.startswith("_")}
    if isinstance(c, (list, tuple)):
        keys = ["id","employee_id","type_contract","start_date","end_date","state",
                "contractor","total_payment","payment_frequency","monthly_payment",
                "transport","value_hour","number_hour","position"]
        return {keys[i]: c[i] for i in range(min(len(c), len(keys)))}
    return dict(c)

def normalize_contracts(contratos: List[Any]) -> List[Dict[str, Any]]:
    data = [_to_dict(c) for c in contratos]
    for c in data:
        c["_start_parsed"] = _parse_date(c.get("start_date") or c.get("start") or c.get("_start_parsed"))
    data.sort(key=lambda x: x.get("_start_parsed") or datetime.min, reverse=True)
    return data

def periodo_y_tipos(contratos_norm: List[Dict[str, Any]]) -> Tuple[Optional[datetime], Optional[datetime], str]:
    fecha_inicio = None
    fecha_fin = None
    tipos = []
    for c in contratos_norm:
        s = _parse_date(c.get("start_date") or c.get("start") or c.get("_start_parsed"))
        e_raw = c.get("end_date") or c.get("end")
        e = _parse_date(e_raw) if e_raw else None
        if s and (fecha_inicio is None or s < fecha_inicio):
            fecha_inicio = s
        if e and (fecha_fin is None or e > fecha_fin):
            fecha_fin = e
        t = (c.get("type_contract") or c.get("type") or "").strip()
        if t and t not in tipos:
            tipos.append(t)
    tipos_text = ", ".join(tipos) if tipos else ""
    return fecha_inicio, fecha_fin, tipos_text

def construir_labores_text(emp_pos: str, contratos_norm: List[Dict[str, Any]]) -> str:
    cargos_raw = []
    for c in contratos_norm:
        pos = (c.get("position") or c.get("cargo") or "").strip()
        if pos:
            cargos_raw.append(pos)
    if emp_pos and emp_pos.strip() and emp_pos.strip() not in cargos_raw:
        cargos_raw.append(emp_pos.strip())
    seen = set(); cargos = []
    for p in cargos_raw:
        if p and p not in seen:
            seen.add(p); cargos.append(p)
    if not cargos:
        return ""
    if len(cargos) == 1:
        return f"como {cargos[0]}"
    if len(cargos) <= 3:
        joined = ", ".join(cargos[:-1]) + " y " + cargos[-1]
    else:
        joined = ", ".join(cargos[:3]) + ", etc."
    return f"desempeñando los cargos de {joined}"
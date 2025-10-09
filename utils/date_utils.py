from datetime import datetime, date

# Storage recomendado: 'iso' (YYYY-MM-DD). Cambiar a 'dmy' solo si realmente quiere guardar DD/MM/YYYY.
DB_STORAGE_FORMAT = 'iso'

INPUT_FORMATS = ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%Y/%m/%d", "%d.%m.%Y")

def _parse_any(value):
    if value is None or value == "":
        return None
    if isinstance(value, date) and not isinstance(value, str):
        return value
    s = str(value).strip()
    # Try ISO first
    try:
        return datetime.fromisoformat(s).date()
    except Exception:
        pass
    for fmt in INPUT_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    return None

def to_db(value):
    """Normaliza entrada y devuelve string para almacenar en DB según DB_STORAGE_FORMAT."""
    d = _parse_any(value)
    if d is None:
        return None
    if DB_STORAGE_FORMAT == 'iso':
        return d.isoformat()           # YYYY-MM-DD
    return d.strftime("%d/%m/%Y")      # DD/MM/YYYY si se cambia la configuración

def to_display(db_value, display_format="dmy"):
    """Convierte valor almacenado en DB a formato para UI. Por defecto devuelve DD/MM/YYYY."""
    if db_value is None or db_value == "":
        return ""
    d = _parse_any(db_value)
    if d is None:
        return str(db_value)
    if display_format == "iso":
        return d.isoformat()
    return d.strftime("%d/%m/%Y")
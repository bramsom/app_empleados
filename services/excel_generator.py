from controllers.contract_controller import listar_contratos
from controllers.employee_controller import listar_empleados
from controllers.affiliation_controller import listar_afiliaciones
import pandas as pd
from typing import List, Dict, Any

def _to_dict_list(items: List[Any]) -> List[Dict[str, Any]]:
    """Convierte lista de objetos/dicts a lista de dicts planos."""
    out = []
    for it in items or []:
        if isinstance(it, dict):
            out.append(it)
        else:
            # si es objeto con __dict__, úsalo; si no, intenta vars()
            try:
                out.append(getattr(it, "__dict__", dict(vars(it))))
            except Exception:
                out.append({"value": str(it)})
    return out

def obtener_datos_contratos():
    """
    Devuelve una lista de diccionarios con los datos de los contratos.
    """
    contratos = listar_contratos()
    return _to_dict_list(contratos)

def obtener_datos_empleados():
    empleados = listar_empleados()
    # Convierte cada objeto a dict con todos sus campos
    return _to_dict_list(empleados)

def obtener_datos_afiliaciones():
    """
    Devuelve una lista de diccionarios con los datos de las afiliaciones.
    """
    afiliaciones = listar_afiliaciones()
    return _to_dict_list(afiliaciones)

def export_to_excel(path: str):
    """
    Crea un Excel con hojas: Contratos, Empleados, Afiliaciones.
    Elimina columnas duplicadas en cada sheet antes de guardar.
    """
    contratos = obtener_datos_contratos()
    empleados = obtener_datos_empleados()
    afiliaciones = obtener_datos_afiliaciones()

    df_contratos = pd.DataFrame(contratos)
    df_empleados = pd.DataFrame(empleados)
    df_afiliaciones = pd.DataFrame(afiliaciones)

    # Eliminar columnas con nombres duplicados (mantiene la primera aparición)
    df_contratos = df_contratos.loc[:, ~df_contratos.columns.duplicated()]
    df_empleados = df_empleados.loc[:, ~df_empleados.columns.duplicated()]
    df_afiliaciones = df_afiliaciones.loc[:, ~df_afiliaciones.columns.duplicated()]

    with pd.ExcelWriter(path, engine="openpyxl", mode="w") as writer:
        df_contratos.to_excel(writer, sheet_name="Contratos", index=False)
        df_empleados.to_excel(writer, sheet_name="Empleados", index=False)
        df_afiliaciones.to_excel(writer, sheet_name="Afiliaciones", index=False)
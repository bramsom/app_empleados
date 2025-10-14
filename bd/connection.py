# bd/conection.py

import sqlite3
import os
import sys
import shutil

def conectar():
    """
    Soporta ejecución desde fuente y desde ejecutable PyInstaller.
    - Si está "frozen", copia la DB embebida (sys._MEIPASS) a una carpeta
      escribible del usuario (LOCALAPPDATA\app_empleados) la primera vez.
    - Conecta siempre a la copia en la carpeta escribible para que los cambios persistan.
    """
    if getattr(sys, 'frozen', False):
        embedded_db = os.path.join(sys._MEIPASS, "empleados.db")
        local_appdata = os.getenv("LOCALAPPDATA") or os.path.expanduser("~")
        app_dir = os.path.join(local_appdata, "app_empleados")
        os.makedirs(app_dir, exist_ok=True)
        db_path = os.path.join(app_dir, "empleados.db")
        # Sólo copiar si no existe (no sobrescribir datos del usuario)
        try:
            if not os.path.exists(db_path) and os.path.exists(embedded_db):
                shutil.copy2(embedded_db, db_path)
        except Exception:
            # en caso de fallo, intentar conectar al embedded (solo lectura posible)
            db_path = embedded_db if os.path.exists(embedded_db) else db_path
    else:
        base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        db_path = os.path.join(base_path, "empleados.db")

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
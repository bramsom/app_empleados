import sys
from pathlib import Path

# asegurar que la raíz del proyecto está en sys.path (permite imports desde scripts/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from bd.connection import conectar
import os
import shutil

DB = "empleados.db"  # ajusta si tu archivo se llama distinto
TABLES = [
    "employees",
    "contracts",
    "affiliations",            # ajusta si tu tabla de afiliaciones tiene otro nombre
    "salary_history",
    "hourly_history",
    "service_order_history"
]

def print_schema(cursor, table):
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,))
    row = cursor.fetchone()
    print(f"\n-- SCHEMA {table} --")
    print(row[0] if row and row[0] else "(no encontrado)")

def print_fk_list(cursor, table):
    print(f"\nPRAGMA foreign_key_list('{table}'):")
    cursor.execute(f"PRAGMA foreign_key_list('{table}')")
    for r in cursor.fetchall():
        print(r)

def count_orphans(cursor, child_table, fk_col, parent_table, parent_col="id"):
    q = f"SELECT COUNT(*) FROM {child_table} WHERE {fk_col} NOT IN (SELECT {parent_col} FROM {parent_table})"
    cursor.execute(q)
    return cursor.fetchone()[0]

def main():
    # respaldo rápido (local)
    if os.path.exists(DB):
        bak = DB + ".bak"
        if not os.path.exists(bak):
            try:
                import shutil
                shutil.copy2(DB, bak)
                print(f"Backup creado: {bak}")
            except Exception as e:
                print("No se pudo crear backup automático:", e)
    conn = conectar()
    cur = conn.cursor()

    # PRAGMA foreign_keys
    cur.execute("PRAGMA foreign_keys;")
    print("PRAGMA foreign_keys =", cur.fetchone()[0])

    # Mostrar esquema y fk list
    for t in TABLES:
        print_schema(cur, t)
        try:
            print_fk_list(cur, t)
        except Exception as e:
            print("Error al listar FKs:", e)

    # Buscar huérfanos comunes (ajusta nombres si tus columnas son distintas)
    checks = [
        ("affiliations", "employee_id", "employees"),
        ("contracts", "employee_id", "employees"),
        ("salary_history", "contract_id", "contracts"),
        ("hourly_history", "contract_id", "contracts"),
        ("service_order_history", "contract_id", "contracts"),
    ]
    print("\n-- Conteo de filas huérfanas --")
    for child, fk, parent in checks:
        try:
            c = count_orphans(cur, child, fk, parent)
            print(f"{child} sin {parent}: {c}")
        except Exception as e:
            print(f"{child}: error ({e})")

    conn.close()
    print("\nComprobación terminada. Si PRAGMA foreign_keys == 1 y las tablas tienen FKs con ON DELETE CASCADE, la eliminación debe cascada.")
    print("Si hay filas huérfanas, elimínalas o corrígelas antes de recrear tablas con CASCADE.")

if __name__ == "__main__":
    main()
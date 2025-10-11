import sys
from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from bd.connection import conectar

def counts(conn, emp_id):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM employees WHERE id=?", (emp_id,))
    print("employees:", cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM contracts WHERE employee_id=?", (emp_id,))
    print("contracts:", cur.fetchone()[0])
    cur.execute("SELECT COUNT(*) FROM affiliations WHERE employee_id=?", (emp_id,))
    print("affiliations:", cur.fetchone()[0])

if __name__ == "__main__":
    # --- Cambia este id por uno real de prueba ---
    emp_id = 2

    print("Antes:")
    conn = conectar()
    counts(conn, emp_id)
    conn.close()

    # Borrar usando la conexión que activa PRAGMA foreign_keys
    conn = conectar()
    cur = conn.cursor()
    cur.execute("BEGIN")
    cur.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    conn.commit()
    conn.close()

    print("\nDespués:")
    conn = conectar()
    counts(conn, emp_id)
    conn.close()
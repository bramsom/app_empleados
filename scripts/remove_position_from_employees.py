import sqlite3
import os
import sys
import os
# asegurar que la raíz del proyecto está en sys.path para poder importar bd.*
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root not in sys.path:
    sys.path.insert(0, root)

from bd.connection import conectar

def eliminar_columna_position():
    db_path = "empleados.db"  # ajusta si tu BD está en otra ruta
    if not os.path.exists(db_path):
        print("No se encontró la base de datos en:", db_path)
        return

    conn = conectar()
    cur = conn.cursor()
    try:
        # Desactivar FK temporalmente para operaciones DDL
        cur.execute("PRAGMA foreign_keys = OFF;")
        cur.execute("BEGIN TRANSACTION;")

        # 1) Crear tabla nueva sin la columna 'position'
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employees_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                document_type TEXT NOT NULL,
                document_number INTEGER NOT NULL UNIQUE,
                document_issuance TEXT NOT NULL,
                birthdate DATE NOT NULL,
                phone_number INTEGER NOT NULL,
                residence_address TEXT,
                RUT TEXT,
                email TEXT
            );
        """)

        # 2) Copiar datos desde la tabla antigua (omitimos position)
        cur.execute("""
            INSERT INTO employees_new (id, name, last_name, document_type, document_number, document_issuance, birthdate, phone_number, residence_address, RUT, email)
            SELECT id, name, last_name, document_type, document_number, document_issuance, birthdate, phone_number, residence_address, RUT, email
            FROM employees;
        """)

        # 3) Borrar tabla antigua y renombrar la nueva
        cur.execute("DROP TABLE employees;")
        cur.execute("ALTER TABLE employees_new RENAME TO employees;")

        conn.commit()
        print("✅ Columna 'position' eliminada de employees con éxito.")
    except sqlite3.Error as e:
        conn.rollback()
        print("Error durante la migración:", e)
    finally:
        # Reactivar FK
        try:
            cur.execute("PRAGMA foreign_keys = ON;")
        except Exception:
            pass
        conn.close()

if __name__ == "__main__":
    eliminar_columna_position()
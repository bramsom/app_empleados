import os
import sys
import shutil

# asegurar que la raíz del proyecto está en sys.path para poder importar bd.connection
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root not in sys.path:
    sys.path.insert(0, root)

from bd.connection import conectar

def main():
    conn = conectar()
    try:
        # obtener ruta física del archivo DB
        db_list = conn.execute("PRAGMA database_list;").fetchall()
        if not db_list:
            print("No se pudo obtener la ruta de la base de datos desde PRAGMA database_list.")
            return
        db_path = db_list[0][2]
        print("Base de datos detectada en:", db_path)

        # crear backup
        backup_path = db_path + ".backup"
        try:
            shutil.copyfile(db_path, backup_path)
            print("Backup creado en:", backup_path)
        except Exception as e:
            print("No se pudo crear backup automáticamente:", e)
            print("Continuando con precaución...")

        cur = conn.cursor()
        cur.execute("BEGIN;")
        cur.execute("DROP TABLE IF EXISTS contracts_old;")
        conn.commit()
        print("Tabla 'contracts_old' eliminada (si existía).")
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print("Error al eliminar contracts_old:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
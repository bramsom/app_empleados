import os
import sys
# Añadir la carpeta raíz del proyecto al path para que "bd" sea importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bd.connection import conectar

conn = conectar()
cur = conn.cursor()

# mostrar si existe la tabla users
cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
if not cur.fetchone():
    print("No existe la tabla 'users' en esta base de datos.")
else:
    cur.execute("SELECT id, username, lower(trim(username)) as norm FROM users;")
    rows = cur.fetchall()
    if not rows:
        print("Tabla users vacía")
    else:
        for r in rows:
            print(r)

conn.close()
# bd/conection.py

import sqlite3

def conectar():
    conn = sqlite3.connect("empleados.db")  # Usa la ruta correcta
    conn.execute("PRAGMA foreign_keys = ON")  # Activa las claves foráneas
    return conn
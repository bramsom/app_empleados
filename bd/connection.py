# bd/conection.py

import sqlite3

def conectar():
    return sqlite3.connect("empleados.db")

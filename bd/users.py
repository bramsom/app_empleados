import bcrypt
import sqlite3
from .connection import conectar

def crear_usuario(username, password, rol):
    if rol not in ['aprendiz', 'administrador']:
        raise ValueError("Rol no válido")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, rol) VALUES (?, ?, ?)", 
                       (username, hashed_password.decode('utf-8'), rol))
        conn.commit()
        print(f"✅ Usuario '{username}' creado con rol '{rol}'.")
    except sqlite3.IntegrityError:
        print(f"❌ El usuario '{username}' ya existe.")
    finally:
        conn.close()

def obtener_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, rol FROM users")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def eliminar_usuario(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def actualizar_usuario(id, nuevo_username, nuevo_rol):
    if nuevo_rol not in ['aprendiz', 'administrador']:
        raise ValueError("Rol no válido")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ?, rol = ? WHERE id = ?", 
                   (nuevo_username, nuevo_rol, id))
    conn.commit()
    conn.close()

def verificar_credenciales(username, password):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT password, rol FROM users WHERE username = ?", (username,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        hashed, rol = resultado
        if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
            return True, rol
    return False, None

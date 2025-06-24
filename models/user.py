import sqlite3
from bd.connection import conectar

class UserModel:
    @staticmethod
    def create(username, hashed_password, rol):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, rol) VALUES (?, ?, ?)", (username, hashed_password, rol))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, rol FROM users")
        users = cursor.fetchall()
        conn.close()
        return users

    @staticmethod
    def get_by_username(username):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT password, rol FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def delete(user_id):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

    @staticmethod
    def update(user_id, new_username, new_rol):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET username = ?, rol = ? WHERE id = ?", (new_username, new_rol, user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def update_password(user_id, new_hashed_password):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_hashed_password, user_id))
        conn.commit()
        conn.close()

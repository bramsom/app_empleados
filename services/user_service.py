import sqlite3
import bcrypt
from models.user import Usuario
from bd.connection import conectar

class UserModel:
    """
    Clase que maneja todas las operaciones de la base de datos para los usuarios.
    Abstrae la lógica de SQL.
    """
    @staticmethod
    def create(username, password_hashed, rol):
        """Crea un nuevo usuario en la base de datos."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, rol) VALUES (?, ?, ?)",
                           (username, password_hashed, rol))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """Obtiene todos los usuarios de la base de datos."""
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, rol FROM users")
        rows = cursor.fetchall()
        conn.close()
        return [Usuario(id=row[0], username=row[1], password=row[2], rol=row[3]) for row in rows]

    @staticmethod
    def get_by_id(user_id):
        """Obtiene un usuario por su ID."""
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password, rol FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Usuario(id=row[0], username=row[1], password=row[2], rol=row[3])
        return None

    @staticmethod
    def get_by_username(username):
        """Obtiene un usuario por su nombre de usuario."""
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT password, rol FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        return row

    @staticmethod
    def update(user_id, username, rol):
        """Actualiza el nombre de usuario y rol de un usuario."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET username = ?, rol = ? WHERE id = ?",
                           (username, rol, user_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    @staticmethod
    def update_password(user_id, new_password_hashed):
        """Actualiza la contraseña de un usuario."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE users SET password = ? WHERE id = ?",
                           (new_password_hashed, user_id))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(user_id):
        """Elimina un usuario de la base de datos."""
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            conn.close()


class UserService:
    """
    Clase que contiene la lógica de negocio para la gestión de usuarios.
    """
    @staticmethod
    def crear_usuario(username, password, rol):
        if rol not in ['aprendiz', 'administrador']:
            raise ValueError("Rol no válido")
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        success = UserModel.create(username, hashed, rol)
        if not success:
            raise ValueError("El nombre de usuario ya existe.")

    @staticmethod
    def obtener_usuarios():
        return UserModel.get_all()

    @staticmethod
    def eliminar_usuario(user_id):
        success = UserModel.delete(user_id)
        if not success:
            raise ValueError("Error al eliminar el usuario.")

    @staticmethod
    def actualizar_usuario(user_id, username, rol):
        success = UserModel.update(user_id, username, rol)
        if not success:
            raise ValueError("El nombre de usuario ya existe o no se pudo actualizar.")

    @staticmethod
    def cambiar_contraseña(user_id, nueva_password):
        hashed = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        success = UserModel.update_password(user_id, hashed)
        if not success:
            raise ValueError("Error al cambiar la contraseña.")

    @staticmethod
    def verificar_credenciales(username, password):
        data = UserModel.get_by_username(username)
        if not data:
            return False, None
        
        hashed, rol = data
        if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
            return True, rol
        return False, None
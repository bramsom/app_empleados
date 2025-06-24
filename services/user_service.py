import bcrypt
from models.user import UserModel

class UserService:
    @staticmethod
    def crear_usuario(username, password, rol):
        if rol not in ['aprendiz', 'administrador']:
            raise ValueError("Rol no válido")

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        UserModel.create(username, hashed, rol)

    @staticmethod
    def obtener_usuarios():
        return UserModel.get_all()

    @staticmethod
    def eliminar_usuario(user_id):
        UserModel.delete(user_id)

    @staticmethod
    def actualizar_usuario(user_id, username, rol):
        UserModel.update(user_id, username, rol)

    @staticmethod
    def cambiar_contraseña(user_id, nueva_password):
        hashed = bcrypt.hashpw(nueva_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        UserModel.update_password(user_id, hashed)

    @staticmethod
    def verificar_credenciales(username, password):
        data = UserModel.get_by_username(username)
        if not data:
            return False, None
        hashed, rol = data
        if bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8')):
            return True, rol
        return False, None

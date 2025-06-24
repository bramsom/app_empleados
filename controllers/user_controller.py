from services.user_service import UserService

class UserController:
    def crear(self, username, password, rol):
        return UserService.crear_usuario(username, password, rol)

    def listar(self):
        return UserService.obtener_usuarios()

    def eliminar(self, user_id):
        return UserService.eliminar_usuario(user_id)

    def actualizar(self, user_id, username, rol):
        return UserService.actualizar_usuario(user_id, username, rol)

    def cambiar_password(self, user_id, nueva):
        return UserService.cambiar_contraseña(user_id, nueva)

    def login(self, username, password):
        return UserService.verificar_credenciales(username, password)

from services.user_service import UserService

class UserController:
    def crear(self, username, password, rol):
        """
        Crea un nuevo usuario a través del servicio.
        """
        try:
            UserService.crear_usuario(username, password, rol)
            return True, "Usuario creado exitosamente."
        except ValueError as e:
            return False, str(e)

    def listar(self):
        """
        Lista todos los usuarios.
        """
        return UserService.obtener_usuarios()

    def eliminar(self, user_id):
        """
        Elimina un usuario por su ID.
        """
        try:
            UserService.eliminar_usuario(user_id)
            return True, "Usuario eliminado correctamente."
        except ValueError as e:
            return False, str(e)

    def actualizar(self, user_id, username, rol):
        """
        Actualiza los datos de un usuario.
        """
        try:
            UserService.actualizar_usuario(user_id, username, rol)
            return True, "Usuario actualizado correctamente."
        except ValueError as e:
            return False, str(e)

    def cambiar_password(self, user_id, nueva):
        """
        Cambia la contraseña de un usuario.
        """
        try:
            UserService.cambiar_contraseña(user_id, nueva)
            return True, "Contraseña cambiada exitosamente."
        except ValueError as e:
            return False, str(e)

    def login(self, username, password):
        """
        Verifica las credenciales de un usuario.
        """
        return UserService.verificar_credenciales(username, password)

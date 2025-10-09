from services.user_service import UserService

class UserController:
    def __init__(self, current_username=None, current_role=None, user_service=None):
        self.user_service = user_service or UserService()
        self.current_username = current_username
        self.current_role = current_role

    def obtener_todos(self):
        usuarios = self.user_service.obtener_usuarios()
        # Si es aprendiz, devuelve solo su propio usuario
        if self.current_role == "aprendiz" and self.current_username:
            return [u for u in usuarios if u.username == self.current_username]
        return usuarios

    def eliminar(self, user_id):
        if self.current_role == "aprendiz":
            raise PermissionError("No tienes permiso para eliminar usuarios.")
        self.user_service.eliminar_usuario(user_id)

    def crear(self, username, password, rol):
        if self.current_role == "aprendiz":
            raise PermissionError("No tienes permiso para crear usuarios.")
        self.user_service.crear_usuario(username, password, rol)

    def actualizar(self, user_id, username, rol, new_password=None):
        # aprendiz solo puede modificar su propio usuario y no cambiar rol
        if self.current_role == "aprendiz":
            # obtener su usuario para comparar
            usuarios = self.user_service.obtener_usuarios()
            usuario_actual = next((u for u in usuarios if u.username == self.current_username), None)
            if usuario_actual is None or usuario_actual.id != user_id:
                raise PermissionError("No tienes permiso para modificar este usuario.")
            if rol != "aprendiz":
                raise PermissionError("No puedes cambiar tu rol.")
        # aplicar cambios
        if new_password:
            self.user_service.cambiar_contraseña(user_id, new_password)
        # finalmente actualizar nombre y rol
        # Si rol es None o vacío, se asume que no se cambia
        rol_final = rol if rol else (self.user_service.get_by_id(user_id).rol if hasattr(self.user_service, "get_by_id") else rol)
        self.user_service.actualizar_usuario(user_id, username, rol_final)
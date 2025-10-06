from services.user_service import UserService
from models.user import Usuario

class UserController:
    def __init__(self):
        self.user_service = UserService()

    def registrar(self, username, password, rol):
        """
        Llama al servicio para registrar un nuevo usuario.
        Lanza excepciones si hay un error.
        """
        self.user_service.crear_usuario(username, password, rol)

    def modificar(self, user_id, username, password, rol):
        """
        Modifica un usuario existente.
        Este método maneja la lógica para actualizar el usuario y la contraseña de forma separada.
        """
        
        # 1. Llama al servicio para actualizar el nombre de usuario y el rol.
        self.user_service.actualizar_usuario(user_id, username, rol)

        # 2. Si se proporciona una contraseña (no es None y no está vacía), llama al servicio para cambiarla.
        if password is not None and password.strip() != "":
            self.user_service.cambiar_contraseña(user_id, password)

    def eliminar(self, user_id):
        """
        Llama al servicio para eliminar un usuario.
        Lanza excepciones si hay un error.
        """
        self.user_service.eliminar_usuario(user_id)

    def obtener_todos(self):
        """
        Llama al servicio para obtener todos los usuarios.
        """
        return self.user_service.obtener_usuarios()

    def obtener_por_id(self, user_id):
        """
        Llama al servicio para obtener un usuario por ID.
        """
        return self.user_service.obtener_por_id(user_id)
        
    def login(self, username, password):
        """
        Llama al servicio para verificar las credenciales de un usuario.
        """
        return self.user_service.verificar_credenciales(username, password)
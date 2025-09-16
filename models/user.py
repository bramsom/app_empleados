class Usuario:
    """
    Clase que representa un usuario de la aplicación.
    Funciona como un objeto de transferencia de datos (DTO).
    """
    def __init__(self, id, username, password, rol):
        self.id = id
        self.username = username
        self.password = password  # La contraseña ya viene hasheada de la base de datos
        self.rol = rol

    def __repr__(self):
        """Representación del objeto para facilitar la depuración."""
        return f"<Usuario(id={self.id}, username='{self.username}', rol='{self.rol}')>"


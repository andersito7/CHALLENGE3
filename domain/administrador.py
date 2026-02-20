
from domain.usuario import Usuario

class Administrador(Usuario):
    """
    Representa a un administrador del sistema.
    """

    def __init__(self, nombres, apellidos, username, pin):
        super().__init__(nombres, apellidos, username, pin, rol="admin")

    def to_dict(self):
        return {
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "username": self.dui,  # aquí dui almacena el username
            "pin": self.pin,
            "rol": self.rol
        }

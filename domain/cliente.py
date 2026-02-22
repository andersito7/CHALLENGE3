
from domain.usuario import Usuario

class Cliente(Usuario):
    """
    Representa a un cliente del banco.
    """

    def __init__(self, nombres, apellidos, dui, pin):
        super().__init__(nombres, apellidos, dui, pin, rol="cliente")

    def to_dict(self):
        """
        Convierte el cliente en un diccionario para CSV.
        """
        return {
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "dui": self.dui,
            "pin": self.pin,
            "rol": self.rol
        }

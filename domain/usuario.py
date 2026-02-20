
from abc import ABC, abstractmethod

class Usuario(ABC):
    """
    Clase base abstracta para todos los usuarios del sistema.
    Contiene datos comunes: nombres, apellidos, DUI, PIN y rol.
    """

    def __init__(self, nombres: str, apellidos: str, dui: str, pin: str, rol: str):
        self.nombres = nombres
        self.apellidos = apellidos
        self.dui = dui
        self.pin = pin
        self.rol = rol  # "cliente" o "admin"

    @abstractmethod
    def to_dict(self):
        """
        Debe implementarse en las clases hijas para serializar datos.
        """
        pass

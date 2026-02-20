
from datetime import datetime
import uuid


class Transferencia:
    """
    Representa una transferencia entre dos cuentas.
    """

    def __init__(self, cuenta_origen: str, cuenta_destino: str, monto: float):
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        self.id = str(uuid.uuid4())
        self.cuenta_origen = cuenta_origen
        self.cuenta_destino = cuenta_destino
        self.monto = monto
        self.fecha = datetime.now()

    def to_dict(self):
        """
        Convierte la transferencia a diccionario para CSV.
        """
        return {
            "id": self.id,
            "cuenta_origen": self.cuenta_origen,
            "cuenta_destino": self.cuenta_destino,
            "monto": self.monto,
            "fecha": self.fecha.isoformat()
        }

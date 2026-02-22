
from datetime import datetime
import uuid


class Transaccion:
    """
    Representa un movimiento realizado en una cuenta bancaria.
    Puede ser depósito, retiro o parte de una transferencia.
    """

    def __init__(self, cuenta_id: str, tipo: str, monto: float):
        """
        Inicializa una transacción.

        cuenta_id: ID de la cuenta
        tipo: "deposito", "retiro", "transferencia_in", "transferencia_out"
        monto: cantidad involucrada
        """

        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        self.id = str(uuid.uuid4())
        self.cuenta_id = cuenta_id
        self.tipo = tipo
        self.monto = monto
        self.fecha = datetime.now()

    def to_dict(self):
        """
        Convierte la transacción en un diccionario serializable para CSV.
        """
        return {
            "id": self.id,
            "cuenta_id": self.cuenta_id,
            "tipo": self.tipo,
            "monto": self.monto,
            "fecha": self.fecha.isoformat()
        }

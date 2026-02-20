
from domain.transaccion import Transaccion

class Cuenta:
    """
    Representa una cuenta bancaria.
    """

    def __init__(self, numero: str, cliente_id: str, tipo: str, saldo_inicial: float = 0.0, activa: bool = True):
        self.numero = numero
        self.cliente_id = cliente_id
        self.tipo = tipo  # "ahorro" o "corriente"
        self.saldo = saldo_inicial
        self.activa = activa

    # -----------------------------
    # OPERACIONES
    # -----------------------------

    def depositar(self, monto: float):
        if not self.activa:
            raise Exception("La cuenta está bloqueada")

        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        self.saldo += monto
        return Transaccion(self.numero, "deposito", monto)

    def retirar(self, monto: float):
        if not self.activa:
            raise Exception("La cuenta está bloqueada")

        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        if monto > self.saldo:
            raise Exception("Saldo insuficiente")

        self.saldo -= monto
        return Transaccion(self.numero, "retiro", monto)

    # -----------------------------
    # ESTADO
    # -----------------------------

    def bloquear(self):
        self.activa = False

    def activar(self):
        self.activa = True

    # -----------------------------
    # SERIALIZACIÓN
    # -----------------------------

    def to_dict(self):
        return {
            "numero": self.numero,
            "cliente_id": self.cliente_id,
            "tipo": self.tipo,
            "saldo": self.saldo,
            "activa": self.activa
        }

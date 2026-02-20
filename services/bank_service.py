from domain.transferencia import Transferencia


class BankService:
    """
    Servicio que orquesta las operaciones bancarias entre cuentas.
    Se comunica con los repositorios para persistir cambios.
    """

    def __init__(self, cuenta_repo, transaccion_repo, transferencia_repo):
        self.cuenta_repo = cuenta_repo
        self.transaccion_repo = transaccion_repo
        self.transferencia_repo = transferencia_repo

    # ============================================================
    # OPERACIONES INDIVIDUALES
    # ============================================================

    def depositar(self, cuenta_num, monto):
        """
        Deposita dinero en una cuenta.
        - Valida existencia
        - Valida estado
        - Actualiza saldo
        - Registra transacción
        """

        cuenta = self.cuenta_repo.obtener_por_numero(cuenta_num)
        if not cuenta:
            raise Exception("Cuenta no encontrada")

        trans = cuenta.depositar(monto)

        # Persistencia
        self.cuenta_repo.actualizar(cuenta)
        self.transaccion_repo.guardar(trans)

        return trans

    def retirar(self, cuenta_num, monto):
        """
        Retira dinero de una cuenta.
        """

        cuenta = self.cuenta_repo.obtener_por_numero(cuenta_num)
        if not cuenta:
            raise Exception("Cuenta no encontrada")

        trans = cuenta.retirar(monto)

        # Persistencia
        self.cuenta_repo.actualizar(cuenta)
        self.transaccion_repo.guardar(trans)

        return trans

    # ============================================================
    # TRANSFERENCIAS
    # ============================================================

    def transferir(self, origen_num, destino_num, monto):
        """
        Ejecuta una transferencia completa:
        - Retira de la cuenta origen
        - Deposita en la cuenta destino
        - Registra transacciones individuales
        - Registra la transferencia global
        """

        origen = self.cuenta_repo.obtener_por_numero(origen_num)
        destino = self.cuenta_repo.obtener_por_numero(destino_num)

        if not origen or not destino:
            raise Exception("Cuenta no encontrada")

        if not origen.activa or not destino.activa:
            raise Exception("Una de las cuentas está bloqueada")

        # Operaciones en memoria
        trans_out = origen.retirar(monto)
        trans_in = destino.depositar(monto)

        transferencia = Transferencia(origen_num, destino_num, monto)

        # Persistencia
        self.cuenta_repo.actualizar(origen)
        self.cuenta_repo.actualizar(destino)

        self.transaccion_repo.guardar(trans_out)
        self.transaccion_repo.guardar(trans_in)
        self.transferencia_repo.guardar(transferencia)

        return transferencia

    # ============================================================
    # CONSULTAS
    # ============================================================

    def obtener_transacciones(self, numero_cuenta):
        """
        Devuelve todas las transacciones asociadas a una cuenta.
        """
        return self.transaccion_repo.obtener_por_cuenta(numero_cuenta)

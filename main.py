

from domain.cuenta import Cuenta
from services.bank_service import BankService
from analytics.estadisticas import Estadisticas

# ============================
# REPOSITORIOS MOCK (TEMPORALES)
# ============================

class MockCuentaRepo:
    def __init__(self):
        self.cuentas = {}

    def agregar(self, cuenta):
        self.cuentas[cuenta.numero] = cuenta

    def obtener_por_numero(self, numero):
        return self.cuentas.get(numero)

    def actualizar(self, cuenta):
        self.cuentas[cuenta.numero] = cuenta


class MockTransaccionRepo:
    def __init__(self):
        self.transacciones = []

    def guardar(self, transaccion):
        self.transacciones.append(transaccion.to_dict())

    def obtener_por_cuenta(self, cuenta_id):
        return [t for t in self.transacciones if t["cuenta_id"] == cuenta_id]

    def obtener_todas(self):
        return self.transacciones


class MockTransferenciaRepo:
    def __init__(self):
        self.transferencias = []

    def guardar(self, transferencia):
        self.transferencias.append(transferencia.to_dict())


# ============================
# INICIALIZACIÓN
# ============================

cuenta_repo = MockCuentaRepo()
trans_repo = MockTransaccionRepo()
transfer_repo = MockTransferenciaRepo()

bank = BankService(cuenta_repo, trans_repo, transfer_repo)

# ============================
# CREAR CUENTAS DE PRUEBA
# ============================

c1 = Cuenta("001", "CLI001", "ahorro", 100)
c2 = Cuenta("002", "CLI002", "ahorro", 50)

cuenta_repo.agregar(c1)
cuenta_repo.agregar(c2)

# ============================
# PRUEBAS DE OPERACIONES
# ============================

print("\n=== PRUEBA DE OPERACIONES ===")

print("Depositando 40 en cuenta 001...")
bank.depositar("001", 40)

print("Retirando 20 de cuenta 001...")
bank.retirar("001", 20)

print("Transfiriendo 30 de cuenta 001 a 002...")
bank.transferir("001", "002", 30)

print("\nSaldos finales:")
print("Cuenta 001:", cuenta_repo.obtener_por_numero("001").saldo)
print("Cuenta 002:", cuenta_repo.obtener_por_numero("002").saldo)

# ============================
# PRUEBA DE ESTADÍSTICAS
# ============================

print("\n=== ESTADÍSTICAS CUENTA 001 ===")

trans_c1 = trans_repo.obtener_por_cuenta("001")
resumen = Estadisticas.resumen_por_cuenta(trans_c1)

for k, v in resumen.items():
    print(f"{k}: {v}")

# ============================
# TRANSACCIONES REGISTRADAS
# ============================

print("\n=== TODAS LAS TRANSACCIONES ===")
for t in trans_repo.obtener_todas():
    print(t)

print("\n=== TRANSFERENCIAS REGISTRADAS ===")
for tr in transfer_repo.transferencias:
    print(tr)

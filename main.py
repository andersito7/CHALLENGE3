# ============================================================
# IMPORTACIÓN DE REPOSITORIOS Y SERVICIOS
# ============================================================

from repositories.usuario_repo import UsuarioRepo
from repositories.cuenta_repo import CuentaRepo
from repositories.transaccion_repo import TransaccionRepo
from repositories.transferencia_repo import TransferenciaRepo

from services.admin_service import AdminService
from services.bank_service import BankService
from services.analytics_service import AnalyticsService


# ============================================================
# INICIALIZACIÓN DE SERVICIOS
# ============================================================

def inicializar_servicios():
    """
    Crea repositorios y servicios principales del sistema.
    """
    usuario_repo = UsuarioRepo()
    cuenta_repo = CuentaRepo()
    transaccion_repo = TransaccionRepo()
    transferencia_repo = TransferenciaRepo()

    admin_service = AdminService(usuario_repo, cuenta_repo)
    bank_service = BankService(cuenta_repo, transaccion_repo, transferencia_repo)
    analytics_service = AnalyticsService(transaccion_repo)

    return admin_service, bank_service, analytics_service, usuario_repo, cuenta_repo, transaccion_repo


# ============================================================
# LOGIN DEL CLIENTE
# ============================================================

def login_cliente(usuario_repo):
    print("\n===== LOGIN CLIENTE =====")
    dui = input("Ingrese su DUI: ")
    pin = input("Ingrese su PIN: ")

    usuario = usuario_repo.buscar_por_dui(dui)

    if not usuario:
        print("Usuario no encontrado.")
        return None

    if usuario.pin != pin:
        print("PIN incorrecto.")
        return None

    if usuario.rol != "cliente":
        print("Este usuario no es un cliente.")
        return None

    print(f"\nBienvenido, {usuario.nombres} {usuario.apellidos}")
    return usuario


# ============================================================
# MENÚ DEL CLIENTE
# ============================================================

def menu_cliente(cliente, cuenta_repo, bank_service, transaccion_repo):
    """
    Menú principal del cliente.
    """
    while True:
        print("\n===== MENÚ CLIENTE =====")
        print("1. Ver mis cuentas")
        print("2. Depositar")
        print("3. Retirar")
        print("4. Transferir")
        print("5. Ver historial de transacciones")
        print("6. Salir al menú principal")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                ver_mis_cuentas(cliente, cuenta_repo)

            elif opcion == "2":
                depositar_cliente(cliente, cuenta_repo, bank_service)

            elif opcion == "3":
                retirar_cliente(cliente, cuenta_repo, bank_service)

            elif opcion == "4":
                transferir_cliente(cliente, cuenta_repo, bank_service)

            elif opcion == "5":
                historial_cliente(cliente, cuenta_repo, transaccion_repo)

            elif opcion == "6":
                break

            else:
                print("Opción inválida.")

        except Exception as e:
            print(f"Error: {e}")


# ============================================================
# FUNCIONES DEL CLIENTE
# ============================================================

def ver_mis_cuentas(cliente, cuenta_repo):
    print("\n--- Mis Cuentas ---")
    cuentas = cuenta_repo.cargar_todas()

    cuentas_cliente = [c for c in cuentas if c.cliente_id == cliente.dui]

    if not cuentas_cliente:
        print("No tienes cuentas registradas.")
        return

    for c in cuentas_cliente:
        estado = "Activa" if c.activa else "Bloqueada"
        print(f"{c.numero} | Tipo: {c.tipo} | Saldo: {c.saldo} | {estado}")


def depositar_cliente(cliente, cuenta_repo, bank_service):
    print("\n--- Depositar ---")
    numero = input("Número de cuenta: ")
    monto = float(input("Monto a depositar: "))

    cuenta = cuenta_repo.obtener_por_numero(numero)

    if not cuenta or cuenta.cliente_id != cliente.dui:
        print("No puedes operar esta cuenta.")
        return

    trans = bank_service.depositar(numero, monto)
    print(f"Depósito realizado. ID transacción: {trans.id}")


def retirar_cliente(cliente, cuenta_repo, bank_service):
    print("\n--- Retirar ---")
    numero = input("Número de cuenta: ")
    monto = float(input("Monto a retirar: "))

    cuenta = cuenta_repo.obtener_por_numero(numero)

    if not cuenta or cuenta.cliente_id != cliente.dui:
        print("No puedes operar esta cuenta.")
        return

    trans = bank_service.retirar(numero, monto)
    print(f"Retiro realizado. ID transacción: {trans.id}")


def transferir_cliente(cliente, cuenta_repo, bank_service):
    print("\n--- Transferir ---")
    origen = input("Cuenta origen: ")
    destino = input("Cuenta destino: ")
    tipoTransaccion = input("Tipo de transacción (depósito/retiro): ")
    tipoCuenta = input("Tipo de cuenta (ahorro/corriente): ")
    monto = float(input("Monto a transferir: "))

    cuenta_origen = cuenta_repo.obtener_por_numero(origen)

    if not cuenta_origen or cuenta_origen.cliente_id != cliente.dui:
        print("No puedes operar esta cuenta.")
        return

    transferencia = bank_service.transferir(origen, destino, monto)
    print(f"Transferencia realizada. ID: {transferencia.id}")


def obtener_cuentas_cliente(cliente, cuenta_repo):
    cuentas = cuenta_repo.cargar_todas()
    return [c.numero for c in cuentas if c.cliente_id == cliente.dui]


def historial_cliente(cliente, cuenta_repo, transaccion_repo):
    print("\n--- Historial de Transacciones ---")

    cuentas_cliente = obtener_cuentas_cliente(cliente, cuenta_repo)
    trans = transaccion_repo.obtener_todas()

    trans_cliente = [t for t in trans if t["cuenta_id"] in cuentas_cliente]

    if not trans_cliente:
        print("No tienes transacciones registradas.")
        return

    for t in trans_cliente:
        print(f"{t['fecha']} | {t['tipo']} | ${t['monto']} | ID: {t['id']}")


# ============================================================
# MENÚ DEL ADMINISTRADOR
# ============================================================

def menu_admin(admin_service, bank_service, analytics_service):
    """
    Menú principal del administrador.
    """
    while True:
        print("\n===== MENÚ ADMINISTRADOR =====")
        print("1. Crear cliente")
        print("2. Crear administrador")
        print("3. Crear cuenta")
        print("4. Listar usuarios")
        print("5. Listar cuentas")
        print("6. Bloquear cuenta")
        print("7. Activar cuenta")
        print("8. Ver estadísticas del sistema")
        print("9. Salir al menú principal")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                crear_cliente(admin_service)

            elif opcion == "2":
                crear_admin(admin_service)

            elif opcion == "3":
                crear_cuenta(admin_service)

            elif opcion == "4":
                listar_usuarios(admin_service)

            elif opcion == "5":
                listar_cuentas(admin_service)

            elif opcion == "6":
                bloquear_cuenta(admin_service)

            elif opcion == "7":
                activar_cuenta(admin_service)

            elif opcion == "8":
                ver_estadisticas(analytics_service)

            elif opcion == "9":
                break

            else:
                print("Opción inválida.")

        except Exception as e:
            print(f"Error: {e}")


# ============================================================
# FUNCIONES DEL ADMINISTRADOR
# ============================================================

def crear_cliente(admin_service):
    print("\n--- Crear Cliente ---")
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    dui = input("DUI: ")
    pin = input("PIN: ")

    cliente = admin_service.crear_cliente(nombres, apellidos, dui, pin)
    print(f"Cliente creado: {cliente.nombres} {cliente.apellidos}")


def crear_admin(admin_service):
    print("\n--- Crear Administrador ---")
    nombres = input("Nombres: ")
    apellidos = input("Apellidos: ")
    username = input("Username: ")
    pin = input("PIN: ")

    admin = admin_service.crear_administrador(nombres, apellidos, username, pin)
    print(f"Administrador creado: {admin.nombres} ({admin.dui})")


def crear_cuenta(admin_service):
    print("\n--- Crear Cuenta ---")
    numero = input("Número de cuenta: ")
    cliente_id = input("DUI del cliente: ")
    tipo = input("Tipo (ahorro/corriente): ")
    saldo = float(input("Saldo inicial: "))

    cuenta = admin_service.crear_cuenta(numero, cliente_id, tipo, saldo)
    print(f"Cuenta creada: {cuenta.numero} para cliente {cuenta.cliente_id}")


def listar_usuarios(admin_service):
    print("\n--- Lista de Usuarios ---")
    usuarios = admin_service.listar_usuarios()

    for u in usuarios:
        print(f"{u.nombres} {u.apellidos} | {u.dui} | rol: {u.rol}")


def listar_cuentas(admin_service):
    print("\n--- Lista de Cuentas ---")
    cuentas = admin_service.listar_cuentas()

    for c in cuentas:
        estado = "Activa" if c.activa else "Bloqueada"
        print(f"{c.numero} | Cliente: {c.cliente_id} | Saldo: {c.saldo} | {estado}")


def bloquear_cuenta(admin_service):
    print("\n--- Bloquear Cuenta ---")
    numero = input("Número de cuenta: ")

    cuenta = admin_service.bloquear_cuenta(numero)
    print(f"Cuenta {cuenta.numero} bloqueada.")


def activar_cuenta(admin_service):
    print("\n--- Activar Cuenta ---")
    numero = input("Número de cuenta: ")

    cuenta = admin_service.activar_cuenta(numero)
    print(f"Cuenta {cuenta.numero} activada.")


def ver_estadisticas(analytics_service):
    print("\n--- Estadísticas del Sistema ---")
    stats = analytics_service.obtener_estadisticas()

    print(f"Total de transacciones: {stats['total_transacciones']}")
    print(f"Total de depósitos: {stats['total_depositos']}")
    print(f"Total de retiros: {stats['total_retiros']}")
    print(f"Total de transferencias: {stats['total_transferencias']}")
    print(f"Monto total movido: ${stats['monto_total']}")
    print(f"Monto promedio por transacción: ${stats['monto_promedio']}")


# ============================================================
# MENÚ PRINCIPAL
# ============================================================

def main():
    admin_service, bank_service, analytics_service, usuario_repo, cuenta_repo, transaccion_repo = inicializar_servicios()

    while True:
        print("\n===== SISTEMA BANCARIO =====")
        print("1. Administrador")
        print("2. Cliente")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_admin(admin_service, bank_service, analytics_service)

        elif opcion == "2":
            cliente = login_cliente(usuario_repo)
            if cliente:
                menu_cliente(cliente, cuenta_repo, bank_service, transaccion_repo)

        elif opcion == "3":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    main()
    
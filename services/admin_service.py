from domain.cliente import Cliente
from domain.administrador import Administrador
from domain.cuenta import Cuenta


class AdminService:
    """
    Servicio que gestiona las funciones administrativas del sistema.
    Se apoya en los repositorios para persistir datos.
    """

    def __init__(self, usuario_repo, cuenta_repo):
        """
        Recibe los repositorios necesarios.
        """
        self.usuario_repo = usuario_repo
        self.cuenta_repo = cuenta_repo

    
    # USUARIOS
    
    def crear_cliente(self, nombres, apellidos, dui, pin):
        """
        Crea un cliente nuevo y lo guarda en el CSV.
        """

        # Validar que no exista un usuario con ese DUI
        if self.usuario_repo.buscar_por_dui(dui):
            raise Exception("Ya existe un usuario con ese DUI")

        cliente = Cliente(nombres, apellidos, dui, pin)
        self.usuario_repo.agregar(cliente)

        return cliente

    def crear_administrador(self, nombres, apellidos, username, pin):
        """
        Crea un administrador del sistema.
        IMPORTANTE:
        - El username se almacena en el campo 'dui' según tu diseño.
        """

        if self.usuario_repo.buscar_por_dui(username):
            raise Exception("Ya existe un administrador con ese username")

        admin = Administrador(nombres, apellidos, username, pin)
        self.usuario_repo.agregar(admin)

        return admin

    def listar_usuarios(self):
        """
        Devuelve todos los usuarios registrados.
        """
        return self.usuario_repo.cargar_todos()

    # CUENTAS
    

    def crear_cuenta(self, numero, cliente_id, tipo, saldo_inicial=0.0):
        """
        Crea una cuenta bancaria para un cliente existente.
        """

        # Validar que el cliente exista
        cliente = self.usuario_repo.buscar_por_dui(cliente_id)
        if not cliente:
            raise Exception("El cliente no existe")

        # Validar que no exista una cuenta con ese número
        if self.cuenta_repo.obtener_por_numero(numero):
            raise Exception("Ya existe una cuenta con ese número")

        cuenta = Cuenta(numero, cliente_id, tipo, saldo_inicial)
        self.cuenta_repo.agregar(cuenta)

        return cuenta

    def listar_cuentas(self):
        """
        Devuelve todas las cuentas registradas.
        """
        return self.cuenta_repo.cargar_todas()

    def bloquear_cuenta(self, numero):
        """
        Cambia el estado de una cuenta a bloqueada.
        """
        cuenta = self.cuenta_repo.obtener_por_numero(numero)
        if not cuenta:
            raise Exception("Cuenta no encontrada")

        cuenta.bloquear()
        self.cuenta_repo.actualizar(cuenta)

        return cuenta

    def activar_cuenta(self, numero):
        """
        Cambia el estado de una cuenta a activa.
        """
        cuenta = self.cuenta_repo.obtener_por_numero(numero)
        if not cuenta:
            raise Exception("Cuenta no encontrada")

        cuenta.activar()
        self.cuenta_repo.actualizar(cuenta)

        return cuenta

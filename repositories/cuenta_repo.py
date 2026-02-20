import csv
import os
from domain.cuenta import Cuenta


class CuentaRepo:
    """
    Repositorio encargado de manejar la persistencia de cuentas bancarias.
    """

    def __init__(self, filepath="data/cuentas.csv"):
        self.filepath = filepath
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        """
        Crea el archivo CSV con los encabezados correctos si no existe.
        """
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["numero", "cliente_id", "tipo", "saldo", "activa"]
                )
                writer.writeheader()

    def cargar_todas(self):
        """
        Carga todas las cuentas desde el CSV y las convierte en objetos Cuenta.
        """
        cuentas = []
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:

                # Convertimos los tipos correctamente
                cuenta = Cuenta(
                    numero=row["numero"],
                    cliente_id=row["cliente_id"],
                    tipo=row["tipo"],
                    saldo_inicial=float(row["saldo"]),
                    activa=row["activa"] == "True"  # CSV guarda booleanos como texto
                )

                cuentas.append(cuenta)

        return cuentas

    def guardar_todas(self, cuentas):
        """
        Sobrescribe el archivo CSV con todas las cuentas.
        """
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["numero", "cliente_id", "tipo", "saldo", "activa"]
            )
            writer.writeheader()

            for c in cuentas:
                writer.writerow(c.to_dict())

    def agregar(self, cuenta):
        """
        Agrega una cuenta nueva al CSV.
        """
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["numero", "cliente_id", "tipo", "saldo", "activa"]
            )
            writer.writerow(cuenta.to_dict())

    def obtener_por_numero(self, numero):
        """
        Busca una cuenta por su número único.
        """
        for c in self.cargar_todas():
            if c.numero == numero:
                return c
        return None

    def actualizar(self, cuenta_actualizada):
        """
        Reemplaza una cuenta existente por su versión actualizada.
        """
        cuentas = self.cargar_todas()

        for i, c in enumerate(cuentas):
            if c.numero == cuenta_actualizada.numero:
                cuentas[i] = cuenta_actualizada
                break

        self.guardar_todas(cuentas)

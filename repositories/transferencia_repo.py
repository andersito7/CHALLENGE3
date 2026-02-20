import csv
import os
from domain.transferencia import Transferencia


class TransferenciaRepo:
    """
    Repositorio encargado de almacenar transferencias completas.
    Devuelve diccionarios para compatibilidad con análisis.
    """

    def __init__(self, filepath="data/transferencias.csv"):
        self.filepath = filepath
        self._asegurar_archivo()

    def _asegurar_archivo(self):
        """
        Crea el archivo CSV si no existe.
        """
        if not os.path.exists(self.filepath):
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=["id", "cuenta_origen", "cuenta_destino", "monto", "fecha"]
                )
                writer.writeheader()

    def obtener_todas(self):
        """
        Devuelve todas las transferencias como diccionarios.
        """
        trans = []
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                trans.append({
                    "id": row["id"],
                    "cuenta_origen": row["cuenta_origen"],
                    "cuenta_destino": row["cuenta_destino"],
                    "monto": float(row["monto"]),
                    "fecha": row["fecha"]
                })
        return trans

    def guardar(self, transferencia: Transferencia):
        """
        Guarda una transferencia generada por BankService.
        """
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["id", "cuenta_origen", "cuenta_destino", "monto", "fecha"]
            )
            writer.writerow(transferencia.to_dict())

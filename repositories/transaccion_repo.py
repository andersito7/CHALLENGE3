import csv
import os
from domain.transaccion import Transaccion


class TransaccionRepo:
    """
    Repositorio encargado de almacenar transacciones.
    IMPORTANTE:
    - Devuelve diccionarios, no objetos, porque Estadisticas.py trabaja con dicts.
    """

    def __init__(self, filepath="data/transacciones.csv"):
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
                    fieldnames=["id", "cuenta_id", "tipo", "monto", "fecha"]
                )
                writer.writeheader()

    def obtener_todas(self):
        """
        Devuelve todas las transacciones como diccionarios.
        """
        trans = []
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                trans.append({
                    "id": row["id"],
                    "cuenta_id": row["cuenta_id"],
                    "tipo": row["tipo"],
                    "monto": float(row["monto"]),
                    "fecha": row["fecha"]
                })
        return trans

    def obtener_por_cuenta(self, cuenta_id):
        """
        Devuelve todas las transacciones asociadas a una cuenta.
        """
        return [t for t in self.obtener_todas() if t["cuenta_id"] == cuenta_id]

    def guardar(self, transaccion: Transaccion):
        """
        Guarda una transacción generada por BankService.
        """
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["id", "cuenta_id", "tipo", "monto", "fecha"]
            )
            writer.writerow(transaccion.to_dict())

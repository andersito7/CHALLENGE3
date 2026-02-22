import numpy as np
from datetime import datetime
from repositories.transaccion_repo import TransaccionRepo

class AnomaliasDetector:
    def __init__(self):
        self.repo = TransaccionRepo()
        self.transacciones = self.repo.obtener_todas()

    def z_score_outliers(self, threshold=3.0):
        """
        Detecta transacciones cuyo monto es un outlier según Z-score.
        """
        montos = np.array([t["monto"] for t in self.transacciones])
        if len(montos) == 0:
            return []
        media = np.mean(montos)
        std = np.std(montos)
        if std == 0:
            return []

        return [ t for t in self.transacciones if std > 0 and abs(t["monto"] - media) / std > threshold]

    def structuring(self, ventana_minutos=30, umbral_monto=100):
        """
        Detecta depósitos pequeños repetidos en una ventana corta de tiempo.
        """
        trans = sorted(self.transacciones, key=lambda t: t["fecha"])
        resultado = []
        for i in range(len(trans) - 1):
            t1 = trans[i]
            t2 = trans[i + 1]
            if t1["tipo"] == "deposito" and t2["tipo"] == "deposito":
                f1 = datetime.fromisoformat(t1["fecha"])
                f2 = datetime.fromisoformat(t2["fecha"])
                if (
                    t1["cuenta_id"] == t2["cuenta_id"]
                    and (f2 - f1).total_seconds() / 60 < ventana_minutos
                    and t1["monto"] < umbral_monto
                    and t2["monto"] < umbral_monto
                ):
                    resultado.append((t1, t2))
        return resultado

    def actividad_nocturna(self):
        """
        Detecta transacciones realizadas entre las 00:00 y las 04:00.
        """
        return [
            t for t in self.transacciones
            if 0 <= datetime.fromisoformat(t["fecha"]).hour < 4
        ]

# ============================================================
# PRUEBA RÁPIDA
# ============================================================

if __name__ == "__main__":
    detector = AnomaliasDetector()

    print("\n--- Anomalías por Z-score ---")
    for t in detector.z_score_outliers():
        print(f"{t['fecha']} | {t['tipo']} | ${t['monto']} | ID: {t['id']}")

    print("\n--- Structuring detectado ---")
    for t1, t2 in detector.structuring():
        print(f"{t1['fecha']} y {t2['fecha']} | {t1['monto']} + {t2['monto']} | Cuenta: {t1['cuenta_id']}")

    print("\n--- Actividad Nocturna ---")
    for t in detector.actividad_nocturna():
        print(f"{t['fecha']} | {t['tipo']} | ${t['monto']} | ID: {t['id']}")


from analytics.estadisticas import Estadisticas


class AnalyticsService:
    """
    Servicio que usa Estadisticas para generar reportes.
    """

    def __init__(self, transaccion_repo):
        self.transaccion_repo = transaccion_repo

    def resumen_por_cuenta(self, cuenta_id):
        trans = self.transaccion_repo.obtener_por_cuenta(cuenta_id)
        return Estadisticas.resumen_por_cuenta(trans)

    def transacciones_por_dia(self):
        trans = self.transaccion_repo.obtener_todas()
        return Estadisticas.transacciones_por_dia(trans)

    def total_diario(self):
        trans = self.transaccion_repo.obtener_todas()
        return Estadisticas.total_diario(trans)


import numpy as np
from datetime import datetime


class Estadisticas:
    """
    Funciones vectorizadas para análisis estadístico de transacciones.
    Cada transacción debe venir como diccionario:
    {
        "id": "...",
        "cuenta_id": "...",
        "tipo": "deposito" | "retiro" | "transferencia_in" | "transferencia_out",
        "monto": float,
        "fecha": "2026-02-01T10:00:00"
    }
    """

   
    # FILTROS BÁSICOS
   

    @staticmethod
    def _filtrar_por_tipo(transacciones, tipo):
        """
        Devuelve un array de montos filtrados por tipo de transacción.
        """
        return np.array([t["monto"] for t in transacciones if t["tipo"] == tipo], dtype=float)

    
    # MÉTRICAS POR CUENTA
    

    @staticmethod
    def total_depositos(transacciones):
        montos = Estadisticas._filtrar_por_tipo(transacciones, "deposito")
        return np.sum(montos) if montos.size > 0 else 0.0

    @staticmethod
    def total_gastos(transacciones):
        montos = Estadisticas._filtrar_por_tipo(transacciones, "retiro")
        return np.sum(montos) if montos.size > 0 else 0.0

    @staticmethod
    def ratio_dep_gastos(transacciones):
        dep = Estadisticas.total_depositos(transacciones)
        gas = Estadisticas.total_gastos(transacciones)
        return dep / gas if gas > 0 else float("inf")

    @staticmethod
    def desviacion_estandar(transacciones):
        montos = np.array([t["monto"] for t in transacciones], dtype=float)
        return np.std(montos) if montos.size > 0 else 0.0

    @staticmethod
    def percentiles(transacciones):
        montos = np.array([t["monto"] for t in transacciones], dtype=float)
        if montos.size == 0:
            return {"p50": 0, "p90": 0, "p99": 0}

        return {
            "p50": np.percentile(montos, 50),
            "p90": np.percentile(montos, 90),
            "p99": np.percentile(montos, 99),
        }

    @staticmethod
    def promedio_diario(transacciones):
        if not transacciones:
            return 0.0

        fechas = np.array([
            datetime.fromisoformat(t["fecha"]).date()
            for t in transacciones
        ])

        dias_unicos = np.unique(fechas)

        return len(transacciones) / len(dias_unicos)

    # RESUMEN COMPLETO POR CUENTA
    

    @staticmethod
    def resumen_por_cuenta(transacciones):
        """
        Devuelve un diccionario con TODAS las métricas solicitadas.
        """
        return {
            "total_depositos": Estadisticas.total_depositos(transacciones),
            "total_gastos": Estadisticas.total_gastos(transacciones),
            "ratio_dep_gastos": Estadisticas.ratio_dep_gastos(transacciones),
            "promedio_diario": Estadisticas.promedio_diario(transacciones),
            "desviacion_estandar": Estadisticas.desviacion_estandar(transacciones),
            "percentiles": Estadisticas.percentiles(transacciones)
        }

   
    # MÉTRICAS GLOBALES DEL BANCO (para dashboard)
    

    @staticmethod
    def transacciones_por_dia(transacciones):
        """
        Devuelve un diccionario:
        { fecha: cantidad_de_transacciones }
        """
        fechas = np.array([
            datetime.fromisoformat(t["fecha"]).date()
            for t in transacciones
        ])

        unicas, conteos = np.unique(fechas, return_counts=True)

        return dict(zip(unicas, conteos))

    @staticmethod
    def total_diario(transacciones):
        """
        Devuelve:
        { fecha: {depositos: x, gastos: y, neto: z} }
        """
        fechas = np.array([
            datetime.fromisoformat(t["fecha"]).date()
            for t in transacciones
        ])

        montos = np.array([t["monto"] for t in transacciones])
        tipos = np.array([t["tipo"] for t in transacciones])

        dias = np.unique(fechas)
        resultado = {}

        for dia in dias:
            mask = fechas == dia
            montos_dia = montos[mask]
            tipos_dia = tipos[mask]

            dep = np.sum(montos_dia[tipos_dia == "deposito"])
            gas = np.sum(montos_dia[tipos_dia == "retiro"])

            resultado[dia] = {
                "depositos": dep,
                "gastos": gas,
                "neto": dep - gas
            }

        return resultado

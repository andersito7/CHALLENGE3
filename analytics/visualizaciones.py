import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from collections import defaultdict

class Visualizador:
    def __init__(self):
        self.df = pd.read_csv("data/transferencias.csv")
        self.df["fecha"] = pd.to_datetime(self.df["fecha"])
        self.df["hora"] = self.df["fecha"].dt.hour
        self.df["dia_semana"] = self.df["fecha"].dt.day_name()

        os.makedirs("outputs/plots", exist_ok=True)

    def serie_temporal(self):
        datos = self.df.groupby(self.df["fecha"].dt.date)["monto"].sum()
        if datos.empty:
            print("⚠️ No hay datos para la serie temporal.")
            return

        fechas = datos.index
        netos = datos.values

        plt.figure(figsize=(10, 5))
        plt.plot(fechas, netos, marker="o")
        plt.title("Serie temporal del banco")
        plt.xlabel("Fecha")
        plt.ylabel("Monto total por día")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("outputs/plots/serie_temporal.png")
        plt.close()

    def heatmap_actividad(self):
        tabla = self.df.groupby(["dia_semana", "hora"]).size().unstack(fill_value=0)
        if tabla.empty:
            print("⚠️ No hay suficientes datos para generar el heatmap.")
            return

        orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        tabla = tabla.reindex(orden_dias)
        plt.figure(figsize=(12, 6))
        sns.heatmap(tabla, cmap="YlGnBu", linewidths=0.5)
        plt.title("Heatmap de actividad (hora vs día)")
        plt.xlabel("Hora del día")
        plt.ylabel("Día de la semana")
        plt.tight_layout()
        plt.savefig("outputs/plots/heatmap_actividad.png")
        plt.close()

    def boxplot_cuentas(self):
        if "tipo_cuenta" not in self.df.columns:
            print("⚠️ La columna 'tipo_cuenta' no está disponible.")
            return

        plt.figure(figsize=(8, 6))
        sns.boxplot(data=self.df, x="tipo_cuenta", y="monto")
        plt.title("Distribución de montos por tipo de cuenta")
        plt.xlabel("Tipo de cuenta")
        plt.ylabel("Monto")
        plt.tight_layout()
        plt.savefig("outputs/plots/boxplot_cuentas.png")
        plt.close()

    def scatter_depositos_vs_gastos(self):
        try:
            df_trans = pd.read_csv("data/transacciones.csv", header=0)
            df_trans["fecha"] = pd.to_datetime(df_trans["fecha"], errors="coerce")

            cuentas = defaultdict(lambda: {"depositos": 0, "gastos": 0})
            for _, t in df_trans.iterrows():
                if t["tipo"] == "deposito":
                    cuentas[t["cuenta_id"]]["depositos"] += t["monto"]
                elif t["tipo"] == "retiro":
                    cuentas[t["cuenta_id"]]["gastos"] += t["monto"]

            df_cuentas = pd.DataFrame([
                {"cuenta_id": cid, "depositos": v["depositos"], "gastos": v["gastos"]}
                for cid, v in cuentas.items()
                if v["depositos"] > 0 and v["gastos"] > 0
            ])

            if df_cuentas.empty:
                print("⚠️ No hay datos suficientes para generar el gráfico de depósitos vs gastos.")
                return

            plt.figure(figsize=(8, 6))
            ax = sns.scatterplot(data=df_cuentas, x="depositos", y="gastos")

            # Agregar etiquetas a cada punto
            for _, row in df_cuentas.iterrows():
                ax.text(row["depositos"] + 5, row["gastos"], row["cuenta_id"], fontsize=9)

            plt.title("Relación entre depósitos y gastos por cuenta")
            plt.xlabel("Total depositado")
            plt.ylabel("Total retirado")
            plt.tight_layout()
            plt.savefig("outputs/plots/scatter_depositos_vs_gastos.png")
            plt.close()
        except Exception as e:
            print(f"⚠️ Error al generar el gráfico de depósitos vs gastos: {e}")

import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

class GrafoTransacciones:
    def __init__(self):
        self.df = pd.read_csv("data/transferencias.csv")
        self.G = nx.DiGraph()
        os.makedirs("outputs/plots", exist_ok=True)

    def construir_grafo(self):
        for _, fila in self.df.iterrows():
            origen = fila["cuenta_origen"]
            destino = fila["cuenta_destino"]
            monto = fila["monto"]

            if self.G.has_edge(origen, destino):
                self.G[origen][destino]["peso"] += monto
                self.G[origen][destino]["cantidad"] += 1
            else:
                self.G.add_edge(origen, destino, peso=monto, cantidad=1)

    def visualizar_grafo(self):
        if self.G.number_of_nodes() == 0:
            print("⚠️ El grafo está vacío. ¿Ejecutaste construir_grafo()?")
            return

        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(self.G, seed=42)
        pesos = [self.G[u][v]["peso"] for u, v in self.G.edges()]
        nx.draw(self.G, pos, with_labels=True, node_size=700, node_color="skyblue", edge_color="gray", width=2)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels={(u, v): f'{d["peso"]:.0f}' for u, v, d in self.G.edges(data=True)})
        plt.title("Grafo de transferencias entre cuentas")
        plt.tight_layout()
        plt.savefig("outputs/plots/grafo_transferencias.png")
        plt.close()

    def resumen_metricas(self):
        print("📊 Métricas del grafo:")
        print(f"➡️ Nodos: {self.G.number_of_nodes()}")
        print(f"➡️ Aristas: {self.G.number_of_edges()}")

        grados = dict(self.G.degree())
        print("🔗 Grado por nodo:")
        for nodo, grado in grados.items():
            print(f"  - Cuenta {nodo}: grado {grado}")

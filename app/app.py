from sdk.moveapps_spec import hook_impl
from sdk.moveapps_io import MoveAppsIo
from movingpandas import TrajectoryCollection
import logging
import pandas as pd
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2

class App(object):
    def __init__(self, moveapps_io):
        self.moveapps_io = moveapps_io

    @hook_impl
    def execute(self, data: TrajectoryCollection, config: dict) -> TrajectoryCollection:
        logging.info("Wildlife Movement Statistics App — starting")

        gdf = data.to_point_gdf().copy()
        gdf = gdf.sort_index()
        id_col = data.get_traj_id_col()

        resultados = []

        for individuo in gdf[id_col].unique():
            df_ind = gdf[gdf[id_col] == individuo].copy()
            coords = list(zip(df_ind.geometry.y, df_ind.geometry.x))
            distancia = sum(
                self._haversine(coords[i][0], coords[i][1], coords[i+1][0], coords[i+1][1])
                for i in range(len(coords) - 1)
            )
            resultados.append({
                "individuo": str(individuo),
                "registros": len(df_ind),
                "distancia_km": round(distancia, 3),
                "primer_registro": str(df_ind.index.min()),
                "ultimo_registro": str(df_ind.index.max()),
            })

        df_stats = pd.DataFrame(resultados)
        logging.info(f"\n{df_stats.to_string(index=False)}")

        csv_file = self.moveapps_io.create_artifacts_file("movement_stats.csv")
        df_stats.to_csv(csv_file, index=False)
        logging.info(f"Stats saved to {csv_file}")

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(df_stats["individuo"], df_stats["distancia_km"], color="steelblue", edgecolor="black")
        ax.set_title("Total distance per individual", fontsize=13, fontweight="bold")
        ax.set_xlabel("Individual")
        ax.set_ylabel("Distance (km)")
        plt.tight_layout()
        plot_file = self.moveapps_io.create_artifacts_file("distance_plot.png")
        plt.savefig(plot_file)
        logging.info(f"Plot saved to {plot_file}")

        return data

    def _haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        a = sin((lat2-lat1)/2)**2 + cos(lat1)*cos(lat2)*sin((lon2-lon1)/2)**2
        return R * 2 * atan2(sqrt(a), sqrt(1-a))

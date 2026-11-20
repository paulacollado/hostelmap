"""Construcción de las variables del modelo.

Replica la lógica de notebooks/08_modelo_base.ipynb para una fecha de origen
concreta, de modo que la app pueda predecir con los datos más recientes.
"""
import pandas as pd

VARIABLES_ESTATICAS = ["categoria", "n_100m", "n_250m", "n_500m",
                       "n_mismo_tipo_250m", "dist_vecino_m"]


def tablas_anchas(panel: pd.DataFrame) -> dict:
    """Pasa el panel largo a tablas local x fecha."""
    return {
        "resenas": panel.pivot(index="id_local", columns="fecha", values="n_reviews"),
        "score": panel.pivot(index="id_local", columns="fecha", values="score"),
        "precio": panel.pivot(index="id_local", columns="fecha", values="precio_medio"),
    }


def variables_en_origen(panel: pd.DataFrame, k: int) -> pd.DataFrame:
    """Variables del modelo tomando como origen la fecha número k (k >= 2)."""
    t = tablas_anchas(panel)
    fechas = list(t["resenas"].columns)
    dias = pd.Series(pd.to_datetime(fechas)).diff().dt.days.values
    rev, sco, pre = t["resenas"], t["score"], t["precio"]

    d = pd.DataFrame(index=rev.index)
    d["resenas"] = rev.iloc[:, k]
    d["score"] = sco.iloc[:, k]
    d["precio"] = pre.iloc[:, k]
    d["vel_1"] = ((rev.iloc[:, k] - rev.iloc[:, k - 1]) / dias[k]).clip(lower=0) * 30
    d["vel_2"] = ((rev.iloc[:, k] - rev.iloc[:, k - 2])
                  / (dias[k] + dias[k - 1])).clip(lower=0) * 30
    d["cambio_score"] = sco.iloc[:, k] - sco.iloc[:, k - 2]

    estaticas = panel.groupby("id_local")[VARIABLES_ESTATICAS].first()
    d = d.join(estaticas)
    d["categoria"] = d["categoria"].astype("category")
    return d

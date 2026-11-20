"""Genera los ficheros ligeros que usa la app a partir del panel completo.

Uso (desde la raíz del repo):
    python scripts/preparar_datos_app.py

Crea:
    data/app/locales.parquet  -> una fila por local con su último estado y sus variables
    data/app/serie.parquet    -> evolución de reseñas y puntuación por local y fecha
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.config import DATOS_APP, LOCALES_PARQUET, PANEL_CSV, SERIE_PARQUET  # noqa: E402
from src.variables import variables_en_origen  # noqa: E402


def main() -> None:
    panel = pd.read_csv(PANEL_CSV, parse_dates=["fecha"])
    panel = panel.sort_values(["id_local", "fecha"])
    ultima = panel["fecha"].max()
    n_fechas = panel["fecha"].nunique()

    # Último estado de cada local (nombre, posición, reseñas, puntuación, precio)
    ficha = (panel[panel["fecha"] == ultima]
             .set_index("id_local")[["nombre", "lat", "lon", "n_reviews", "score",
                                     "precio", "precio_medio", "tags"]]
             .rename(columns={"precio": "rango_precio"}))

    # Variables del modelo con la última fecha como origen
    variables = variables_en_origen(panel, k=n_fechas - 1)
    variables = variables.drop(columns=["resenas", "score", "precio"])

    locales = ficha.join(variables).reset_index()
    locales["fecha_datos"] = ultima

    serie = panel[["id_local", "fecha", "n_reviews", "score"]].reset_index(drop=True)

    DATOS_APP.mkdir(parents=True, exist_ok=True)
    locales.to_parquet(LOCALES_PARQUET, index=False)
    serie.to_parquet(SERIE_PARQUET, index=False)
    print(f"{len(locales)} locales -> {LOCALES_PARQUET}")
    print(f"{len(serie)} filas de evolución -> {SERIE_PARQUET}")


if __name__ == "__main__":
    main()

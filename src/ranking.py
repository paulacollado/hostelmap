"""Ranking de bares "en racha" según la predicción del modelo."""
import pandas as pd

from src.config import NIVELES_ACTIVIDAD

MIN_RESENAS_RANKING = 100  # evita que un bar con 3 reseñas aparezca con +300 %


def nivel_actividad(prediccion: pd.Series) -> pd.Series:
    """Clasifica la predicción en quintiles: Muy baja ... Muy alta."""
    rango = prediccion.rank(method="first", pct=True)
    return pd.cut(rango, bins=[0, .2, .4, .6, .8, 1], labels=NIVELES_ACTIVIDAD)


def tabla_en_racha(locales: pd.DataFrame, criterio: str, n: int = 10) -> pd.DataFrame:
    """Top n locales por reseñas previstas o por crecimiento relativo."""
    t = locales[locales["n_reviews"] >= MIN_RESENAS_RANKING].copy()
    t["crecimiento"] = t["prediccion_30d"] / t["n_reviews"] * 100
    columna = "prediccion_30d" if criterio == "Reseñas previstas" else "crecimiento"
    t = t.nlargest(n, columna)
    return t[["id_local", "nombre", "categoria", "n_reviews", "prediccion_30d",
              "crecimiento"]].reset_index(drop=True)

"""Predicción de reseñas nuevas cada 30 días."""
import pandas as pd

# Nombre de cada variable del modelo -> columna de la tabla de locales de la app
COLUMNAS_APP = {"resenas": "n_reviews", "precio": "precio_medio"}


def predecir(paquete: dict, locales: pd.DataFrame) -> pd.Series:
    """Reseñas nuevas previstas por cada 30 días (nunca negativas)."""
    variables = paquete["variables"]
    X = pd.DataFrame({v: locales[COLUMNAS_APP.get(v, v)] for v in variables})
    pred = paquete["modelo"].predict(X)
    return pd.Series(pred, index=locales.index).clip(lower=0)

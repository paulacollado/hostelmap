"""Pruebas básicas: variables del modelo, ranking y arranque de la app.

Ejecutar desde la raíz del repo:  python -m pytest
"""
from pathlib import Path

import pandas as pd
from streamlit.testing.v1 import AppTest

from src.ranking import nivel_actividad, tabla_en_racha
from src.variables import variables_en_origen


def panel_de_prueba() -> pd.DataFrame:
    """Dos locales y cuatro fechas con valores conocidos."""
    fechas = pd.to_datetime(["2026-01-01", "2026-01-31", "2026-03-02", "2026-04-01"])
    filas = []
    for id_local, resenas in [("a", [100, 130, 160, 190]), ("b", [50, 50, 40, 60])]:
        for f, r in zip(fechas, resenas):
            filas.append({"id_local": id_local, "fecha": f, "n_reviews": r, "score": 4.5,
                          "precio_medio": 15.0, "categoria": "Bar", "n_100m": 1,
                          "n_250m": 2, "n_500m": 3, "n_mismo_tipo_250m": 1,
                          "dist_vecino_m": 10.0})
    return pd.DataFrame(filas)


def test_ritmo_de_resenas_cada_30_dias():
    v = variables_en_origen(panel_de_prueba(), k=3)
    assert v.loc["a", "vel_1"] == 30          # +30 reseñas en 30 días
    assert v.loc["a", "vel_2"] == 30          # +60 reseñas en 60 días
    assert v.loc["b", "vel_2"] >= 0           # nunca negativo aunque bajen las reseñas


def test_niveles_de_actividad_equilibrados():
    niveles = nivel_actividad(pd.Series(range(100), dtype=float))
    assert niveles.value_counts().tolist() == [20] * 5


def test_ranking_excluye_locales_pequenos():
    locales = pd.DataFrame({"id_local": ["a", "b"], "nombre": ["A", "B"],
                            "categoria": ["Bar", "Bar"], "n_reviews": [50, 500],
                            "prediccion_30d": [40.0, 10.0]})
    ranking = tabla_en_racha(locales, "Crecimiento relativo")
    assert list(ranking["id_local"]) == ["b"]


def test_la_app_arranca_sin_errores():
    app = AppTest.from_file(str(Path(__file__).parent.parent / "app.py"),
                            default_timeout=60).run()
    assert not app.exception
    assert app.metric[0].value == "2.029"

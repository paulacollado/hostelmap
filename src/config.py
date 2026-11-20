"""Rutas y constantes compartidas por toda la app."""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# Datos de origen (no se suben a GitHub)
PANEL_CSV = RAIZ / "data" / "madrid_panel_prox.csv"

# Datos ligeros que usa la app (los genera scripts/preparar_datos_app.py)
DATOS_APP = RAIZ / "data" / "app"
LOCALES_PARQUET = DATOS_APP / "locales.parquet"
SERIE_PARQUET = DATOS_APP / "serie.parquet"

MODELO = RAIZ / "models" / "modelo_base.joblib"

# Centro del mapa (Puerta del Sol)
CENTRO_MADRID = {"lat": 40.4168, "lon": -3.7038}

# Un color fijo por categoría para que el mapa y las gráficas coincidan
COLORES_CATEGORIA = {
    "Bar": "#E4572E",
    "Bar de tapas y taberna": "#F3A712",
    "Cervecería": "#29335C",
    "Ocio nocturno y copas": "#A855F7",
    "Vinos y sidra": "#8B1E3F",
    "Restaurante": "#669BBC",
}

# Por encima de este ritmo (reseñas / 30 días, percentil 99 del entrenamiento) el modelo
# tiene muy pocos ejemplos y tiende a quedarse corto: la ficha lo avisa.
RITMO_FUERA_DE_RANGO = 53

"""Mapa de locales con Plotly."""
import pandas as pd
import plotly.express as px

from src.config import CENTRO_MADRID, COLORES_CATEGORIA


def mapa_locales(locales: pd.DataFrame):
    fig = px.scatter_map(
        locales, lat="lat", lon="lon", color="categoria",
        color_discrete_map=COLORES_CATEGORIA,
        hover_name="nombre",
        hover_data={"n_reviews": True, "score": True, "lat": False, "lon": False,
                    "categoria": False},
        labels={"n_reviews": "Reseñas", "score": "Puntuación", "categoria": "Categoría"},
        center=CENTRO_MADRID, zoom=11.5, height=560, map_style="carto-positron",
    )
    fig.update_traces(marker={"size": 7, "opacity": 0.8})
    fig.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0},
                      legend={"orientation": "h", "y": -0.02, "title": None})
    return fig

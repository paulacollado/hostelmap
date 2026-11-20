"""Mapa de locales con Plotly."""
import pandas as pd
import plotly.express as px

from src.config import CENTRO_MADRID, COLORES_CATEGORIA


def mapa_locales(locales: pd.DataFrame, id_seleccionado: str | None = None):
    """Mapa por categoría. Cada punto lleva su id_local para poder seleccionarlo."""
    fig = px.scatter_map(
        locales, lat="lat", lon="lon", color="categoria",
        color_discrete_map=COLORES_CATEGORIA,
        custom_data=["id_local"],
        hover_name="nombre",
        hover_data={"n_reviews": ":.0f", "score": ":.1f", "lat": False, "lon": False,
                    "categoria": False},
        labels={"n_reviews": "Reseñas", "score": "Puntuación", "categoria": "Categoría"},
        center=CENTRO_MADRID, zoom=11.5, height=600, map_style="carto-positron",
    )
    fig.update_traces(marker={"size": 8, "opacity": 0.8})

    # Resalta el local seleccionado con un anillo
    if id_seleccionado is not None and id_seleccionado in set(locales["id_local"]):
        sel = locales[locales["id_local"] == id_seleccionado]
        fig.add_scattermap(lat=sel["lat"], lon=sel["lon"], mode="markers",
                           marker={"size": 20, "color": "#111111", "opacity": 0.35},
                           hoverinfo="skip", showlegend=False)
        fig.update_layout(map_center={"lat": float(sel["lat"].iloc[0]),
                                      "lon": float(sel["lon"].iloc[0])})

    fig.update_layout(margin={"l": 0, "r": 0, "t": 0, "b": 0},
                      legend={"orientation": "h", "y": -0.02, "title": None},
                      clickmode="event+select")
    return fig


def id_desde_seleccion(evento) -> str | None:
    """Devuelve el id_local del punto en el que se ha hecho clic (o None)."""
    puntos = (evento or {}).get("selection", {}).get("points", [])
    for p in puntos:
        datos = p.get("customdata")
        if datos:
            return datos[0]
    return None

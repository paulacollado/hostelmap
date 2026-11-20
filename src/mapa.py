"""Mapa de locales con Plotly."""
import pandas as pd
import plotly.express as px

from src.config import (CENTRO_MADRID, COLORES_ACTIVIDAD, COLORES_CATEGORIA,
                        NIVELES_ACTIVIDAD)


def mapa_locales(locales: pd.DataFrame, id_seleccionado: str | None = None,
                 por_actividad: bool = False):
    """Mapa de locales coloreado por categoría o por actividad prevista.

    Cada punto lleva su id_local para poder seleccionarlo con un clic.
    """
    if por_actividad:
        # Los menos activos primero, para que los "en racha" queden dibujados encima
        locales = locales.sort_values("prediccion_30d")
        color, colores, orden = "actividad", COLORES_ACTIVIDAD, NIVELES_ACTIVIDAD
    else:
        color, colores, orden = "categoria", COLORES_CATEGORIA, None

    fig = px.scatter_map(
        locales, lat="lat", lon="lon", color=color,
        color_discrete_map=colores,
        category_orders={"actividad": orden} if orden else None,
        custom_data=["id_local"],
        hover_name="nombre",
        hover_data={"categoria": True, "n_reviews": ":.0f", "score": ":.1f",
                    "prediccion_30d": ":.1f", "lat": False, "lon": False,
                    "actividad": False},
        labels={"n_reviews": "Reseñas", "score": "Puntuación", "categoria": "Categoría",
                "prediccion_30d": "Previstas / 30 días", "actividad": "Actividad prevista"},
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

    fig.update_layout(separators=",.", margin={"l": 0, "r": 0, "t": 30, "b": 0},
                      legend={"orientation": "h", "x": 0, "y": 1.0, "yanchor": "bottom",
                              "title": None, "bgcolor": "rgba(255,255,255,0)"},
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

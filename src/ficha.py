"""Ficha de un local: datos actuales, evolución y predicción."""
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src.config import COLORES_CATEGORIA, RITMO_FUERA_DE_RANGO


def _num(x: float, decimales: int = 0) -> str:
    """Formato numérico español: 1.234,5"""
    return f"{x:,.{decimales}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def grafica_evolucion(serie_local: pd.DataFrame, prediccion_30d: float, color: str):
    """Reseñas acumuladas en el tiempo + tramo previsto a 30 días."""
    ultima = serie_local.iloc[-1]
    fecha_pred = ultima["fecha"] + pd.Timedelta(days=30)
    valor_pred = ultima["n_reviews"] + prediccion_30d

    fig = go.Figure()
    fig.add_scatter(x=serie_local["fecha"], y=serie_local["n_reviews"], mode="lines+markers",
                    name="Reseñas", line={"color": color, "width": 3},
                    hovertemplate="%{x|%d/%m/%Y}<br>%{y:.0f} reseñas<extra></extra>")
    fig.add_scatter(x=[ultima["fecha"], fecha_pred], y=[ultima["n_reviews"], valor_pred],
                    mode="lines+markers", name="Predicción",
                    line={"color": color, "width": 3, "dash": "dot"},
                    marker={"symbol": ["circle", "star"], "size": [6, 14]},
                    hovertemplate="%{x|%d/%m/%Y}<br>%{y:.0f} reseñas (previsto)<extra></extra>")
    fig.update_layout(separators=",.", height=260, margin={"l": 0, "r": 0, "t": 10, "b": 0},
                      showlegend=False, yaxis_title=None, xaxis_title=None,
                      hovermode="x unified")
    return fig


def mostrar_ficha(local: pd.Series, serie_local: pd.DataFrame, locales: pd.DataFrame) -> None:
    color = COLORES_CATEGORIA.get(local["categoria"], "#E4572E")

    st.subheader(local["nombre"], anchor=False)
    precio = local["rango_precio"] if pd.notna(local["rango_precio"]) else "precio sin datos"
    st.caption(f"{local['categoria']} · {precio}")

    c1, c2, c3 = st.columns(3)
    primera = serie_local.iloc[0]
    c1.metric("Reseñas", _num(local["n_reviews"]),
              delta=f"+{_num(local['n_reviews'] - primera['n_reviews'])}",
              help="Cambio desde abril de 2025")
    cambio_score = local["score"] - primera["score"]
    c2.metric("Puntuación", _num(local["score"], 1),
              delta=_num(cambio_score, 1) if abs(cambio_score) >= 0.05 else None,
              help="Cambio desde abril de 2025")
    c3.metric("Previstas / 30 días", _num(local["prediccion_30d"], 1),
              help="Reseñas nuevas que el modelo espera en los próximos 30 días")
    st.caption(f"Ritmo de los últimos meses: **{_num(local['vel_2'], 1)} reseñas / 30 días**")
    if local["vel_2"] > RITMO_FUERA_DE_RANGO:
        st.warning("Este bar tiene muchísimo más movimiento que casi todos los del histórico. "
                   "Con tan pocos casos parecidos, el modelo tiende a quedarse corto: toma la "
                   "predicción como un mínimo.", icon="⚠️")

    st.plotly_chart(grafica_evolucion(serie_local, local["prediccion_30d"], color),
                    width="stretch", config={"displayModeBar": False})

    # Comparación con su categoría
    misma = locales[locales["categoria"] == local["categoria"]]
    percentil = (misma["prediccion_30d"] < local["prediccion_30d"]).mean() * 100
    ranking = (f"**Más activo que el {percentil:.0f} %** de los locales de su categoría"
               if percentil < 99.5 else "**El más activo** de su categoría")
    st.markdown(f"{ranking} según la predicción. Tiene **{local['n_100m']:.0f} locales "
                f"a 100 m** y {local['n_500m']:.0f} a 500 m.")

    etiquetas = [t for t in str(local["tags"]).split(";") if t]
    if etiquetas:
        st.caption("Etiquetas: " + " · ".join(etiquetas))

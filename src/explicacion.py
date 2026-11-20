"""Sección "Cómo funciona": datos, modelo y validación.

Las cifras de validación e importancia salen de notebooks/08_modelo_base.ipynb
(entrenamiento hasta el 27/03/2026, prueba de abril a septiembre de 2026).
"""
import pandas as pd
import plotly.express as px
import streamlit as st

# Error medio absoluto (reseñas / 30 días) en el periodo de prueba
MAE_PRUEBA = pd.DataFrame({
    "metodo": ["Predecir 0", "Mediana histórica", "Repetir último ritmo",
               "Repetir ritmo de 2 fechas", "Modelo HostelMap"],
    "mae": [5.94, 5.63, 5.60, 4.23, 4.02],
})

# Importancia por permutación (aumento del error al desordenar cada variable)
IMPORTANCIA = pd.DataFrame({
    "variable": ["Ritmo de las 2 últimas fechas", "Nº de reseñas",
                 "Ritmo de la última fecha", "Locales a 500 m", "Puntuación"],
    "importancia": [1.447, 0.656, 0.039, 0.033, 0.013],
})


def _barras(df: pd.DataFrame, x: str, y: str, destacar: str | None, titulo_x: str):
    colores = ["#E4572E" if v == destacar else "#C9CED6" for v in df[y]]
    fig = px.bar(df, x=x, y=y, orientation="h", text=x)
    fig.update_traces(marker_color=colores, texttemplate="%{text:.2f}",
                      textposition="outside", cliponaxis=False,
                      hovertemplate="%{y}: %{x:.3f}<extra></extra>")
    fig.update_layout(height=230, margin={"l": 0, "r": 30, "t": 0, "b": 0},
                      separators=",.",  # decimales con coma, como en el resto de la app
                      xaxis_title=titulo_x, yaxis_title=None,
                      yaxis={"categoryorder": "array", "categoryarray": list(df[y])[::-1]})
    return fig


def mostrar_como_funciona() -> None:
    with st.expander("🧠 ¿Cómo funciona HostelMap?"):
        st.markdown(
            "**Datos.** 18 fotografías de los bares y restaurantes de Madrid entre abril de "
            "2025 y septiembre de 2026. Solo se usan los **2.029 locales presentes en todas "
            "las fechas**, clasificados en categorías a partir de sus etiquetas. A cada uno "
            "se le calcula su entorno: cuántos locales tiene a 100, 250 y 500 m.\n\n"
            "**Modelo.** Un *gradient boosting* (`HistGradientBoostingRegressor`) predice "
            "las **reseñas nuevas que tendrá cada bar en los próximos 30 días** a partir de "
            "su ritmo reciente, su tamaño, su puntuación, su precio y su entorno.\n\n"
            "**Validación.** Se entrenó con datos hasta marzo de 2026 y se puso a prueba con "
            "lo que pasó de abril a septiembre, datos que el modelo no había visto."
        )
        c1, c2 = st.columns(2)
        c1.markdown("**Error medio en la prueba** (reseñas / 30 días, menos es mejor)")
        c1.plotly_chart(_barras(MAE_PRUEBA, "mae", "metodo", "Modelo HostelMap", None),
                        width="stretch", config={"displayModeBar": False})
        c1.caption("El modelo mejora un 5 % a la mejor regla simple.")
        c2.markdown("**Qué mira más el modelo**")
        c2.plotly_chart(_barras(IMPORTANCIA, "importancia", "variable",
                                "Ritmo de las 2 últimas fechas", None),
                        width="stretch", config={"displayModeBar": False})
        c2.caption("El ritmo reciente manda, y el entorno (locales a 500 m) también cuenta.")
        st.markdown(
            "**Limitaciones.** El modelo no predice aperturas ni cierres, porque solo "
            "incluye locales que existen en todas las fechas. En los pocos bares con un "
            "movimiento extraordinario (más de 53 reseñas al mes) tiende a quedarse corto, "
            "y la ficha lo avisa."
        )

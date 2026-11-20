"""HostelMap · El pulso de los bares de Madrid.

Ejecutar en local:  streamlit run app.py
"""
import streamlit as st

from src.datos import cargar_locales, cargar_modelo
from src.mapa import mapa_locales
from src.modelo import predecir

st.set_page_config(page_title="HostelMap · Bares de Madrid", page_icon="🍻", layout="wide")

locales = cargar_locales()
locales["prediccion_30d"] = predecir(cargar_modelo(), locales)

# --- Barra lateral: filtros ---
st.sidebar.header("Filtros")
categorias = sorted(locales["categoria"].cat.categories)
elegidas = st.sidebar.multiselect("Categoría", categorias, default=categorias)
vista = locales[locales["categoria"].isin(elegidas)]

# --- Cabecera ---
st.title("🍻 HostelMap")
st.caption(f"El pulso de {len(locales):,} bares de Madrid · datos a "
           f"{locales['fecha_datos'].max():%d/%m/%Y}".replace(",", "."))

c1, c2, c3, c4 = st.columns(4)
c1.metric("Locales mostrados", f"{len(vista):,}".replace(",", "."))
c2.metric("Mediana de reseñas", f"{vista['n_reviews'].median():.0f}")
c3.metric("Puntuación media", f"{vista['score'].mean():.2f}".replace(".", ","))
c4.metric("Reseñas nuevas previstas / 30 días",
          f"{vista['prediccion_30d'].sum():,.0f}".replace(",", "."))

st.plotly_chart(mapa_locales(vista), width="stretch")

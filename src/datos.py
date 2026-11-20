"""Carga de datos y del modelo, con caché de Streamlit."""
import joblib
import pandas as pd
import streamlit as st

from src.config import LOCALES_PARQUET, MODELO, SERIE_PARQUET


@st.cache_data
def cargar_locales() -> pd.DataFrame:
    locales = pd.read_parquet(LOCALES_PARQUET)
    locales["categoria"] = locales["categoria"].astype("category")
    return locales


@st.cache_data
def cargar_serie() -> pd.DataFrame:
    return pd.read_parquet(SERIE_PARQUET)


@st.cache_resource
def cargar_modelo() -> dict:
    """Devuelve {'modelo': HistGradientBoostingRegressor, 'variables': [...]}."""
    return joblib.load(MODELO)

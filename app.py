"""HostelMap · El pulso de los bares de Madrid.

Ejecutar en local:  streamlit run app.py
"""
import streamlit as st

from src.config import RITMO_FUERA_DE_RANGO
from src.datos import cargar_locales, cargar_modelo, cargar_serie
from src.ficha import _num, mostrar_ficha
from src.mapa import id_desde_seleccion, mapa_locales
from src.modelo import predecir
from src.ranking import nivel_actividad, tabla_en_racha

st.set_page_config(page_title="HostelMap · Bares de Madrid", page_icon="🍻", layout="wide")


@st.cache_data
def locales_con_prediccion():
    locales = cargar_locales().copy()
    locales["prediccion_30d"] = predecir(cargar_modelo(), locales)
    locales["actividad"] = nivel_actividad(locales["prediccion_30d"])
    return locales


locales = locales_con_prediccion()
serie = cargar_serie()

# --- Estado: local seleccionado (por clic en el mapa o por el buscador) ---
# Al abrir, el bar con más actividad prevista dentro del rango fiable del modelo
if "id_sel" not in st.session_state:
    fiables = locales[locales["vel_2"] <= RITMO_FUERA_DE_RANGO]
    st.session_state.id_sel = fiables.loc[fiables["prediccion_30d"].idxmax(), "id_local"]


def _al_buscar():
    st.session_state.id_sel = st.session_state.buscador


def _seleccionar(id_local: str | None, origen: str) -> None:
    """Selecciona un local desde el mapa o el ranking (solo si es un clic nuevo)."""
    if id_local and id_local != st.session_state.get(f"ultimo_{origen}"):
        st.session_state[f"ultimo_{origen}"] = id_local
        st.session_state.id_sel = id_local
        st.rerun()


# --- Barra lateral: filtros ---
with st.sidebar:
    st.header("Filtros")
    categorias = list(locales["categoria"].value_counts().index)
    elegidas = st.pills("Categoría", categorias, selection_mode="multi", default=categorias)
    min_resenas = st.slider("Mínimo de reseñas", 0, 1000, 0, step=50)

vista = locales[locales["categoria"].isin(elegidas or categorias)
                & (locales["n_reviews"] >= min_resenas)]

# --- Cabecera ---
st.title("🍻 HostelMap")
st.caption(f"El pulso de {_num(len(locales))} bares de Madrid · datos a "
           f"{locales['fecha_datos'].max():%d/%m/%Y}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Locales mostrados", _num(len(vista)))
c2.metric("Mediana de reseñas", _num(vista["n_reviews"].median()))
c3.metric("Puntuación media", _num(vista["score"].mean(), 2))
c4.metric("Reseñas nuevas previstas / 30 días", _num(vista["prediccion_30d"].sum()))

# --- Mapa + ficha ---
col_mapa, col_ficha = st.columns([3, 2], gap="large")

with col_mapa:
    modo = st.segmented_control("Colorear por", ["Categoría", "🔥 Actividad prevista"],
                                default="Categoría", label_visibility="collapsed")
    st.caption("Haz clic en un bar para ver su ficha")
    figura = mapa_locales(vista, st.session_state.id_sel,
                          por_actividad=(modo == "🔥 Actividad prevista"))
    evento = st.plotly_chart(figura, width="stretch", on_select="rerun",
                             selection_mode="points", key="mapa",
                             config={"scrollZoom": True, "displayModeBar": False})
    _seleccionar(id_desde_seleccion(evento), "mapa")

with col_ficha:
    opciones = vista.sort_values("nombre")
    ids = list(opciones["id_local"])
    nombres = dict(zip(opciones["id_local"], opciones["nombre"]))
    if st.session_state.id_sel in ids:
        st.session_state.buscador = st.session_state.id_sel
    st.selectbox("Busca un bar", ids, format_func=nombres.get, key="buscador",
                 on_change=_al_buscar, index=None, placeholder="Escribe un nombre…")

    seleccionado = locales[locales["id_local"] == st.session_state.id_sel]
    if seleccionado.empty:
        st.info("Selecciona un bar en el mapa o con el buscador.")
    else:
        local = seleccionado.iloc[0]
        serie_local = serie[serie["id_local"] == local["id_local"]].sort_values("fecha")
        mostrar_ficha(local, serie_local, locales)

# --- Ranking de bares en racha ---
st.divider()
cab, criterio_col = st.columns([3, 2])
cab.subheader("🔥 Bares en racha")
cab.caption("Los que más reseñas nuevas ganarán en los próximos 30 días según el modelo "
            "(con al menos 100 reseñas y los filtros aplicados). Haz clic en una fila "
            "para ver su ficha.")
criterio = criterio_col.segmented_control("Ordenar por",
                                          ["Reseñas previstas", "Crecimiento relativo"],
                                          default="Reseñas previstas")
ranking = tabla_en_racha(vista, criterio or "Reseñas previstas")
seleccion = st.dataframe(
    ranking, hide_index=True, width="stretch", on_select="rerun",
    selection_mode="single-row", key="ranking",
    column_order=["nombre", "categoria", "n_reviews", "prediccion_30d", "crecimiento"],
    column_config={
        "nombre": "Bar",
        "categoria": "Categoría",
        "n_reviews": st.column_config.NumberColumn("Reseñas", format="localized"),
        "prediccion_30d": st.column_config.ProgressColumn(
            "Previstas / 30 días", format="%.0f", min_value=0,
            max_value=float(max(ranking["prediccion_30d"].max(), 1))),
        "crecimiento": st.column_config.NumberColumn("Crecimiento / 30 días",
                                                     format="+%.1f %%"),
    },
)
filas = seleccion.selection.rows if seleccion else []
if filas:
    _seleccionar(ranking.loc[filas[0], "id_local"], "ranking")

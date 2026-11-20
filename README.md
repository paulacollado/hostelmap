# 🍻 HostelMap · El pulso de los bares de Madrid

Aplicación web interactiva para explorar la distribución territorial y la evolución temporal de los bares de Madrid y anticipar qué locales van a ganar más reseñas.

> **App desplegada:** _próximamente_

## Descripción

HostelMap sitúa en un mapa **2.029 bares de Madrid** seguidos durante **18 fechas (abril 2025 – septiembre 2026)**. Permite filtrar por categoría, consultar la ficha de cada local con la evolución de sus reseñas y su puntuación, y ver la **predicción de reseñas nuevas para los próximos 30 días** que da un modelo de *machine learning* entrenado con el histórico.

## Objetivos

- Integrar datos de establecimientos hosteleros de diferentes periodos.
- Analizar la distribución territorial de la hostelería en Madrid.
- Clasificar los establecimientos en categorías homogéneas.
- Analizar la evolución temporal de reseñas, puntuación y precio.
- Integrar un modelo predictivo de la actividad (reseñas nuevas cada 30 días).
- Crear visualizaciones interactivas con Plotly.
- Desplegar la aplicación en una URL pública.

## Tecnologías

- Python 3.11 · Pandas · NumPy
- Plotly (mapa y gráficas)
- **Streamlit** (interfaz web) y Streamlit Community Cloud (despliegue)
- scikit-learn 1.9.1 (`HistGradientBoostingRegressor`)
- Git / GitHub

> **Cambio respecto a la propuesta:** la propuesta inicial planteaba Dash. Se ha optado por Streamlit porque permite desplegar gratis directamente desde GitHub e iterar más rápido sobre el diseño y la interacción, que son el foco de la aplicación.

## Datos y modelo

- **Origen:** 18 extracciones de bares y restaurantes de Madrid (coordenadas, nombre, etiquetas, nº de reseñas, puntuación y rango de precio), cedidas por el tutor del TFG.
- **Panel:** solo los locales presentes en las 18 fechas → 2.029 locales × 18 fechas (36.522 filas).
- **Categorías** (reglas sobre etiquetas): Bar, Bar de tapas y taberna, Cervecería, Ocio nocturno y copas, Vinos y sidra, Restaurante.
- **Proximidad:** nº de locales a 100, 250 y 500 m, del mismo tipo a 250 m y distancia al vecino más cercano.
- **Modelo:** `HistGradientBoostingRegressor` que predice las reseñas nuevas cada 30 días. Probado de abril a septiembre de 2026: **MAE 4,02** frente a 4,23 de la mejor referencia simple (mejora del 5 %).
- **Limitación:** al trabajar solo con locales presentes en todas las fechas, el modelo no predice aperturas ni cierres.

## Estructura del repositorio

```
app.py                       # Página principal de la app
src/
  config.py                  # Rutas, centro del mapa y colores por categoría
  datos.py                   # Carga de datos y del modelo (con caché)
  variables.py               # Variables del modelo (misma lógica que el notebook 08)
  modelo.py                  # Predicción de reseñas nuevas / 30 días
  mapa.py                    # Mapa de locales con Plotly
scripts/preparar_datos_app.py  # Genera data/app/ a partir del panel completo
data/app/                    # Datos ligeros que usa la app (parquet)
models/modelo_base.joblib    # Modelo entrenado
notebooks/                   # Construcción de variables y entrenamiento
```

## Cómo ejecutarla en local

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Para regenerar `data/app/` hacen falta los CSV originales en `data/` (no incluidos):

```bash
python scripts/preparar_datos_app.py
```

## Plan de trabajo

- [x] **Fase 1 — Preparación de los datos:** integración, limpieza, identificación de locales y categorías.
- [x] **Fase 2 — Análisis exploratorio:** distribución territorial, categorías, reseñas, puntuación y evolución.
- [x] **Fase 3 — Variables y modelo:** proximidad, velocidad de reseñas y modelo base.
- [ ] **Fase 4 — Desarrollo de la aplicación**
  - [x] Esqueleto de la app, indicadores y mapa por categoría
  - [ ] Ficha de cada local con su evolución
  - [ ] Predicción integrada en la ficha y en el mapa
  - [ ] Mejoras de diseño e interacción
- [ ] **Fase 5 — Validación y despliegue:** despliegue en URL pública, pruebas, documentación y presentación.

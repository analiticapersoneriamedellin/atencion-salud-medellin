# 🩺 Vigilancia de Atención Oportuna en Salud — Medellín

**Concurso Datos al Ecosistema 2026: IA para Colombia — Ministerio TIC**
**Reto:** Salud y Bienestar (ID 117) · **Equipo:** 330
**Para:** Personería Distrital de Medellín

## Descripción

Sistema de análisis de datos e inteligencia artificial que identifica patrones de demora, barreras de acceso y riesgos de vulneración del derecho a la salud en Medellín, a partir de los reportes oficiales de Peticiones, Quejas, Reclamos y Denuncias (PQRD) en salud publicados por la Superintendencia Nacional de Salud (Supersalud).

El proyecto integra 6 años de reportes (2021-2026), aplica un modelo de detección de anomalías (z-score) para identificar picos de riesgo por motivo de reclamo, y presenta los resultados en un dashboard interactivo, para apoyar la labor de vigilancia de derechos ciudadanos de la Personería Distrital de Medellín.

## Hallazgos principales

1. 📈 Los reclamos en salud en Medellín **casi se triplicaron** entre 2021 y 2025-2026 (+164%).
2. 🚨 **Septiembre de 2025** presentó una falla sistémica: 7 de 10 motivos de reclamo en riesgo alto simultáneamente.
3. ⚠️ **"Falta de oportunidad en referencia y contrarreferencia"** es un problema emergente con tendencia de crecimiento activo en 2026.

Ver el [informe descriptivo completo](reports/informe_descriptivo.md) para el detalle y las recomendaciones.

## Estructura del repositorio

```
├── docs/                       # Documentación técnica
│   ├── planteamiento_problema.md
│   ├── marco_metodologico.md   # Metodología CRISP-ML, supuestos y limitaciones
│   ├── fuentes_datos.md        # Datasets usados, con trazabilidad
│   └── data_dictionary.md      # Diccionario de variables
├── data/
│   ├── raw/                    # Reportes Excel originales de Supersalud
│   └── processed/              # Datos consolidados y listos para análisis
├── notebooks/                  # Análisis exploratorio paso a paso
├── src/
│   └── parse_pqrd.py           # Extracción robusta de datos desde los Excel
├── reports/
│   ├── figures/                # Gráficos exportados
│   └── informe_descriptivo.md  # Resultados y recomendaciones
└── dashboard/
    └── app.py                  # Dashboard interactivo (Streamlit)
```

## Cómo ejecutar el proyecto

```bash
pip install -r requirements.txt

# 1. Extraer y consolidar los datos (requiere los .xlsx en data/raw/)
python src/parse_pqrd.py

# 2. Ejecutar el dashboard interactivo
streamlit run dashboard/app.py
```

## Fuente de datos

Superintendencia Nacional de Salud (Supersalud) — Reportes PQRD en salud, 2021-2026. Ver [`docs/fuentes_datos.md`](docs/fuentes_datos.md) para el detalle completo con trazabilidad (IDs, fechas, licencia).

## Metodología

CRISP-ML(Q). Ver [`docs/marco_metodologico.md`](docs/marco_metodologico.md), que incluye la documentación explícita del supuesto de desagregación proporcional utilizado y el cambio de taxonomía de Supersalud identificado en julio de 2023.

## Stack técnico

Python · Pandas · openpyxl · Streamlit · Plotly · Google Colab (exploración inicial) · GitHub

## Equipo

Equipo 330 — Personería Distrital de Medellín

## Licencia

MIT

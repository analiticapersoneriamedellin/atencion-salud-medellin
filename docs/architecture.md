# Arquitectura de la Solución

## Diagrama de capas

```
┌─────────────────────────────────────────────────────────────┐
│  FUENTE DE DATOS                                              │
│  Superintendencia Nacional de Salud (Supersalud)              │
│  Reportes PQRD "año corrido" (.xlsx), 2021-2026                │
└───────────────────────────┬────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  CAPA DE EXTRACCIÓN Y CONSOLIDACIÓN                            │
│  src/parse_pqrd.py                                             │
│  - Búsqueda de tablas por texto (no por posición fija de fila) │
│  - Extracción: Medellín, Antioquia, Dirección Seccional Salud, │
│    motivos específicos (2 taxonomías: legacy y nueva)          │
│  - Normalización de meses sin datos (None, no cero falso)      │
│  → data/processed/pqrd_consolidado.csv                         │
└───────────────────────────┬────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  CAPA DE INGENIERÍA DE VARIABLES Y ANÁLISIS                    │
│  notebooks/01_analisis_exploratorio.ipynb                      │
│  - Desagregación proporcional de motivos a nivel Medellín      │
│    (supuesto documentado en docs/marco_metodologico.md)        │
│  - Variables derivadas: variación %, promedio móvil, z-score   │
│  → data/processed/medellin_dataset_modelo.csv                  │
└───────────────────────────┬────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  CAPA DE MODELADO (IA)                                          │
│  Detección de anomalías basada en z-score respecto al           │
│  histórico de cada motivo específico                            │
│  Clasificación de riesgo: bajo / medio / alto                   │
└───────────────────────────┬────────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  CAPA DE PRESENTACIÓN                                            │
│  dashboard/app.py (Streamlit + Plotly)                          │
│  - KPIs principales                                              │
│  - Tendencia general (línea + promedio móvil)                   │
│  - Mapa de calor de riesgo por motivo y mes                      │
│  - Alertas activas filtrables, con exportación CSV               │
└─────────────────────────────────────────────────────────────┘
```

## Principio de diseño

Cada capa es independiente: se puede reemplazar la fuente de datos, el método de modelado, o la herramienta de visualización, sin reescribir las demás capas. Por ejemplo, si en el futuro se obtiene acceso a datos de Medellín desagregados directamente por motivo (eliminando el supuesto de proporcionalidad), solo cambiaría la capa de ingeniería de variables, no el resto del pipeline.

## Componente de Inteligencia Artificial

| Componente | Ubicación | Descripción |
|---|---|---|
| Detección de anomalías (z-score) | Notebook de análisis / `medellin_dataset_modelo.csv` | Identifica meses donde el volumen de un motivo específico se aleja significativamente de su comportamiento histórico |
| Clasificación de riesgo | Mismo dataset, columna `nivel_riesgo` | Traduce el z-score en una categoría interpretable (bajo/medio/alto) para facilitar la lectura no técnica |

## Decisiones de arquitectura explícitamente descartadas

- **Microservicios / API dedicada:** el volumen y la frecuencia de actualización de los datos (reportes mensuales de Supersalud) no justifican una arquitectura de servicios en producción continua.
- **Bases de datos relacionales/NoSQL dedicadas:** el volumen de datos (cientos de filas consolidadas) se maneja adecuadamente con archivos CSV; una base de datos añadiría complejidad operativa sin beneficio real para el alcance de este proyecto.
- **Procesamiento distribuido (Spark/Flink):** no aplica al volumen de datos de este proyecto.
# Arquitectura de la Solución

## Diagrama de capas

```
┌─────────────────────────────────────────────────────────────┐
│  FUENTES DE DATOS                                              │
│  SIVIGILA/MEData (dengue) │ IDEAM (clima) │ DANE (población)   │
└───────────┬─────────────────────┬──────────────────┬────────────┘
            ▼                     ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│  CAPA DE INGESTA                                                │
│  src/ingest_clima.py -- descarga histórica IDEAM (por año,     │
│  con reintentos, evitando el problema de offsets altos)        │
└───────────┬───────────────────────────────────────────────────┘
            ▼
┌─────────────────────────────────────────────────────────────┐
│  CAPA DE CONSOLIDACIÓN Y ANÁLISIS                               │
│  src/consolidar_dengue_clima.py -- cruce dengue+clima,          │
│    variables de rezago (lags), usado en el intento de modelo    │
│  src/analisis_incidencia_iceberg.py -- los 3 pilares centrales: │
│    1. Tasa de incidencia real (dengue + población)               │
│    2. Efecto "punta del iceberg" (proporción de hospitalizados) │
│    3. (Literatura científica externa, no automatizada)          │
└───────────┬───────────────────────────────────────────────────┘
            ▼
┌─────────────────────────────────────────────────────────────┐
│  CAPA DE MODELADO (IA)                                          │
│  src/train_modelo_dengue.py -- Random Forest (intento           │
│    documentado, resultado no satisfactorio, ver                 │
│    docs/marco_metodologico.md sección 3)                        │
│  Detección de anomalías / análisis descriptivo (componente      │
│    de IA final usado, más robusto con el volumen de datos       │
│    disponible)                                                  │
└───────────┬───────────────────────────────────────────────────┘
            ▼
┌─────────────────────────────────────────────────────────────┐
│  CAPA DE PRESENTACIÓN                                            │
│  dashboard/app.py (Streamlit + Plotly)                          │
│  - Tendencia e incidencia                                       │
│  - Efecto iceberg (barras + línea combinada)                    │
│  - Comparación por comuna                                       │
│  - Hallazgos y recomendaciones para la Personería                │
└─────────────────────────────────────────────────────────────┘
```

## Principio de diseño

Cada capa es independiente y reemplazable. El componente de modelado
predictivo (Random Forest) se mantiene en el repositorio como evidencia
transparente de un intento metodológico riguroso, aunque no forma parte
del flujo final de producción del dashboard — esta decisión de diseño
prioriza la honestidad metodológica sobre presentar únicamente los
resultados favorables.

## Componente de Inteligencia Artificial

| Componente | Ubicación | Estado |
|---|---|---|
| Random Forest Regressor (predicción de conteo semanal) | `src/train_modelo_dengue.py` | Implementado y evaluado; resultado documentado como no satisfactorio (R² ≈ 0, comparable a línea base ingenua) |
| Detección de patrones / análisis descriptivo riguroso | `src/analisis_incidencia_iceberg.py` | Componente de IA/analítica final usado en el dashboard — más robusto ante el volumen de datos real disponible |

## Decisiones de arquitectura explícitamente descartadas

- **Modelo predictivo como componente central:** se intentó, se
  documentó honestamente su bajo desempeño, y se decidió no forzarlo como
  la pieza central del proyecto (ver `docs/marco_metodologico.md`).
- **Procesamiento distribuido (Spark/Flink), microservicios, bases de
  datos dedicadas:** no se justifican para el volumen de datos de este
  proyecto (decenas de miles de filas, no millones).
- **Ingesta en tiempo real:** las tres fuentes usadas (SIVIGILA, IDEAM
  histórico, DANE) se publican por lotes periódicos, no en streaming.
# Diccionario de Datos

## 1. Fuente: casos de dengue (`data/raw/sivigila_dengue.csv`)

Dataset original de SIVIGILA vía MEData (Alcaldía de Medellín), 53.813
filas, 38 columnas. Columnas usadas activamente en el análisis:

| Columna | Tipo | Descripción | Uso en el proyecto |
|---|---|---|---|
| `id` | Numérico | Identificador único del caso | Conteo de casos |
| `semana` | Numérico | Semana epidemiológica | Agregación temporal |
| `year_` (renombrada a `anio`) | Numérico | Año del caso | Filtro de ventana 2017-2021, tendencia |
| `comuna` | Texto | Comuna/corregimiento de residencia | Desagregación territorial, tasa de incidencia |
| `nombre_barrio` | Texto | Barrio | No usado en esta versión (posible trabajo futuro) |
| `fec_con_` | Fecha | Fecha de consulta | No usado activamente en esta versión |
| `ini_sin_` | Fecha | Fecha de inicio de síntomas | No usado activamente en esta versión |
| `clas_dengue` | Categórica (código) | Clasificación de gravedad (1=sin signos alarma, 2=con signos alarma, 3=grave) | Indicador secundario de iceberg — **con limitación de calidad de dato documentada** (discontinuidad de codificación entre años) |
| `pac_hos_` | Categórica (código, viene como texto) | Hospitalización (1=sí, 2=no) | Indicador principal de "efecto iceberg" |

## 2. Fuente: clima histórico IDEAM

### Temperatura (`data/raw/ideam_temperatura_medellin_semanal.csv`)
Agregado semanal (promedio) desde el crudo horario de las estaciones
Aeropuerto Olaya Herrera y Pajarito. Histórico real: 2005-2026.

### Precipitación (`data/raw/ideam_precipitacion_medellin_semanal.csv`)
Agregado semanal (suma) desde el crudo horario. Histórico real y
consistente: **2017-2024** (antes de 2016-2017 el sensor no reportaba de
forma confiable en las estaciones de Medellín — limitación confirmada
empíricamente, no supuesta).

| Columna | Tipo | Descripción |
|---|---|---|
| `anio` | Numérico | Año |
| `semana` | Numérico | Semana epidemiológica (ISO) |
| `nombreestacion` | Texto | Estación IDEAM de origen |
| `temperatura_promedio` | Numérico (°C) | Promedio semanal de temperatura |
| `precipitacion_acumulada` | Numérico (mm) | Suma semanal de precipitación |

## 3. Fuente: población por comuna (`data/raw/poblacion_comunas_medellin.csv`)

Proyecciones DANE/Alcaldía de Medellín 2018-2030, formato ancho (una
columna por año: `total_2018` ... `total_2030`), transformado a formato
largo en `src/analisis_incidencia_iceberg.py`.

| Columna original | Descripción |
|---|---|
| `nombre` | Nombre de la comuna/corregimiento (con tildes) |
| `total_YYYY` | Población proyectada para ese año |

**Nota de mapeo de nombres:** existen diferencias de tildes y estructura
de nombre entre este dataset y el de dengue (ej. "Belen" vs. "Belén",
"Corregimiento De San Cristobal" vs. "San Cristóbal"). Se resolvieron con
un diccionario de equivalencias explícito (`EQUIVALENCIAS_COMUNA` en
`src/analisis_incidencia_iceberg.py`), documentado y verificado
manualmente.

## 4. Datasets consolidados / de salida (`data/processed/`)

### `dengue_clima_consolidado.csv`
Casos de dengue agregados por semana-comuna, cruzados con clima y
variables de rezago (lags 2 y 4 semanas). Usado en el intento de modelo
predictivo (resultado documentado en `docs/marco_metodologico.md`).

### `dengue_ciudad_consolidado.csv`
Igual al anterior, pero agregado a nivel de ciudad completa (sin
desagregar por comuna) — usado en la segunda iteración del intento de
modelo predictivo.

### `dengue_tasa_incidencia.csv`
| Columna | Descripción |
|---|---|
| `comuna` | Comuna/corregimiento |
| `anio` | Año |
| `casos` | Casos notificados |
| `poblacion` | Población proyectada (2018 usada como aproximación para 2017) |
| `tasa_incidencia_100k` | Casos por 100.000 habitantes |

### `dengue_efecto_iceberg.csv`
| Columna | Descripción |
|---|---|
| `anio` | Año |
| `total_casos` | Total de casos notificados |
| `casos_hospitalizados` | Casos con `pac_hos_ == 1` |
| `casos_graves` | Casos con `clas_dengue == 3` (ver limitación de calidad de dato) |
| `proporcion_hospitalizados` | Indicador principal de subregistro |
| `proporcion_graves` | Indicador secundario (poco confiable, ver sección 1) |

## 5. Variable objetivo original (modelo predictivo, no usado en la versión final)

`casos_dengue_semana_siguiente`: casos de la semana siguiente, por
comuna. Se mantiene documentada por transparencia metodológica, aunque el
modelo entrenado con esta variable no alcanzó poder predictivo aceptable
(ver `docs/marco_metodologico.md`, sección 3).
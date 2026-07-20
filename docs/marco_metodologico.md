# Marco Metodológico

## Metodología general

Se adopta CRISP-ML(Q) como marco de trabajo: comprensión del problema,
adquisición y preparación de datos, ingeniería de variables, modelado,
evaluación y despliegue, con controles de calidad en cada fase.

## 1. Fuentes de datos

### 1.1 Casos de dengue (fuente principal)
**SIVIGILA, vía MEData** (Alcaldía de Medellín) — dataset ID `1-026-22-000135`.
53.813 casos individuales, 2008-2021, con 38 variables (demografía,
síntomas clínicos, clasificación de gravedad, hospitalización, barrio,
comuna). Ver `docs/fuentes_datos.md` para el detalle completo.

### 1.2 Clima histórico
**IDEAM**, vía datos.gov.co — temperatura (`sbwg-7ju4`) y precipitación
(`s54a-sgyg`), estaciones de Medellín (Aeropuerto Olaya Herrera, Pajarito).
Temperatura: histórico desde 2005. Precipitación: histórico real y
consistente **solo desde 2016-2017** (confirmado empíricamente — antes de
esa fecha el sensor de precipitación no reportaba de forma consistente en
las estaciones de Medellín).

### 1.3 Población por comuna
**DANE / Alcaldía de Medellín**, vía MEData — Proyecciones de Población
por comuna y corregimiento 2018-2030 (Contrato interadministrativo
4600085225 de 2020, base Censo 2018). No cubre 2017; se usó la población
de 2018 como aproximación para ese año (supuesto documentado, ver sección 6).

## 2. Ventana de análisis: 2017-2021

Aunque el dengue cubre 2008-2021 y la temperatura tiene histórico desde
2005, la precipitación solo tiene cobertura confiable desde 2017. Se
definió esta ventana como el período de análisis principal para garantizar
que ambas variables climáticas estén disponibles simultáneamente.

## 3. Intento de modelo predictivo (Random Forest) — documentado como aprendizaje metodológico

Siguiendo el documento de estrategia inicial del equipo, se entrenó un
Random Forest Regressor para predecir el número de casos de dengue de la
semana siguiente, usando temperatura y precipitación rezagadas (lags de 2
y 4 semanas) como predictores.

**Resultado con validación temporal (entrenamiento 2017-2018, validación
2019), a nivel de agregación semana-comuna:** R² = -0,06 (peor que
predecir el promedio histórico). **A nivel de agregación semana-ciudad**
(sumando todas las comunas): R² = -0,01, con MAE de 7,06 casos frente a un
MAE de línea base ingenua similar.

**Diagnóstico:** con ~250 puntos semanales disponibles (5 años x 52
semanas) y una tendencia temporal muy fuerte (caída del 90% entre 2017 y
2021, ver sección 4), el modelo no logra generalizar de forma confiable:
la variable `año` explica por sí sola cerca de la mitad de la importancia
del modelo, evidenciando que el volumen de datos es insuficiente para que
la señal climática se distinga de la tendencia temporal dominante.

**Decisión metodológica:** en lugar de forzar un modelo de regresión con
bajo poder predictivo, el proyecto reorienta el componente de IA hacia
análisis descriptivo riguroso y detección de anomalías (sección 5), que
son más robustos ante volúmenes de datos limitados y no requieren
generalizar a datos futuros no vistos.

## 4. Hallazgo 1: tendencia y tasa de incidencia real

Se calculó la tasa de incidencia (casos / población x 100.000 habitantes)
por comuna y año, en lugar de usar solo conteos crudos, siguiendo la misma
metodología que usa oficialmente la Secretaría de Salud de Medellín en su
dataset "Dengue Geográfico".

**Resultado:** la tasa de incidencia promedio cayó de 80,7 (2017) a 8,2
(2021) casos por 100.000 habitantes — una reducción del 90%, consistente
en todas las comunas.

## 5. Hallazgo 2: efecto "punta del iceberg" (detección de anomalías / proxy de subregistro)

Se calculó la proporción de casos hospitalizados sobre el total de casos
notificados, por año, usando la variable `pac_hos_` del dataset SIVIGILA.

**Resultado:**

| Año | Casos totales | % Hospitalizados |
|---|---|---|
| 2017 | 2.154 | 15,3% |
| 2018 | 1.188 | 14,6% |
| 2019 | 1.236 | 21,4% |
| 2020 | 629 | 25,0% |
| 2021 | 240 | 43,8% |

La proporción de hospitalizados casi se triplicó mientras el volumen
total caía 90%. Esto es la firma característica de subregistro: los casos
graves, que requieren atención hospitalaria y no pueden pasar
desapercibidos, se siguen captando; los casos leves, que dependen de que
el paciente busque atención voluntariamente, dejan de notificarse en una
proporción creciente.

**Nota de calidad de dato:** se intentó un segundo indicador (proporción
de "dengue grave" según la variable `clas_dengue`), pero se encontró que
esta variable tiene una discontinuidad de codificación severa: los códigos
de gravedad no se usaron en 2017-2019, cambiaron radicalmente en 2020, y
el campo quedó sin diligenciar ("SD") en el 100% de los casos de 2021. Esta
discontinuidad se documenta como evidencia adicional (no como indicador
cuantitativo confiable) de disrupción del sistema de captura de datos
clínicos durante el período de pandemia.

## 6. Hallazgo 3: respaldo de literatura científica

Un estudio revisado por pares ("Integrated vector management program in
the framework of the COVID-19 pandemic in Medellín, Colombia", *PMC*)
documenta que el programa de vigilancia entomológica de la ciudad cambió
de metodología durante 2018-2021: la vigilancia domiciliaria se sustituyó
por vigilancia institucional debido a la pandemia. Esta es una
confirmación externa e independiente, documentada por pares académicos,
de que el sistema de captación de información sobre dengue en Medellín
sufrió una disrupción real durante exactamente el período analizado.

## 7. Síntesis de la pregunta de investigación

Los tres hallazgos, obtenidos de forma independiente (tasas de incidencia,
proporción de hospitalizados, y literatura externa), apuntan en la misma
dirección: la caída del 90% en dengue notificado es más consistente con
subregistro creciente que con una mejora epidemiológica real. No se
descarta que exista también una mejora real subyacente (ej. por control
vectorial efectivo) — la evidencia disponible no permite separar
completamente ambos efectos, pero sí permite afirmar que **el patrón
observado no puede interpretarse como una mejora real sin cuestionamiento**.

## 8. Limitaciones metodológicas reconocidas

- El modelo predictivo de conteo exacto (Random Forest) no alcanzó poder
  predictivo aceptable con el volumen de datos disponible — documentado
  como resultado honesto, no ocultado.
- La población de 2017 se aproximó con la de 2018 (dataset de población
  no cubre 2017).
- Seis comunas/corregimientos requirieron un mapeo manual de nombres entre
  el dataset de dengue y el de población, por diferencias de tildes y
  estructura de nombre (documentado en `src/analisis_incidencia_iceberg.py`).
- El clima es a nivel de ciudad (estaciones puntuales), no por comuna —
  todas las comunas de una misma semana comparten el mismo dato climático.
- La variable `clas_dengue` no es confiable como indicador cuantitativo
  por su discontinuidad de codificación entre años (ver sección 5).
- No se descarta la posibilidad de que la caída de casos combine
  subregistro real con una mejora epidemiológica genuina; este análisis no
  permite cuantificar la proporción de cada efecto por separado.
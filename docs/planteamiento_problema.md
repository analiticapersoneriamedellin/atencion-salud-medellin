# Planteamiento del Problema

## Contexto

La Personería Distrital de Medellín tiene una función constitucional de
vigilancia y defensa de los derechos ciudadanos, incluyendo el derecho
fundamental a la salud (Ley Estatutaria 1751 de 2015). El dengue es una
enfermedad endémica en Medellín, transmitida por el mosquito *Aedes
aegypti*, cuya dinámica de transmisión está fuertemente influenciada por
condiciones climáticas (temperatura, precipitación).

## El reto (registrado oficialmente ante el concurso)

**ID del Equipo:** 330. **ID del Reto:** 117. **Categoría:** Salud y Bienestar.

**Enunciado oficial:** "Desarrollar modelos de IA para predecir brotes de
enfermedades transmisibles usando datos de salud pública, vacunación y
condiciones ambientales."

## Problema identificado

Los casos de dengue notificados en Medellín cayeron un 90% entre 2017 y
2021 (de 2.154 a 240 casos anuales; tasa de incidencia de 80,7 a 8,2 por
100.000 habitantes). Esta caída plantea una pregunta que no puede
responderse solo con el dato agregado: **¿es una mejora epidemiológica
real, o un síntoma de subregistro creciente en el sistema de vigilancia?**

Esta pregunta es relevante para la Personería porque, si se trata de
subregistro, implica que el sistema de información en salud de la ciudad
está perdiendo capacidad de detección temprana de brotes — lo cual
compromete tanto la respuesta oportuna del Estado como el derecho de los
ciudadanos a un sistema de salud que los proteja de manera efectiva.

## Pregunta de investigación

¿La caída en los casos de dengue notificados en Medellín (2017-2021)
refleja una mejora epidemiológica real, o es consecuencia de un patrón de
subregistro — visible en la composición de los propios casos notificados
y respaldado por evidencia de cambios documentados en la metodología de
vigilancia de la ciudad durante el mismo período?

## Alcance

- **Fuente principal:** casos de dengue notificados en Medellín,
  2008-2021 (SIVIGILA, vía MEData), con foco analítico en 2017-2021
  (ventana con clima histórico completo disponible).
- **Fuentes complementarias:** clima histórico de Medellín (IDEAM,
  temperatura y precipitación); proyecciones de población por comuna
  (DANE/Alcaldía de Medellín, 2018-2030).
- **Nivel geográfico:** Medellín, con desagregación por comuna/corregimiento.
- **Componentes de análisis:**
  1. Tendencia y tasa de incidencia real (casos/población) por comuna y año.
  2. Indicador de "efecto punta del iceberg": proporción de casos
     hospitalizados sobre el total notificado, como proxy de subregistro.
  3. Contraste con literatura científica sobre cambios en la vigilancia
     entomológica de Medellín durante la pandemia.
  4. Análisis de correlación (no predicción forzada) entre variables
     climáticas y casos de dengue.
  5. Detección de anomalías sobre la serie de casos/tasas.

## Justificación de la fuente y del enfoque

Se evaluó inicialmente un enfoque de predicción de conteo exacto de casos
(Random Forest Regressor) por semana y comuna, siguiendo el documento de
estrategia inicial del equipo. Sin embargo, la validación temporal reveló
que el volumen de datos disponible (5 años de datos semanales) es
insuficiente para que un modelo de regresión generalice de forma
confiable — resultado documentado y comparado contra una línea base
ingenua en `docs/marco_metodologico.md`. En consecuencia, el proyecto
reorienta el componente de IA hacia análisis descriptivo riguroso,
detección de anomalías y una pregunta de investigación con implicaciones
directas para la labor de vigilancia de la Personería, en lugar de forzar
una predicción de precisión que los datos no pueden sostener.
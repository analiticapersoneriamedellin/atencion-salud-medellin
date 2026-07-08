# Marco Metodológico

## Metodología general

Se adopta CRISP-ML(Q) (Cross-Industry Standard Process for Machine Learning
with Quality assurance) como marco de trabajo, cubriendo comprensión del
problema, adquisición y preparación de datos, ingeniería de variables,
modelado, evaluación y despliegue.

## 1. Comprensión del problema

Ver `planteamiento_problema.md`. Objetivo: analizar la atención oportuna en
salud en Medellín (tiempos de atención, asignación de citas, autorizaciones,
PQRS, acceso a especialistas, servicios de urgencias), para apoyar la labor
de vigilancia de derechos de la Personería Distrital de Medellín — según el
plan de desarrollo registrado oficialmente ante los organizadores del
concurso (Reto ID 117, Equipo ID 330).

## 2. Fuente de datos

**Superintendencia Nacional de Salud (Supersalud)** — reportes periódicos
"año corrido" de Peticiones, Quejas, Reclamos y Denuncias (PQRD) en salud,
descargados en formato Excel desde el portal oficial de Supersalud. Ver
`fuentes_datos.md` para el detalle de cada archivo usado.

Cada archivo trae 11 tablas: total nacional, por tipo de riesgo, por canal
de radicación, por departamento, por capital de departamento (incluye
Medellín), por macromotivo, por motivo específico, por EPS (contributivo,
subsidiado, indígena) y por otro tipo de vigilado (incluye Dirección
Seccional de Salud de Antioquia).

## 3. HALLAZGO METODOLÓGICO CONFIRMADO: cambio de taxonomía a mitad de 2023

Al inspeccionar los archivos crudos y validar la extracción con los datos
reales (no solo con la descripción teórica de Supersalud), se confirmó que
la taxonomía de "motivos específicos" de reclamo **cambió de forma gradual
a mediados de 2023**, no de un año completo a otro:

- **Enero 2021 – Junio 2023:** taxonomía LEGACY. 10 motivos orientados a
  especialidades médicas y trámites clínicos (ej. "falta de oportunidad en
  cita con especialista", "demora en programación de exámenes de
  laboratorio", "falta de oportunidad en programación de cirugía").
  También usa la clasificación "TIPO DE PQRD" (categorías
  REGULARES/SIS), no "tipo de riesgo".
- **Julio 2023 en adelante:** taxonomía NUEVA. 9-10 motivos orientados a
  barreras de acceso y autorizaciones (ej. "negación en la asignación de
  citas", "falta de oportunidad en autorización de tecnologías",
  "negación para la entrega de tecnologías en salud"). Usa la
  clasificación "TIPO DE RIESGO" (SIMPLE / PRIORIZADO / RIESGO VITAL).
  La categoría "falta de oportunidad en el proceo de referencia y
  contrarreferencia" se incorporó un poco más tarde, ya en 2024.

**Implicación para el modelado:** el archivo de 2023 contiene AMBAS
taxonomías (legacy en enero-junio, nueva en julio-octubre) — esto es un
reflejo real de los datos, no un error de extracción. Se decidió tratar
cada taxonomía como una serie separada (`motivo_especifico_legacy_2021_2023`
y `motivo_especifico_2024_2026` en el dataset consolidado), sin intentar
reconciliarlas en una sola categoría, para no introducir distorsión
artificial. El período de mayor consistencia y riqueza para el componente
de IA es **julio 2023 en adelante** (taxonomía nueva).

## 4. Preparación de datos

- Extracción automatizada por búsqueda de texto (no por posición fija de
  fila/columna), dado que las tablas se desplazan de fila entre archivos
  de distintos años. Ver `src/parse_pqrd.py`.
- Los meses sin datos (archivos "año corrido" de meses intermedios) se
  tratan como valores nulos explícitos, nunca como cero.
- Normalización de texto (mayúsculas, sin tildes) para hacer robusta la
  búsqueda ante variaciones de formato entre archivos.

## 5. Variables consideradas

Ver `data_dictionary.md` (pendiente de completar con el detalle final una
vez definida la variable objetivo del modelo).

## 6. Limitaciones metodológicas reconocidas

- La fuente es un reporte agregado/tabular publicado por Supersalud, no
  microdatos de caso individual — el análisis es a nivel de volumen
  agregado mensual por categoría, no de trazabilidad de casos puntuales.
- El cambio de taxonomía a mitad de 2023 limita la comparabilidad directa
  de "motivos específicos" antes y después de julio 2023.
- El foco geográfico del componente de IA se concentra en Medellín/Antioquia
  (alineado al plan registrado), aunque la fuente permite en principio
  extender el análisis a otros departamentos/capitales si el tiempo lo
  permite.

## 7. Limitación de granularidad geográfica y supuesto adoptado

**Limitación confirmada:** el reporte de Supersalud NO cruza motivo
específico × ciudad. La tabla "por capital de departamento" da el volumen
total de reclamos de Medellín (sin desglose por motivo), y la tabla "por
motivo específico" da el desglose por motivo a nivel NACIONAL (sin
desglose por ciudad). No existe en esta fuente un dato directo de
"cuántos reclamos por motivo X hubo en Medellín".

**Supuesto adoptado (DECISIÓN METODOLÓGICA EXPLÍCITA, declarada ante el
jurado):** se asume que la composición porcentual de motivos específicos
a nivel nacional es representativa de la composición de motivos en
Medellín. Bajo este supuesto, se estima el volumen mensual de reclamos por
motivo específico en Medellín como:

```
reclamos_estimados(motivo, mes, Medellín) =
    reclamos_totales(mes, Medellín) × proporción_nacional(motivo, mes)
```

donde `proporción_nacional(motivo, mes)` = reclamos nacionales de ese
motivo en ese mes / total nacional de reclamos en ese mes.

**Justificación del supuesto:** Medellín es la segunda ciudad más poblada
de Colombia y su sistema de salud opera bajo el mismo marco regulatorio
y las mismas EPS que operan a nivel nacional, por lo que no hay razón
estructural fuerte para esperar que la composición de motivos difiera
drásticamente de la nacional. Sin embargo, esto es un supuesto de
proporcionalidad, no un dato observado directamente, y se declara así
para transparencia metodológica.

**Riesgo del supuesto:** si Medellín tiene particularidades locales (ej.
una EPS con problemas específicos de operación en la ciudad, o un tipo de
servicio con mayor demanda relativa), esta desagregación proporcional no
las capturaría. Se recomienda como trabajo futuro validar este supuesto
si se logra acceso a datos desagregados directamente por ciudad y motivo.
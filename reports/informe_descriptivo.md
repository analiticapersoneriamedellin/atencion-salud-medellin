# Informe Descriptivo: Vigilancia de Atención Oportuna en Salud en Medellín

**Concurso Datos al Ecosistema 2026: IA para Colombia — Ministerio TIC**
**Reto:** Salud y Bienestar (ID 117) — Equipo 330
**Elaborado para:** Personería Distrital de Medellín
**Fuente de datos:** Superintendencia Nacional de Salud (Supersalud), reportes PQRD 2021-2026
**Fecha del análisis:** Julio de 2026

---

## 1. Resumen ejecutivo

Este análisis integra los reportes oficiales de Peticiones, Quejas, Reclamos y Denuncias (PQRD) en salud publicados por la Superintendencia Nacional de Salud entre 2021 y 2026, con el objetivo de identificar patrones de demora, barreras de acceso y riesgos de vulneración del derecho a la salud en Medellín, como insumo para la labor de vigilancia de la Personería Distrital.

Se identificaron **tres hallazgos principales**:

1. Los reclamos en salud en Medellín se **casi triplicaron** entre 2021 y 2025-2026.
2. **Septiembre de 2025** presentó una falla sistémica: siete de los diez motivos de reclamo alcanzaron niveles de riesgo alto simultáneamente.
3. **"Falta de oportunidad en el proceso de referencia y contrarreferencia"** es un problema emergente con tendencia de crecimiento sostenido en 2026, a diferencia de otros motivos que se normalizaron después del pico de 2025.

---

## 2. Hallazgo 1: Tendencia sostenida de crecimiento en los reclamos

El volumen mensual de reclamos en salud en Medellín pasó de un rango de 6.000-8.000 reclamos mensuales en 2021 a picos de 18.000-19.000 reclamos mensuales en 2025, lo que representa un incremento aproximado del **164% entre el primer y el último mes analizado**.

Esta tendencia es sostenida a lo largo de cinco años, no un evento aislado, lo que sugiere un deterioro progresivo y estructural en el acceso a servicios de salud en la ciudad, más que fluctuaciones puntuales.

**Implicación para la Personería:** el crecimiento del volumen de reclamos, por sí solo, ya constituye evidencia cuantitativa de un problema creciente que amerita seguimiento sistemático, independientemente de los motivos específicos.

---

## 3. Hallazgo 2: Pico sistémico en septiembre de 2025

Al desagregar los reclamos por motivo específico, se identificó que en **septiembre de 2025** siete de los diez motivos de reclamo monitoreados alcanzaron simultáneamente su nivel de riesgo más alto del período analizado:

- Negación en la asignación de citas o consultas
- Falta de oportunidad en las citas o consultas
- Falta de oportunidad en la autorización de citas de consulta
- Falta de oportunidad en la autorización de otros servicios de salud
- Falta de oportunidad en la autorización de tecnologías en salud
- Negación en la atención en otros servicios de salud
- Falta de oportunidad en la atención en otros servicios de salud

Que múltiples motivos —que en principio corresponden a distintos puntos del proceso de atención (asignación de citas, autorizaciones, prestación de servicios)— se deterioren al mismo tiempo sugiere una **falla generalizada del sistema en ese período**, no un problema aislado de un solo trámite o servicio.

**Implicación para la Personería:** este tipo de pico simultáneo en múltiples frentes es la señal de alerta más fuerte identificada en el análisis, y sería el punto de partida recomendado para una indagación específica (por ejemplo, verificar si coincidió con una contingencia operativa de alguna EPS con alta participación en Medellín, cambios normativos, u otro evento puntual del sistema de salud en esas fechas).

---

## 4. Hallazgo 3: Riesgo emergente en referencia y contrarreferencia

El motivo "falta de oportunidad en el proceso de referencia y contrarreferencia" (traslado de pacientes entre niveles de atención, por ejemplo de un centro de atención primaria hacia un especialista o un hospital de mayor complejidad) muestra un comportamiento distinto al resto: **mientras los demás motivos se normalizaron después del pico de septiembre-octubre 2025, este continuó en niveles de riesgo alto en enero, marzo y abril de 2026**.

**Implicación para la Personería:** a diferencia del hallazgo anterior (un pico puntual ya ocurrido), este es un problema activo y en curso al momento de este análisis. Representa la alerta con mayor relevancia para una acción de vigilancia inmediata, dado que la tendencia no muestra señales de autocorrección.

---

## 5. Nota metodológica (transparencia sobre el alcance del análisis)

Los reportes de Supersalud publican el volumen total de reclamos por ciudad (incluyendo Medellín) y, por separado, el desglose por motivo específico a nivel nacional, pero no cruzan ambas dimensiones en un solo dato. Para este análisis, el volumen de reclamos por motivo específico en Medellín se **estimó aplicando la proporción nacional de cada motivo al volumen total de reclamos de Medellín** en cada mes.

Este es un supuesto de proporcionalidad, no un dato observado directamente. Se considera razonable dado que Medellín opera bajo el mismo marco regulatorio y las mismas EPS que actúan a nivel nacional, pero no captura eventuales particularidades locales. El detalle completo de esta decisión metodológica, junto con el cambio de taxonomía de motivos que Supersalud introdujo a mediados de 2023, se documenta en `docs/marco_metodologico.md` del repositorio técnico del proyecto.

---

## 6. Recomendaciones para la labor de vigilancia

1. **Priorizar el seguimiento del motivo "referencia y contrarreferencia"** en los próximos meses, dado que es el único con tendencia de deterioro activo y sin señales de mejora al cierre de este análisis.
2. **Solicitar información puntual sobre septiembre de 2025** a las entidades de salud con mayor participación en Medellín, para esclarecer las causas del pico sistémico identificado.
3. **Establecer un monitoreo periódico** (mensual o trimestral) de los reportes PQRD de Supersalud, replicando la metodología de este análisis, para detectar tempranamente picos similares en el futuro.
4. **Explorar el acceso a datos desagregados directamente por ciudad y motivo** (si Supersalud o el Ministerio de Salud los ponen a disposición), para eliminar el supuesto de proporcionalidad nacional y ganar precisión territorial.

---

## 7. Producto técnico asociado

Este informe se acompaña de un dashboard interactivo (desarrollado en Streamlit) que permite explorar la evolución temporal, el mapa de riesgo por motivo y mes, y las alertas activas de forma dinámica. El código fuente, los datos procesados y la documentación técnica completa están disponibles en el repositorio público del proyecto en GitHub.

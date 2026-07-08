# Planteamiento del Problema

## Contexto

La Personería Distrital de Medellín tiene una función constitucional de
vigilancia y defensa de los derechos ciudadanos, incluyendo el derecho
fundamental a la salud. Identificar de forma oportuna dónde se concentran
las demoras y barreras de acceso a servicios de salud permite dirigir mejor
la labor de vigilancia institucional.

## El reto (registrado oficialmente ante el concurso)

**ID del Equipo:** 330. **ID del Reto:** 117. **Categoría:** Salud y Bienestar.

Plan de desarrollo registrado:

> "Analizar la atención oportuna en salud en Medellín mediante el uso de
> Inteligencia Artificial y análisis de datos, con el objetivo de
> identificar patrones de demora, barreras de acceso y posibles riesgos en
> la prestación de servicios de salud para apoyar la labor de la
> Personería Distrital de Medellín."

## Problema identificado

1. Existen demoras documentadas en distintos puntos del proceso de atención
   en salud: asignación de citas, autorizaciones de servicios/tecnologías,
   atención en urgencias, y procesos de referencia entre niveles de atención.
2. Estas demoras representan un riesgo de vulneración del derecho
   fundamental a la salud (Ley 1751 de 2015, Ley Estatutaria de Salud).
3. La Superintendencia Nacional de Salud (Supersalud) recibe y clasifica
   estos reclamos ciudadanos (PQRD), publicando reportes agregados
   periódicos, pero no existe un análisis sistemático propio de la
   Personería que traduzca esta información en focos de vigilancia
   territorial concretos para Medellín.

## Pregunta de investigación

¿Es posible identificar, a partir de los reclamos ciudadanos en salud (PQRD)
reportados ante Supersalud, patrones de demora y barreras de acceso a
servicios de salud en Medellín — por tipo de motivo y evolución temporal —
que sirvan de base para priorizar la labor de vigilancia de la Personería
Distrital de Medellín?

## Alcance

- **Fuente principal:** reportes PQRD de Supersalud, 2021-2026 (con foco
  analítico en julio 2023 en adelante, período de taxonomía consistente).
- **Nivel geográfico:** Medellín (capital) y Antioquia (departamento) como
  contexto comparativo.
- **Unidad de análisis:** volumen mensual de reclamos por motivo específico
  y por tipo de riesgo (simple/priorizado/riesgo vital).
- **Componente de IA:** análisis de tendencias y detección de anomalías
  sobre el volumen de reclamos por motivo/mes; clasificación de riesgo o
  priorización según el patrón histórico observado.
- **Fuera de alcance de esta versión:** microdatos de caso individual
  (Supersalud publica agregados, no registros por paciente); integración
  con sistemas internos de la Personería (no confirmados como disponibles
  al momento de iniciar el proyecto).

## Justificación de la fuente de datos elegida

Se evaluó la posibilidad de usar registros internos de la Personería, pero
no se confirmó su disponibilidad a tiempo para el desarrollo del proyecto.
Se optó por los reportes oficiales de Supersalud porque:

- Es la entidad nacional competente que recibe y clasifica formalmente los
  reclamos en salud de los ciudadanos.
- Publica series periódicas desde 2014, con desagregación específica para
  Medellín como capital de departamento.
- Clasifica los reclamos por motivo específico, lo cual traduce
  directamente los conceptos del plan registrado (tiempos de atención,
  asignación de citas, autorizaciones, acceso a especialistas, urgencias)
  en categorías de datos ya existentes y oficiales.
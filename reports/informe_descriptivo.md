# Informe Descriptivo: Vigilancia Epidemiológica de Dengue en Medellín

**Concurso Datos al Ecosistema 2026: IA para Colombia — Ministerio TIC**
**Reto:** Salud y Bienestar (ID 117) — Equipo 330
**Elaborado para:** Personería Distrital de Medellín
**Fuentes:** SIVIGILA/MEData (casos de dengue), IDEAM (clima), DANE/Alcaldía de Medellín (población)
**Fecha del análisis:** Julio de 2026

---

## 1. Resumen ejecutivo

Este análisis examina la evolución de los casos de dengue notificados en
Medellín entre 2017 y 2021, encontrando una caída del 90% en la tasa de
incidencia (de 80,7 a 8,2 casos por 100.000 habitantes). En lugar de
interpretar esta caída como una mejora automática, el proyecto investiga
si refleja **subregistro creciente** — es decir, una pérdida de capacidad
del sistema de salud para detectar y notificar casos, más que una
reducción real de la transmisión de la enfermedad.

Se encontraron **tres líneas de evidencia independientes** que apuntan en
la misma dirección:

1. La proporción de casos hospitalizados sobre el total **casi se
   triplicó** (15,3% a 43,8%) mientras el volumen total caía.
2. La calidad del registro de clasificación clínica de gravedad se
   deterioró severamente durante 2020-2021.
3. Un estudio científico independiente confirma que el programa de
   vigilancia entomológica de la ciudad cambió de metodología durante la
   pandemia (2018-2021).

---

## 2. Hallazgo 1: la caída de casos, medida correctamente

Usando la tasa de incidencia (casos por 100.000 habitantes, no solo
conteos crudos) y las proyecciones oficiales de población por comuna, se
confirma que la caída no es un artefacto del crecimiento poblacional: la
tasa de incidencia promedio en Medellín pasó de **80,7 casos por 100.000
habitantes en 2017 a 8,2 en 2021**.

**Implicación para la Personería:** una caída de esta magnitud amerita
verificación — no es prudente asumir automáticamente que refleja éxito en
el control del dengue sin contrastarla con otros indicadores.

---

## 3. Hallazgo 2: el efecto "punta del iceberg"

| Año | Casos notificados | % Hospitalizados |
|---|---|---|
| 2017 | 2.154 | 15,3% |
| 2018 | 1.188 | 14,6% |
| 2019 | 1.236 | 21,4% |
| 2020 | 629 | 25,0% |
| 2021 | 240 | **43,8%** |

Cuando el volumen total de casos notificados cae, pero la proporción de
casos que terminan hospitalizados sube de forma sostenida, es una señal
característica de que **solo los casos más graves —los que no se pueden
ocultar porque requieren atención hospitalaria— siguen siendo captados
por el sistema**. Los casos leves, que dependen de que la persona busque
atención médica voluntariamente, parecen estar quedando cada vez más por
fuera del registro oficial.

**Implicación para la Personería:** este patrón es consistente con
barreras de acceso a la atención en salud, un asunto directamente
relacionado con el derecho fundamental a la salud.

---

## 4. Hallazgo 3: respaldo de literatura científica independiente

Un estudio publicado en una revista científica revisada por pares
(disponible en PMC) documenta que, durante la pandemia de COVID-19, el
programa de vigilancia y control de vectores de Medellín tuvo que
modificar su metodología: la vigilancia entomológica domiciliaria fue
sustituida por vigilancia desde el entorno institucional, como medida de
bioseguridad. Este cambio documentado coincide exactamente con el período
en que se observa la mayor caída de casos notificados.

**Implicación para la Personería:** existe evidencia externa e
independiente, no generada por este proyecto, de que la capacidad de
vigilancia de enfermedades transmitidas por vector en la ciudad se vio
comprometida durante el período analizado.

---

## 5. Nota metodológica sobre el componente predictivo

Se evaluó la posibilidad de construir un modelo de inteligencia artificial
que predijera el número exacto de casos de dengue esperados cada semana,
usando variables climáticas. La validación rigurosa (entrenando con años
pasados y evaluando contra un año no visto por el modelo) mostró que el
volumen de datos disponible no es suficiente para que dicho modelo
generalice de forma confiable — resultado documentado con transparencia en
`docs/marco_metodologico.md`, incluyendo la comparación contra una línea
base simple. En lugar de presentar una predicción poco confiable, el
proyecto prioriza el análisis descriptivo riguroso y la detección de
patrones anómalos, que sí son robustos con los datos disponibles.

---

## 6. Recomendaciones para la labor de vigilancia de la Personería

1. **Solicitar a la Secretaría de Salud de Medellín una explicación formal
   sobre la evolución del programa de vigilancia entomológica** desde la
   pandemia hasta la actualidad — en particular, si la vigilancia
   domiciliaria ya se restableció, y con qué cobertura territorial.

2. **Priorizar el seguimiento de comunas con tasas de incidencia
   históricamente altas**, verificando si la asignación de recursos de
   control vectorial (fumigación, entrega de toldillos) es proporcional al
   riesgo epidemiológico real de cada territorio.

3. **Indagar sobre el acceso oportuno a diagnóstico temprano de dengue**,
   dado que el aumento en la proporción de casos hospitalizados sugiere que
   los pacientes podrían estar llegando al sistema de salud en etapas más
   avanzadas de la enfermedad.

4. **Promover el monitoreo periódico de este tipo de indicador** (tasa de
   incidencia vs. proporción de casos graves) como herramienta de alerta
   temprana ante posibles fallas de captación del sistema de vigilancia,
   replicable a otras enfermedades de notificación obligatoria.

---

## 7. Producto técnico asociado

Este informe se acompaña de un dashboard interactivo que permite explorar
la evolución de la tasa de incidencia por comuna, el efecto iceberg, y las
variables climáticas asociadas. El código fuente, los datos procesados y
la documentación técnica completa —incluyendo el análisis honesto de las
limitaciones del componente predictivo— están disponibles en el
repositorio público del proyecto en GitHub.
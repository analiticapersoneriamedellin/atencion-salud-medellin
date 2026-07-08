# Diccionario de Datos

Corresponde al dataset consolidado `data/processed/pqrd_consolidado.csv`,
generado por `src/parse_pqrd.py`.

## Estructura del archivo consolidado (formato largo/tidy)

| Columna | Tipo | Descripción |
|---|---|---|
| `anio` | Entero | Año del reporte (2021-2026). |
| `mes` | Categórica (texto) | Mes abreviado en español: ENE, FEB, MAR, ABR, MAY, JUN, JUL, AGO, SEP, OCT, NOV, DIC. |
| `tabla_origen` | Categórica | De cuál de las 11 tablas del reporte Supersalud proviene el registro. Valores: `capital_departamento`, `departamento`, `otro_vigilado`, `motivo_especifico_2024_2026`, `motivo_especifico_legacy_2021_2023`. |
| `categoria` | Categórica (texto) | Nombre específico dentro de la tabla de origen (ej. "MEDELLIN", "ANTIOQUIA", o el texto truncado del motivo específico). |
| `valor` | Numérico | Número de reclamos reportados para esa categoría, mes y año. |

## Valores posibles de `categoria` por `tabla_origen`

### `capital_departamento`
- `MEDELLIN`

### `departamento`
- `ANTIOQUIA`

### `otro_vigilado`
- `DIRECCION_SECCIONAL_SALUD_ANTIOQUIA`

### `motivo_especifico_2024_2026` (taxonomía vigente desde julio 2023)
- Negación para la entrega de tecnologías en salud y/o de otros servicios autorizados
- Negación en la asignación de citas o consultas
- Falta de oportunidad en las citas o consultas
- Falta de oportunidad en la atención en otros servicios de salud
- Falta de oportunidad en la entrega o entrega incompleta de tecnologías en salud
- Negación en la atención en otros servicios de salud
- Falta de oportunidad en la autorización de otros servicios de salud
- Falta de oportunidad en la autorización de tecnologías en salud
- Falta de oportunidad en la autorización de citas de consulta
- Falta de oportunidad en el proceso de referencia y contrarreferencia (solo desde 2024)

### `motivo_especifico_legacy_2021_2023` (taxonomía anterior a julio 2023)
- Falta de oportunidad en la asignación de citas de consulta médica especializada
- Falta de oportunidad en la entrega de medicamentos POS
- Demora de la programación de exámenes de laboratorio o diagnósticos
- Falta de oportunidad en la programación de cirugía
- Falta de oportunidad para la prestación de servicios de imagenología
- No aplicación de normas, guías o protocolos de atención
- Deficiencias en la seguridad del paciente
- Falta de oportunidad en la entrega de medicamentos NO POS
- Falta de oportunidad en la asignación de citas de consulta médica general
- Deficiente información sobre derechos, deberes y trámites

## Variable objetivo (target del componente de IA) — PENDIENTE DE DEFINIR

Opciones en evaluación (completar una vez se avance el EDA):

1. **Clasificación de riesgo/anomalía mensual:** ¿el volumen de reclamos de
   un motivo/mes se sale del comportamiento histórico esperado? (similar al
   concepto de "canal endémico" usado en vigilancia epidemiológica).
2. **Predicción de volumen:** estimar el número de reclamos esperado el
   próximo mes para un motivo específico, para anticipar picos.
3. **Priorización/ranking:** ordenar los motivos por severidad de tendencia
   (crecimiento sostenido) para orientar la vigilancia de la Personería.

## Variables predictoras candidatas

- `mes` (estacionalidad).
- `anio` (tendencia de largo plazo).
- `tabla_origen` / `categoria` (tipo de motivo).
- Variables derivadas a construir: variación mes a mes (%), promedio móvil
  de 3 meses, comparación Medellín vs. Antioquia (proporción del
  departamento que corresponde a la capital).
# Fuentes de Datos

## Fuente principal: Reportes PQRD de la Superintendencia Nacional de Salud

**Entidad:** Superintendencia Nacional de Salud (Supersalud).

**Portal oficial:** https://www.supersalud.gov.co/es-co/Paginas/Protecci%C3%B3n%20al%20Usuario/reportes-de-peticiones-quejas-reclamos-o-denuncias.aspx

**Descripción:** reportes periódicos "año corrido" (acumulados desde enero
hasta el mes de corte) del comportamiento de Peticiones, Quejas, Reclamos o
Denuncias (PQRD) y solicitudes de información formuladas por los usuarios
del sistema de salud colombiano.

**Formato:** Excel (.xlsx), con 11 tablas por archivo (total nacional, tipo
de riesgo, canal de radicación, departamento, capital de departamento,
macromotivo, motivo específico, EPS contributivo, EPS subsidiado, EPS
indígena, otro tipo de vigilado).

**Licencia:** información pública oficial, publicada bajo Ley 1712 de 2014
de Transparencia y Acceso a la Información Pública.

### Archivos descargados y usados en este proyecto

| Archivo | Año | Meses cubiertos | Fecha de descarga |
|---|---|---|---|
| RQ-PQRD y solicitudes de información diciembre 2021.xlsx | 2021 | Ene-Dic | [completar] |
| RQ-PQRD y solicitudes de información octubre de 2022.xlsx | 2022 | Ene-Oct | [completar] |
| RQ-PQRD y solicitudes de información octubre de 2023.xlsx | 2023 | Ene-Oct | [completar] |
| RQ-PQRD-y-solicitudes-de-informacion-noviembre-de-2024.xlsx | 2024 | Ene-Nov | [completar] |
| RQ-PQRD y solicitudes de información octubre 2025.xlsx | 2025 | Ene-Oct | [completar] |
| RQ-PQRD y solicitudes de información abril 2026.xlsx | 2026 | Ene-Abr | [completar] |

**Nota:** para completar años faltantes (2019, 2020) o cerrar el año 2026,
descargar del mismo portal el archivo más reciente disponible de cada año
faltante y agregarlo a `data/raw/`, luego volver a correr
`src/parse_pqrd.py` (el script detecta y procesa automáticamente cualquier
archivo `.xlsx` nuevo en esa carpeta).

### Categorías extraídas de cada archivo (ver `src/parse_pqrd.py`)

- Reclamos en salud — Medellín (capital de departamento).
- Reclamos en salud — Antioquia (departamento).
- Reclamos en salud — Dirección Seccional de Salud de Antioquia (otro
  tipo de vigilado).
- Motivos específicos — taxonomía nueva (jul 2023 en adelante): negación
  de tecnologías, negación/falta de oportunidad en citas, autorizaciones,
  atención en otros servicios, referencia y contrarreferencia.
- Motivos específicos — taxonomía legacy (ene 2021 - jun 2023): citas con
  especialista/médico general, entrega de medicamentos POS/NO POS,
  exámenes de laboratorio, programación de cirugía, imagenología,
  protocolos de atención, seguridad del paciente, información sobre
  derechos.

Ver `docs/marco_metodologico.md` para el detalle completo del cambio de
taxonomía confirmado en julio de 2023.

## Cifras de referencia (contexto, no usadas directamente en el modelo)

- El "Abecé del reporte PQRD" de Supersalud confirma que el reporte
  interactivo cubre series desde 2017, con tasas por cada 10.000
  afiliados, y una clasificación jerárquica de 6 macromotivos, 27 motivos
  generales y 228 motivos específicos en su versión completa (el reporte
  descargable que usamos aquí trae los 10 motivos de mayor volumen, no
  los 228 completos).
- Circular Externa 008 de 2018 (Supersalud) y Ley 1755 de 2015 establecen
  los tiempos normativos de respuesta a PQRS (15 días hábiles general, 10
  días para solicitudes de información) — usar como referencia normativa
  si se define un umbral objetivo de "demora" para el componente de IA.

## Fuentes exploradas pero NO usadas (documentar por transparencia)

- **datos.gov.co** — se buscaron datasets de malaria y dengue en una fase
  anterior del proyecto (antes de conocer el plan oficial registrado);
  esa exploración quedó descartada del alcance final. Ver historial de
  decisiones del proyecto si se requiere retomar esa vía en el futuro.
- **Registros internos de la Personería Distrital de Medellín** — no se
  confirmó su disponibilidad a tiempo para este desarrollo; queda como
  posible fuente complementaria para una fase futura del proyecto.
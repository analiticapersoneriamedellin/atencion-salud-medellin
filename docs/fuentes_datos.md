# Fuentes de Datos

## 1. Casos de dengue (fuente principal)

**Entidad:** Alcaldía de Medellín — Secretaría de Salud, vía el portal MEData.

**Dataset:** "Dengue" — SIVIGILA, Medellín.

**ID del dataset:** `1-026-22-000135`

**URL:** https://medata.gov.co/dataset/1-026-22-000135

**Descripción:** casos confirmados/notificados de dengue en Medellín,
reportados al Sistema Nacional de Vigilancia en Salud Pública (SIVIGILA).

**Cobertura:** 2008-2021, 53.813 registros individuales, 38 variables
(demografía, síntomas clínicos, clasificación de gravedad,
hospitalización, barrio, comuna).

**Ventana usada en el análisis:** 2017-2021 (ver justificación en
`docs/marco_metodologico.md`, sección 2).

**Licencia:** información pública oficial, Ley 1712 de 2014.

**Fecha de descarga:** julio de 2026.

## 2. Clima histórico

**Entidad:** Instituto de Hidrología, Meteorología y Estudios Ambientales (IDEAM).

**Datasets (vía API Socrata de datos.gov.co):**

| Variable | Nombre del dataset | Resource ID | URL |
|---|---|---|---|
| Temperatura | Datos Hidrometeorológicos Crudos - Red de Estaciones | `sbwg-7ju4` | https://www.datos.gov.co/resource/sbwg-7ju4.json |
| Precipitación | Datos Hidrometeorológicos Crudos - Red de Estaciones | `s54a-sgyg` | https://www.datos.gov.co/resource/s54a-sgyg.json |

**Estaciones usadas (Medellín):** Aeropuerto Olaya Herrera, Pajarito - AUT
(y variantes de nombre del mismo sitio físico a través del tiempo:
"APTO OLAYA HERRERA - TX GPRS", "AEROPUERTO OLAYA HERRERA", "OLAYA HERRERA").

**Cobertura confirmada empíricamente (no asumida):**
- Temperatura: 2005-2026, continua.
- Precipitación: **2016-2024**, con cobertura real y consistente desde
  2017. Antes de esa fecha, el sensor de precipitación no reportaba
  de forma confiable en las estaciones de Medellín — verificado
  directamente contra la API, no es una limitación documental sino un
  hallazgo empírico del proyecto.

**Nota técnica importante:** existe un dataset distinto ("Datos de
Estaciones de IDEAM y de Terceros", resource_id `57sv-p2fu`) que **solo
contiene observaciones en tiempo real/recientes**, no histórico — se
descartó tras confirmar que todas sus fechas correspondían al mes de la
consulta. Los IDs usados en este proyecto (`sbwg-7ju4`, `s54a-sgyg`) son
los datasets históricos correctos.

**Fecha de descarga:** julio de 2026.

## 3. Población por comuna

**Entidad:** DANE / Departamento Administrativo de Planeación, Alcaldía de Medellín.

**Dataset:** "Proyecciones de Población por comuna y corregimiento 2018-2030".

**Contrato:** interadministrativo No. 4600085225 de 2020, DANE - Municipio
de Medellín, base de proyección Censo 2018.

**URL:** https://medata.gov.co/ (buscar "Proyecciones de Población")

**Cobertura:** 2018-2030, por comuna/corregimiento, desagregado por sexo
(sumado a total en este proyecto).

**Limitación:** no cubre 2017. Se usó la población de 2018 como
aproximación para ese año (supuesto documentado en
`docs/marco_metodologico.md`, sección 8).

**Fecha de descarga:** julio de 2026.

## 4. Literatura científica de respaldo (no es un dataset, es evidencia externa)

**Fuente:** "Integrated vector management program in the framework of the
COVID-19 pandemic in Medellín, Colombia", publicado en PMC (revista
científica revisada por pares).

**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC10495193/

**Uso en el proyecto:** confirmación externa e independiente de que el
programa de vigilancia entomológica de Medellín cambió de metodología
(de vigilancia domiciliaria a institucional) durante 2018-2021, evidencia
citada como Hallazgo 3 en `reports/informe_descriptivo.md`.

## 5. Fuentes exploradas pero NO usadas en la versión final (transparencia)

- **PQRD de Supersalud** (proyecto de fase anterior, sobre atención
  oportuna en salud): descartado tras decisión de reformular el proyecto
  completo hacia dengue, alineado con el enunciado original del reto.
  Documentación e implementación completa disponibles en el historial de
  commits del repositorio, por transparencia.
- **Portal de datos abiertos del Área Metropolitana del Valle de Aburrá**
  (`datosabiertos.metropol.gov.co`): explorado como fuente climática
  alternativa, descartado por bloqueo de acceso automatizado (robots.txt)
  y disponibilidad de una alternativa funcional (IDEAM vía datos.gov.co).
- **Dataset "Datos de Estaciones de IDEAM y de Terceros"** (`57sv-p2fu`):
  descartado por no tener histórico (ver sección 2).
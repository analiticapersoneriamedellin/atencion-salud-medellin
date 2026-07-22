# 🦟 Vigilancia Epidemiológica de Dengue — Medellín

**Concurso Datos al Ecosistema 2026: IA para Colombia — Ministerio TIC**
**Reto:** Salud y Bienestar (ID 117) · **Equipo:** 330
**Para:** Personería Distrital de Medellín

## Descripción

Análisis de datos e inteligencia artificial que investiga si la caída del
90% en los casos de dengue notificados en Medellín entre 2017 y 2021
refleja una mejora epidemiológica real o un patrón de subregistro
creciente en el sistema de vigilancia — con implicaciones directas para
la labor de vigilancia de derechos de la Personería Distrital de Medellín.

## Hallazgos principales

1. La tasa de incidencia de dengue cayó de **80,7 a 8,2 casos por
   100.000 habitantes** (2017-2021), una reducción del 90%.
2. La proporción de casos hospitalizados **casi se triplicó** (15,3% →
   43,8%) en el mismo período — señal característica de subregistro: solo
   los casos graves siguen siendo captados por el sistema.
3. Un estudio científico revisado por pares confirma que el programa de
   vigilancia entomológica de Medellín cambió de metodología durante
   2018-2021, coincidiendo con el período analizado.

Ver el [informe descriptivo completo](reports/informe_descriptivo.md)
para el detalle y las recomendaciones institucionales.

## Estructura del repositorio

```
├── docs/                       # Documentación técnica
│   ├── planteamiento_problema.md
│   ├── marco_metodologico.md   # CRISP-ML, los 3 hallazgos, limitaciones honestas
│   ├── fuentes_datos.md        # Trazabilidad completa de las 3 fuentes usadas
│   └── data_dictionary.md      # Diccionario de variables
├── data/
│   ├── raw/                    # Dengue (SIVIGILA), clima (IDEAM), población (DANE)
│   └── processed/              # Datasets consolidados y resultados de análisis
├── src/
│   ├── ingest_clima.py                  # Descarga histórica IDEAM
│   ├── consolidar_dengue_clima.py       # Cruce dengue+clima (usado en el modelo)
│   ├── analisis_incidencia_iceberg.py   # Los 3 pilares del análisis central
│   └── train_modelo_dengue.py           # Intento de modelo predictivo (documentado)
├── reports/
│   └── informe_descriptivo.md  # Hallazgos y recomendaciones para la Personería
└── dashboard/
    └── app.py                  # Dashboard interactivo (Streamlit)
```

## Cómo ejecutar el proyecto

```bash
pip install -r requirements.txt

# 1. Descargar histórico climático de IDEAM
python src/ingest_clima.py

# 2. Ejecutar el análisis central (tasa de incidencia + efecto iceberg)
python src/analisis_incidencia_iceberg.py

# 3. Ejecutar el dashboard interactivo
streamlit run dashboard/app.py
```

## Fuentes de datos

SIVIGILA vía MEData (dengue), IDEAM (clima histórico), DANE/Alcaldía de
Medellín (población por comuna). Ver
[`docs/fuentes_datos.md`](docs/fuentes_datos.md) para trazabilidad
completa (IDs, URLs, fechas de descarga, licencias).

## Metodología

CRISP-ML(Q). Ver [`docs/marco_metodologico.md`](docs/marco_metodologico.md),
que incluye la documentación transparente de un intento de modelo
predictivo (Random Forest) cuyo desempeño no fue satisfactorio, y la
decisión metodológica de priorizar análisis descriptivo riguroso en su
lugar.

## Stack técnico

Python · Pandas · Scikit-learn · Streamlit · Plotly · GitHub · Hugging Face Spaces (despliegue)

## Nivel de complejidad

**Intermedio**, según los criterios del concurso: 3 fuentes de datos
estructuradas, más de 20 variables entre las distintas fases del análisis,
y más de 50.000 registros base (53.813 casos de dengue individuales, antes
de agregación).

## Equipo

Equipo 330 — Personería Distrital de Medellín

## Recursos del Proyecto

| Recurso | Enlace |
|---|---|
| Dashboard interactivo (Streamlit) | https://huggingface.co/spaces/unidad-analitica-personeria/atencion-salud-medellin |
| Presentación de la sustentación | https://app.slidesai.io/p/0c872193-8143-4f4f-a8aa-156f8eaef7de |
| PowerBi el cual presenta datos complentarios incluyendo una estructura amigable | [https://app.slidesai.io/p/0c872193-8143-4f4f-a8aa-156f8eaef7de](https://app.powerbi.com/view?r=eyJrIjoiMTE1ZWJiODgtNmJkOC00YzBjLTkyNmItOWIzMjkzNTRlNDI2IiwidCI6ImEyYmE0MzQ1LTc3NjQtNGQyMi1iNmExLTdjZjUyOGYzYjNhNSIsImMiOjR9&pageName=b069b11e664507033db4) |
| Página web del proyecto | https://dengue-insight-hub.lovable.app/ |

## Licencia

MIT

"""
app.py — Vigilancia Epidemiológica de Dengue en Medellín
Concurso Datos al Ecosistema 2026: IA para Colombia
Personería Distrital de Medellín

Ejecutar con:
    streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

st.set_page_config(
    page_title="Vigilancia Dengue Medellín | Datos al Ecosistema 2026",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    .stMetric {
        background-color: #1a1f2e;
        border: 1px solid #2d3548;
        border-radius: 12px;
        padding: 16px 20px;
    }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; color: #fafafa !important; }
    div[data-testid="stMetricLabel"] { color: #cbd5e1 !important; }
    div[data-testid="stMetricDelta"] { color: #fafafa !important; }
    h1, h2, h3 { font-family: 'Segoe UI', sans-serif; color: #fafafa !important; }
    p, span, label, .stCaption, div[data-testid="stCaptionContainer"] { color: #cbd5e1; }
    .header-container {
        padding: 1.2rem 1.5rem;
        background: linear-gradient(135deg, #1e5f3a 0%, #0e1117 100%);
        border-radius: 14px;
        border-left: 5px solid #2ecc71;
        margin-bottom: 1.5rem;
    }
    .header-container h1 { color: #ffffff !important; margin-bottom: 0; }
    .header-container p { color: #cbd5e1 !important; margin-top: 4px; }
    .finding-box {
        background-color: #1a1f2e;
        border-left: 4px solid #e74c3c;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
        color: #fafafa !important;
    }
    .action-box {
        background-color: #16241e;
        border-left: 4px solid #2ecc71;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
        color: #fafafa !important;
    }
    .warning-box {
        background-color: #2d1518;
        border-left: 4px solid #e74c3c;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
        color: #fafafa !important;
    }
    button[data-baseweb="tab"] { color: #cbd5e1 !important; }
    button[data-baseweb="tab"][aria-selected="true"] { color: #ffffff !important; }
    section[data-testid="stSidebar"] { background-color: #131722; }
    section[data-testid="stSidebar"] * { color: #e2e8f0; }
    .footer-note {
        font-size: 12px;
        color: #6b7280 !important;
        border-top: 1px solid #2d3548;
        padding-top: 12px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

COLOR_PRIMARIO = "#2ecc71"
COLOR_ALERTA = "#e74c3c"
COLOR_SECUNDARIO = "#3498db"
COLOR_NARANJA = "#e67e22"

# ============================================================
# CARGA DE DATOS
# ============================================================
@st.cache_data
def cargar_datos():
    datos = {}
    try:
        datos["incidencia"] = pd.read_csv("data/processed/dengue_tasa_incidencia.csv")
        datos["iceberg"] = pd.read_csv("data/processed/dengue_efecto_iceberg.csv")
    except FileNotFoundError:
        return None

    # Estos dos son opcionales -- si no existen, esas pestañas avisan
    # en vez de romper el resto del dashboard.
    try:
        datos["correlacion"] = pd.read_csv("data/processed/correlacion_clima_dengue.csv")
    except FileNotFoundError:
        datos["correlacion"] = None

    try:
        datos["canal"] = pd.read_csv("data/processed/canal_endemico.csv")
    except FileNotFoundError:
        datos["canal"] = None

    return datos

datos = cargar_datos()

if datos is None:
    st.error(
        "⚠️ No se encontraron los archivos de datos procesados. "
        "Ejecuta primero los scripts en src/ (ingest_clima.py, "
        "analisis_incidencia_iceberg.py) para generar los datasets."
    )
    st.stop()

incidencia = datos["incidencia"]
iceberg = datos["iceberg"]
correlacion = datos["correlacion"]
canal = datos["canal"]

# ============================================================
# ENCABEZADO
# ============================================================
st.markdown("""
<div class="header-container">
    <h1 style="margin-bottom:0;">🦟 Vigilancia Epidemiológica de Dengue — Medellín</h1>
    <p style="color:#cbd5e1; margin-top:4px;">
    Concurso Datos al Ecosistema 2026: IA para Colombia · Personería Distrital de Medellín ·
    Fuentes: SIVIGILA/MEData, IDEAM, DANE
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# BARRA LATERAL
# ============================================================
st.sidebar.header("🔎 Filtros")
comunas_disponibles = sorted(incidencia["comuna"].unique())
comuna_sel = st.sidebar.multiselect(
    "Comunas a mostrar (pestaña Por Comuna)",
    options=comunas_disponibles,
    default=[],
)
st.sidebar.markdown("---")
st.sidebar.caption(
    "**Pregunta de investigación:** ¿la caída del 90% en dengue notificado "
    "(2017-2021) refleja una mejora real, o subregistro creciente? "
    "Ver metodología completa en `docs/marco_metodologico.md`."
)

# ============================================================
# KPIs PRINCIPALES
# ============================================================
tasa_2017 = incidencia[incidencia["anio"] == 2017]["tasa_incidencia_100k"].mean()
tasa_2021 = incidencia[incidencia["anio"] == 2021]["tasa_incidencia_100k"].mean()
caida_pct = (1 - tasa_2021 / tasa_2017) * 100 if tasa_2017 else 0

hosp_2017 = iceberg[iceberg["anio"] == 2017]["proporcion_hospitalizados"].values[0]
hosp_2021 = iceberg[iceberg["anio"] == 2021]["proporcion_hospitalizados"].values[0]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Tasa de incidencia 2017", f"{tasa_2017:.1f} / 100k hab.")
with col2:
    st.metric("Tasa de incidencia 2021", f"{tasa_2021:.1f} / 100k hab.",
               delta=f"-{caida_pct:.0f}%", delta_color="inverse")
with col3:
    st.metric("% Hospitalizados 2017", f"{hosp_2017*100:.1f}%")
with col4:
    st.metric("% Hospitalizados 2021", f"{hosp_2021*100:.1f}%",
               delta=f"+{(hosp_2021-hosp_2017)*100:.1f} pp", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📉 Tendencia e Incidencia", "🧊 Efecto Iceberg", "🗺️ Por Comuna",
    "🌡️ Correlación Clima", "📡 Canal Endémico", "💡 Hallazgos y Recomendaciones"
])

# --- TAB 1: TENDENCIA ---
with tab1:
    st.subheader("Tasa de incidencia promedio de dengue en Medellín (2017-2021)")

    tendencia = incidencia.groupby("anio")["tasa_incidencia_100k"].mean().reset_index()
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=tendencia["anio"], y=tendencia["tasa_incidencia_100k"],
        mode="lines+markers", line=dict(color=COLOR_PRIMARIO, width=4),
        marker=dict(size=12), fill="tozeroy", fillcolor="rgba(46,204,113,0.15)",
        hovertemplate="Año %{x}<br>%{y:.1f} casos/100k hab.<extra></extra>",
    ))
    fig.update_layout(
        template="plotly_dark", height=420,
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis=dict(title="Año", dtick=1, gridcolor="#2d3548"),
        yaxis=dict(title="Tasa por 100.000 habitantes", gridcolor="#2d3548"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        f"💡 La tasa de incidencia cayó **{caida_pct:.0f}%** entre 2017 y 2021. "
        "Ver pestaña 'Hallazgos' para la interpretación completa."
    )

# --- TAB 2: ICEBERG ---
with tab2:
    st.subheader("Efecto 'punta del iceberg': proporción de casos hospitalizados")

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        x=iceberg["anio"], y=iceberg["total_casos"], name="Casos totales",
        marker_color=COLOR_SECUNDARIO, yaxis="y1",
    ))
    fig2.add_trace(go.Scatter(
        x=iceberg["anio"], y=iceberg["proporcion_hospitalizados"] * 100,
        name="% Hospitalizados", mode="lines+markers",
        line=dict(color=COLOR_ALERTA, width=4), marker=dict(size=12),
        yaxis="y2",
    ))
    fig2.update_layout(
        template="plotly_dark", height=450,
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis=dict(title="Año", dtick=1, gridcolor="#2d3548"),
        yaxis=dict(title="Casos totales", side="left", gridcolor="#2d3548"),
        yaxis2=dict(title="% Hospitalizados", side="right", overlaying="y", range=[0, 50]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption(
        "💡 Mientras los casos totales (barras azules) caen, el porcentaje de "
        "hospitalizados (línea roja) sube — señal característica de subregistro: "
        "solo los casos graves siguen siendo captados por el sistema."
    )

# --- TAB 3: POR COMUNA ---
with tab3:
    st.subheader("Tasa de incidencia por comuna")

    datos_mapa = incidencia.copy()
    if comuna_sel:
        datos_mapa = datos_mapa[datos_mapa["comuna"].isin(comuna_sel)]

    fig3 = px.line(
        datos_mapa, x="anio", y="tasa_incidencia_100k", color="comuna",
        template="plotly_dark", height=500,
        labels={"tasa_incidencia_100k": "Tasa por 100k hab.", "anio": "Año"},
    )
    fig3.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis=dict(dtick=1, gridcolor="#2d3548"),
        yaxis=dict(gridcolor="#2d3548"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Ranking de comunas por tasa de incidencia (2017, año base)")
    ranking_2017 = incidencia[incidencia["anio"] == 2017].sort_values(
        "tasa_incidencia_100k", ascending=True
    )
    fig4 = go.Figure(go.Bar(
        x=ranking_2017["tasa_incidencia_100k"], y=ranking_2017["comuna"],
        orientation="h", marker_color=COLOR_PRIMARIO,
    ))
    fig4.update_layout(
        template="plotly_dark", height=500,
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis=dict(title="Tasa por 100.000 hab.", gridcolor="#2d3548"),
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig4, use_container_width=True)

# --- TAB 4: CORRELACIÓN CLIMA (NUEVA) ---
with tab4:
    st.subheader("Correlación entre variables climáticas y casos de dengue")

    if correlacion is None:
        st.warning(
            "⚠️ No se encontró `data/processed/correlacion_clima_dengue.csv`. "
            "Corre `python src/correlacion_estacionalidad.py` para generarlo."
        )
    else:
        corr_ordenada = correlacion.sort_values("pearson_r")
        colores = [COLOR_SECUNDARIO if r < 0 else COLOR_NARANJA for r in corr_ordenada["pearson_r"]]

        fig5 = go.Figure(go.Bar(
            x=corr_ordenada["pearson_r"], y=corr_ordenada["variable"],
            orientation="h", marker_color=colores,
            text=[f"r = {r:+.2f}" for r in corr_ordenada["pearson_r"]],
            textposition="outside",
            hovertemplate="%{y}<br>Pearson r = %{x:.3f}<extra></extra>",
        ))
        fig5.add_vline(x=0, line_color="#4b5563", line_width=1)
        fig5.update_layout(
            template="plotly_dark", height=420,
            margin=dict(t=20, b=20, l=20, r=60),
            xaxis=dict(title="Coeficiente de correlación de Pearson", gridcolor="#2d3548",
                       range=[-0.5, 0.5]),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig5, use_container_width=True)

        n_sig = corr_ordenada["significativo_pearson_95pct"].sum()
        st.caption(
            f"💡 Las {n_sig} de {len(corr_ordenada)} variables climáticas son "
            "estadísticamente significativas (p < 0.05). Hallazgo inesperado: "
            "**más temperatura se asocia con MENOS casos** en Medellín (azul), "
            "posiblemente por el clima templado particular de la ciudad — "
            "contrario al patrón típico de ciudades cálidas. La "
            "**precipitación** (naranja) sí va en la dirección biológica esperada."
        )

        with st.expander("Ver tabla completa de resultados"):
            st.dataframe(correlacion, use_container_width=True)

# --- TAB 5: CANAL ENDÉMICO (NUEVA) ---
with tab5:
    st.subheader("Canal endémico 2021 (método Bortman, mismo que usa el INS)")

    if canal is None:
        st.warning(
            "⚠️ No se encontró `data/processed/canal_endemico.csv`. "
            "Corre `python src/canal_endemico.py` para generarlo."
        )
    else:
        fig6 = go.Figure()

        # Banda de confianza histórica (área sombreada)
        fig6.add_trace(go.Scatter(
            x=canal["semana"], y=canal["canal_superior"],
            mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip",
        ))
        fig6.add_trace(go.Scatter(
            x=canal["semana"], y=canal["canal_inferior"],
            mode="lines", line=dict(width=0), fill="tonexty",
            fillcolor="rgba(46,204,113,0.15)", name="Banda histórica esperada",
            hoverinfo="skip",
        ))
        fig6.add_trace(go.Scatter(
            x=canal["semana"], y=canal["canal_medio"],
            mode="lines", line=dict(color="#4b5563", width=1, dash="dot"),
            name="Media histórica",
        ))
        fig6.add_trace(go.Scatter(
            x=canal["semana"], y=canal["casos"],
            mode="lines+markers", line=dict(color=COLOR_PRIMARIO, width=3),
            marker=dict(size=5), name="Casos reales 2021",
        ))

        fig6.update_layout(
            template="plotly_dark", height=450,
            margin=dict(t=20, b=20, l=20, r=20),
            xaxis=dict(title="Semana epidemiológica", gridcolor="#2d3548"),
            yaxis=dict(title="Casos", gridcolor="#2d3548"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig6, use_container_width=True)

        semanas_alerta = canal[canal["zona"].isin(["Epidemia", "Alerta"])]
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Semanas en zona de Éxito/Seguridad", int((canal["zona"].isin(["Éxito","Seguridad"])).sum()))
        with col_b:
            st.metric("Semanas en zona de Alerta/Epidemia", len(semanas_alerta))

        st.markdown("""
        <div class="warning-box">
        ⚠️ <b>Esto no es tranquilizador:</b> el canal endémico solo puede evaluar
        los casos que el sistema efectivamente captura. Si el subregistro aumenta,
        esta herramienta oficial se vuelve ciega al problema real, dando una falsa
        sensación de seguridad — 2021 no muestra ninguna alerta precisamente en el
        año con mayor proporción de hospitalizados (ver pestaña Efecto Iceberg).
        </div>
        """, unsafe_allow_html=True)

# --- TAB 6: HALLAZGOS ---
with tab6:
    st.subheader("Síntesis de hallazgos")

    st.markdown(f"""
    <div class="finding-box">
    <b>Hallazgo 1 — Tendencia:</b> la tasa de incidencia de dengue cayó de
    {tasa_2017:.1f} a {tasa_2021:.1f} casos por 100.000 habitantes
    ({caida_pct:.0f}%) entre 2017 y 2021.
    </div>
    <div class="finding-box">
    <b>Hallazgo 2 — Efecto iceberg:</b> la proporción de casos hospitalizados
    subió de {hosp_2017*100:.1f}% a {hosp_2021*100:.1f}% en el mismo período —
    señal de que solo los casos graves siguen siendo captados por el sistema.
    </div>
    <div class="finding-box">
    <b>Hallazgo 3 — Literatura científica:</b> un estudio revisado por pares
    confirma que el programa de vigilancia entomológica de Medellín cambió de
    metodología (de domiciliaria a institucional) durante 2018-2021, por la
    pandemia.
    </div>
    <div class="finding-box">
    <b>Hallazgo 4 — Correlación climática:</b> todas las variables climáticas
    analizadas muestran correlación estadísticamente significativa con los
    casos de dengue, con un patrón inesperado de temperatura (negativo) que
    amerita más estudio.
    </div>
    <div class="finding-box">
    <b>Hallazgo 5 — Canal endémico:</b> el método oficial del INS no detecta
    ninguna alerta en 2021, justo el año con mayor evidencia de subregistro —
    demostrando el límite de esta herramienta cuando el sistema de captura falla.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Recomendaciones")
    st.markdown("""
    <div class="action-box">1. Solicitar a la Secretaría de Salud una explicación formal sobre la evolución del programa de vigilancia entomológica desde la pandemia.</div>
    <div class="action-box">2. Priorizar el seguimiento de comunas con tasas de incidencia históricamente altas y verificar la asignación de recursos de control vectorial.</div>
    <div class="action-box">3. Indagar sobre el acceso oportuno a diagnóstico temprano de dengue, dado el aumento de casos hospitalizados.</div>
    <div class="action-box">4. Promover el monitoreo periódico de este indicador como alerta temprana, replicable a otras enfermedades de notificación obligatoria.</div>
    """, unsafe_allow_html=True)

    st.info(
        "📄 Ver el informe completo en `reports/informe_descriptivo.md` y la "
        "metodología detallada, incluyendo limitaciones, en "
        "`docs/marco_metodologico.md`."
    )

st.markdown("""
<div class="footer-note">
Fuentes: SIVIGILA vía MEData (dengue), IDEAM (clima), DANE/Alcaldía de Medellín (población).
Metodología y limitaciones documentadas en docs/marco_metodologico.md.
Proyecto desarrollado para el Concurso Datos al Ecosistema 2026: IA para Colombia — Ministerio TIC.
</div>
""", unsafe_allow_html=True)
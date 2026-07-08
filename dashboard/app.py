"""
app.py — Dashboard de Vigilancia de Atención Oportuna en Salud, Medellín
Concurso Datos al Ecosistema 2026: IA para Colombia
Personería Distrital de Medellín

Ejecutar con:
    streamlit run dashboard/app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(
    page_title="Vigilancia Salud Medellín | Datos al Ecosistema 2026",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# ESTILOS PERSONALIZADOS (CSS)
# ============================================================
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .stMetric {
        background-color: #1a1f2e;
        border: 1px solid #2d3548;
        border-radius: 12px;
        padding: 16px 20px;
    }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: 700; }
    h1, h2, h3 { font-family: 'Segoe UI', sans-serif; }
    .header-container {
        padding: 1.2rem 1.5rem;
        background: linear-gradient(135deg, #1e3a5f 0%, #0e1117 100%);
        border-radius: 14px;
        border-left: 5px solid #ff4b4b;
        margin-bottom: 1.5rem;
    }
    .alert-box {
        background-color: #2d1518;
        border-left: 4px solid #ff4b4b;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
    .footer-note {
        font-size: 12px;
        color: #6b7280;
        border-top: 1px solid #2d3548;
        padding-top: 12px;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Paleta de colores consistente (tema salud/alerta)
COLOR_BAJO = "#2ecc71"
COLOR_MEDIO = "#f39c12"
COLOR_ALTO = "#e74c3c"
COLOR_PRIMARIO = "#3498db"
MAPA_RIESGO = {"bajo": COLOR_BAJO, "medio": COLOR_MEDIO, "alto": COLOR_ALTO}

ORDEN_MESES = ["ENE","FEB","MAR","ABR","MAY","JUN","JUL","AGO","SEP","OCT","NOV","DIC"]

# ============================================================
# CARGA DE DATOS
# ============================================================
@st.cache_data
def cargar_datos():
    try:
        df_medellin = pd.read_csv("data/processed/pqrd_consolidado.csv")
        df_medellin['mes'] = pd.Categorical(df_medellin['mes'], categories=ORDEN_MESES, ordered=True)
        df_modelo = pd.read_csv("data/processed/medellin_dataset_modelo.csv")
        df_modelo['mes'] = pd.Categorical(df_modelo['mes'], categories=ORDEN_MESES, ordered=True)
        return df_medellin, df_modelo
    except FileNotFoundError:
        return None, None

df_medellin, df_modelo = cargar_datos()

if df_medellin is None:
    st.error(
        "⚠️ No se encontraron los archivos de datos procesados. "
        "Ejecuta primero `python src/parse_pqrd.py` y el notebook de "
        "análisis exploratorio para generar `data/processed/pqrd_consolidado.csv` "
        "y `data/processed/medellin_dataset_modelo.csv`."
    )
    st.stop()

# ============================================================
# ENCABEZADO
# ============================================================
st.markdown("""
<div class="header-container">
    <h1 style="margin-bottom:0;">🩺 Vigilancia de Atención Oportuna en Salud — Medellín</h1>
    <p style="color:#a0aec0; margin-top:4px;">
    Concurso Datos al Ecosistema 2026: IA para Colombia · Personería Distrital de Medellín ·
    Fuente: Superintendencia Nacional de Salud (PQRD)
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# BARRA LATERAL — FILTROS
# ============================================================
st.sidebar.header("🔎 Filtros")
medellin_serie = df_medellin[df_medellin['categoria'] == 'MEDELLIN'].copy()
anios_disponibles = sorted(medellin_serie['anio'].unique())
anio_rango = st.sidebar.select_slider(
    "Rango de años",
    options=anios_disponibles,
    value=(anios_disponibles[0], anios_disponibles[-1]),
)

nivel_filtro = st.sidebar.multiselect(
    "Nivel de riesgo (mapa de calor y alertas)",
    options=["bajo", "medio", "alto"],
    default=["alto"],
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "**Metodología:** los reclamos por motivo específico en Medellín se "
    "estiman aplicando la proporción nacional de cada motivo al volumen "
    "total de reclamos de Medellín (supuesto documentado en "
    "`docs/marco_metodologico.md`)."
)

# Filtrar por rango de años
medellin_f = medellin_serie[(medellin_serie['anio'] >= anio_rango[0]) & (medellin_serie['anio'] <= anio_rango[1])].copy()
medellin_f = medellin_f.sort_values(['anio','mes'])
medellin_f['periodo'] = medellin_f['anio'].astype(str) + '-' + medellin_f['mes'].astype(str)

df_modelo_f = df_modelo[(df_modelo['anio'] >= anio_rango[0]) & (df_modelo['anio'] <= anio_rango[1])].copy()

# ============================================================
# KPIs PRINCIPALES
# ============================================================
col1, col2, col3, col4 = st.columns(4)

total_periodo = medellin_f['valor'].sum()
primer_valor = medellin_f['valor'].iloc[0] if len(medellin_f) else 0
ultimo_valor = medellin_f['valor'].iloc[-1] if len(medellin_f) else 0
crecimiento = ((ultimo_valor - primer_valor) / primer_valor * 100) if primer_valor else 0
alertas_altas = df_modelo_f[df_modelo_f['nivel_riesgo']=='alto'].shape[0] if 'nivel_riesgo' in df_modelo_f else 0
motivo_top = (
    df_modelo_f.groupby('categoria')['reclamos_estimados_medellin'].sum().idxmax()
    if 'reclamos_estimados_medellin' in df_modelo_f.columns and len(df_modelo_f) else "N/D"
)

with col1:
    st.metric("Reclamos totales (período)", f"{total_periodo:,.0f}")
with col2:
    st.metric("Variación primer→último mes", f"{crecimiento:+.1f}%",
               delta=f"{crecimiento:+.1f}%", delta_color="inverse")
with col3:
    st.metric("Alertas de riesgo alto detectadas", f"{alertas_altas}")
with col4:
    st.metric("Motivo con mayor volumen", motivo_top[:28] + "..." if len(str(motivo_top)) > 28 else motivo_top)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# TABS DE NAVEGACIÓN
# ============================================================
tab1, tab2, tab3 = st.tabs(["📈 Tendencia General", "🗺️ Mapa de Riesgo por Motivo", "🚨 Alertas Activas"])

# --- TAB 1: TENDENCIA ---
with tab1:
    st.subheader("Evolución mensual de reclamos en salud — Medellín")

    fig_linea = go.Figure()
    fig_linea.add_trace(go.Scatter(
        x=medellin_f['periodo'], y=medellin_f['valor'],
        mode='lines+markers', name='Reclamos',
        line=dict(color=COLOR_PRIMARIO, width=3),
        marker=dict(size=6),
        fill='tozeroy', fillcolor='rgba(52,152,219,0.1)',
        hovertemplate='%{x}<br>%{y:,.0f} reclamos<extra></extra>',
    ))

    # Línea de promedio móvil de 3 meses
    medellin_f['promedio_movil'] = medellin_f['valor'].rolling(3, min_periods=1).mean()
    fig_linea.add_trace(go.Scatter(
        x=medellin_f['periodo'], y=medellin_f['promedio_movil'],
        mode='lines', name='Promedio móvil (3 meses)',
        line=dict(color='#f39c12', width=2, dash='dash'),
    ))

    fig_linea.update_layout(
        template='plotly_dark', height=450,
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis=dict(tickangle=-90, showgrid=False),
        yaxis=dict(title="Número de reclamos", gridcolor='#2d3548'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_linea, use_container_width=True)

    st.caption(
        "💡 **Lectura:** el volumen de reclamos en salud en Medellín muestra una "
        "tendencia sostenida al alza en el período analizado. El promedio móvil "
        "(línea punteada) suaviza la variación mes a mes para revelar la tendencia real."
    )

    # Comparación Medellín vs Antioquia
    st.subheader("Medellín como proporción del departamento (Antioquia)")
    antioquia_f = df_medellin[(df_medellin['categoria']=='ANTIOQUIA') &
                               (df_medellin['anio']>=anio_rango[0]) & (df_medellin['anio']<=anio_rango[1])].copy()
    antioquia_f = antioquia_f.sort_values(['anio','mes'])
    antioquia_f['periodo'] = antioquia_f['anio'].astype(str) + '-' + antioquia_f['mes'].astype(str)

    comparacion = medellin_f[['periodo','valor']].merge(
        antioquia_f[['periodo','valor']], on='periodo', suffixes=('_medellin','_antioquia'))
    comparacion['proporcion_medellin'] = comparacion['valor_medellin'] / comparacion['valor_antioquia'] * 100

    fig_prop = px.area(comparacion, x='periodo', y='proporcion_medellin',
                        template='plotly_dark', height=300)
    fig_prop.update_traces(line_color=COLOR_PRIMARIO, fillcolor='rgba(52,152,219,0.2)')
    fig_prop.update_layout(
        margin=dict(t=10, b=20, l=20, r=20),
        yaxis=dict(title="% del total departamental", gridcolor='#2d3548'),
        xaxis=dict(tickangle=-90, showgrid=False, title=""),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_prop, use_container_width=True)

# --- TAB 2: MAPA DE CALOR ---
with tab2:
    st.subheader("Mapa de riesgo por motivo específico y mes")
    st.caption(
        "Nivel de riesgo calculado mediante z-score respecto al histórico de cada "
        "motivo (ver `docs/marco_metodologico.md`). Solo se muestra el período "
        "2024-2026, taxonomía de motivos consistente."
    )

    if 'reclamos_estimados_medellin' in df_modelo_f.columns:
        pivot = df_modelo_f.pivot_table(
            index='categoria', columns=['anio','mes'], values='z_score', observed=True
        )
        pivot.columns = [f"{a}-{m}" for a, m in pivot.columns]
        pivot.index = [c[:55] for c in pivot.index]

        fig_heat = go.Figure(data=go.Heatmap(
            z=pivot.values, x=pivot.columns, y=pivot.index,
            colorscale='RdYlGn_r', zmid=0,
            colorbar=dict(title="Z-score"),
            hovertemplate='%{y}<br>%{x}<br>Z-score: %{z:.2f}<extra></extra>',
        ))
        fig_heat.update_layout(
            template='plotly_dark', height=500,
            margin=dict(t=20, b=20, l=20, r=20),
            xaxis=dict(tickangle=-90, showgrid=False),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("Ranking de motivos por volumen total (estimado Medellín)")
    ranking = df_modelo_f.groupby('categoria')['reclamos_estimados_medellin'].sum().sort_values()
    fig_bar = go.Figure(go.Bar(
        x=ranking.values, y=[c[:55] for c in ranking.index], orientation='h',
        marker_color=COLOR_PRIMARIO,
        hovertemplate='%{y}<br>%{x:,.0f} reclamos estimados<extra></extra>',
    ))
    fig_bar.update_layout(
        template='plotly_dark', height=400,
        margin=dict(t=20, b=20, l=20, r=20),
        xaxis=dict(title="Reclamos estimados", gridcolor='#2d3548'),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- TAB 3: ALERTAS ---
with tab3:
    st.subheader("🚨 Casos de riesgo activo")

    alertas = df_modelo_f[df_modelo_f['nivel_riesgo'].isin(nivel_filtro)].copy()
    alertas = alertas.sort_values(['anio','mes'], ascending=[False, False])

    if len(alertas) == 0:
        st.info("No hay alertas para los filtros seleccionados.")
    else:
        for _, row in alertas.head(20).iterrows():
            color = MAPA_RIESGO.get(row['nivel_riesgo'], '#888')
            st.markdown(f"""
            <div class="alert-box" style="border-left-color:{color};">
                <b>{row['anio']}-{row['mes']}</b> ·
                <span style="color:{color}; font-weight:600;">{row['nivel_riesgo'].upper()}</span><br>
                {row['categoria']}<br>
                <span style="color:#a0aec0;">
                {row['reclamos_estimados_medellin']:,.0f} reclamos estimados ·
                variación {row['variacion_pct']:+.1f}% vs. mes anterior
                </span>
            </div>
            """, unsafe_allow_html=True)

    st.download_button(
        "⬇️ Descargar alertas filtradas (CSV)",
        data=alertas.to_csv(index=False).encode('utf-8'),
        file_name="alertas_riesgo_salud_medellin.csv",
        mime="text/csv",
    )

# ============================================================
# PIE DE PÁGINA
# ============================================================
st.markdown("""
<div class="footer-note">
Fuente: Superintendencia Nacional de Salud (Supersalud) — Reportes PQRD 2021-2026.
Metodología y limitaciones documentadas en docs/marco_metodologico.md.
Proyecto desarrollado para el Concurso Datos al Ecosistema 2026: IA para Colombia — Ministerio TIC.
</div>
""", unsafe_allow_html=True)
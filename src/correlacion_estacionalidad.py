"""
correlacion_estacionalidad.py
Dos análisis complementarios usando los datos ya consolidados:

1. CORRELACIÓN ESTADÍSTICA REAL entre clima (temperatura, precipitación,
   con rezagos) y casos de dengue a nivel ciudad -- da un número concreto
   (coeficiente de Pearson y Spearman) en vez de solo la importancia de
   variables del modelo Random Forest que ya sabemos que no generalizó bien.

2. ESTACIONALIDAD: promedio de casos por mes del año (combinando los 5
   años 2017-2021), para ver si hay un patrón estacional claro.

Uso:
    cd src
    python correlacion_estacionalidad.py
"""

import pandas as pd
from scipy import stats

RUTA_DATOS = "../data/processed/dengue_ciudad_consolidado.csv"
RUTA_DENGUE_RAW = "../data/raw/sivigila_dengue.csv"
RUTA_SALIDA_CORR = "../data/processed/correlacion_clima_dengue.csv"
RUTA_SALIDA_ESTACIONAL = "../data/processed/estacionalidad_mensual.csv"


def analizar_correlacion():
    print("=" * 60)
    print("ANÁLISIS 1: CORRELACIÓN CLIMA-DENGUE")
    print("=" * 60)

    df = pd.read_csv(RUTA_DATOS)
    df = df.dropna(subset=["casos_dengue"])

    variables_clima = [
        "temperatura_promedio", "precipitacion_acumulada",
        "temperatura_lag2", "precipitacion_lag2",
        "temperatura_lag4", "precipitacion_lag4",
    ]

    resultados = []
    for var in variables_clima:
        sub = df.dropna(subset=[var, "casos_dengue"])
        if len(sub) < 10:
            print(f"[WARN] '{var}': muy pocos datos válidos ({len(sub)}), se omite")
            continue

        pearson_r, pearson_p = stats.pearsonr(sub[var], sub["casos_dengue"])
        spearman_r, spearman_p = stats.spearmanr(sub[var], sub["casos_dengue"])

        resultados.append({
            "variable": var,
            "n": len(sub),
            "pearson_r": round(pearson_r, 3),
            "pearson_p_valor": round(pearson_p, 4),
            "significativo_pearson_95pct": pearson_p < 0.05,
            "spearman_r": round(spearman_r, 3),
            "spearman_p_valor": round(spearman_p, 4),
            "significativo_spearman_95pct": spearman_p < 0.05,
        })

    resultado_df = pd.DataFrame(resultados).sort_values("pearson_r", key=abs, ascending=False)
    resultado_df.to_csv(RUTA_SALIDA_CORR, index=False)

    print("\nResultados (ordenados por fuerza de correlación de Pearson):")
    print(resultado_df.to_string(index=False))

    print("\nInterpretación de referencia (Cohen, 1988):")
    print("  |r| < 0.10        -> prácticamente nula")
    print("  0.10 <= |r| < 0.30 -> débil")
    print("  0.30 <= |r| < 0.50 -> moderada")
    print("  |r| >= 0.50        -> fuerte")


def analizar_estacionalidad():
    print("\n" + "=" * 60)
    print("ANÁLISIS 2: ESTACIONALIDAD MENSUAL (2017-2021)")
    print("=" * 60)

    df = pd.read_csv(RUTA_DENGUE_RAW, low_memory=False)
    df = df.rename(columns={"year_": "anio"})
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df = df[(df["anio"] >= 2017) & (df["anio"] <= 2021)]

    # La fecha de inicio de síntomas es más representativa del momento
    # real de infección que la fecha de consulta administrativa
    df["ini_sin_"] = pd.to_datetime(df["ini_sin_"], errors="coerce")
    df["mes"] = df["ini_sin_"].dt.month
    df = df.dropna(subset=["mes"])

    # Promedio de casos por mes, dividido entre 5 años para tener el
    # promedio mensual real, no la suma acumulada
    casos_por_mes_anio = df.groupby(["anio", "mes"]).size().reset_index(name="casos")
    promedio_mensual = casos_por_mes_anio.groupby("mes")["casos"].mean().reset_index()
    promedio_mensual.columns = ["mes", "promedio_casos"]

    nombres_meses = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun",
                      7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
    promedio_mensual["mes_nombre"] = promedio_mensual["mes"].map(nombres_meses)

    promedio_mensual.to_csv(RUTA_SALIDA_ESTACIONAL, index=False)

    print("\nPromedio de casos por mes (2017-2021):")
    print(promedio_mensual[["mes_nombre", "promedio_casos"]].to_string(index=False))

    mes_max = promedio_mensual.loc[promedio_mensual["promedio_casos"].idxmax()]
    mes_min = promedio_mensual.loc[promedio_mensual["promedio_casos"].idxmin()]
    print(f"\nMes con más casos en promedio: {mes_max['mes_nombre']} ({mes_max['promedio_casos']:.1f} casos)")
    print(f"Mes con menos casos en promedio: {mes_min['mes_nombre']} ({mes_min['promedio_casos']:.1f} casos)")


if __name__ == "__main__":
    analizar_correlacion()
    analizar_estacionalidad()

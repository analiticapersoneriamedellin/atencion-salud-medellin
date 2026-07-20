"""
analisis_incidencia_iceberg.py
Construye el análisis central del proyecto reformulado:
1. Tasa de incidencia real de dengue por comuna y año (casos / población x 100.000)
2. Indicador "efecto punta del iceberg": proporción de casos graves/hospitalizados
   sobre el total de casos notificados, por año.

Objetivo: evaluar si la caida del 90% en casos notificados de dengue
(2017-2021) refleja una mejora real o un patron de subregistro creciente.

Uso:
    cd src
    python analisis_incidencia_iceberg.py

IMPORTANTE: este script asume que ya descargaste el dataset de
"Proyecciones de Población por comuna y corregimiento 2018-2030" (DANE /
Alcaldía de Medellín, vía MEData) y lo guardaste en:
    ../data/raw/poblacion_comunas_medellin.csv
Si el archivo tiene columnas con nombres distintos a los usados aquí,
ajusta el diccionario COLUMNAS_POBLACION más abajo.
"""

import pandas as pd

RUTA_DENGUE = "../data/raw/sivigila_dengue.csv"
RUTA_POBLACION = "../data/raw/poblacion_comunas_medellin.csv"
RUTA_SALIDA_INCIDENCIA = "../data/processed/dengue_tasa_incidencia.csv"
RUTA_SALIDA_ICEBERG = "../data/processed/dengue_efecto_iceberg.csv"

ANIO_INICIO = 2017
ANIO_FIN = 2021

# AJUSTAR según los nombres reales de columnas del archivo de población
# descargado (varían según el portal). Ejemplo típico esperado:
COLUMNAS_POBLACION = {
    "comuna": "comuna",       # nombre de la comuna/corregimiento
    "anio": "anio",           # año de la proyección
    "poblacion": "poblacion", # total de población (ambos sexos)
}


def normalizar_comuna(serie: pd.Series) -> pd.Series:
    """Misma normalización usada en consolidar_dengue_clima.py, para que
    los nombres de comuna coincidan entre ambos datasets al cruzar."""
    return serie.astype(str).str.strip().str.title()


# Diccionario de equivalencias entre los nombres de comuna del dataset de
# DENGUE (izquierda, ya normalizados con Title Case) y los nombres del
# dataset de POBLACIÓN (derecha, tal como aparecen en el archivo real).
# Confirmado manualmente comparando ambos datasets -- las diferencias son
# tildes faltantes/distintas y estructura de nombre distinta para
# corregimientos.
EQUIVALENCIAS_COMUNA = {
    "Belen": "Belén",
    "Corregimiento De San Cristobal": "San Cristóbal",
    "Corregimiento De Santa Elena": "Santa Elena",
    "La America": "La América",
    "Laureles": "Laureles Estadio",
    # NOTA: .title() capitaliza TODAS las palabras (incluida "de"/"la"),
    # por eso el lado derecho debe coincidir con esa capitalización, no
    # con la ortografía "natural" del nombre.
    "Doce De Octubre": "Doce De Octubre",  # ya coincide tras title(), sin cambio real necesario
    "San Sebastian De Palmitas": "San Sebastián De Palmitas",
}


def aplicar_equivalencias(serie: pd.Series) -> pd.Series:
    return serie.replace(EQUIVALENCIAS_COMUNA)


def cargar_dengue_por_comuna_anio() -> pd.DataFrame:
    print("[INFO] Cargando y agregando casos de dengue por comuna-año...")
    df = pd.read_csv(RUTA_DENGUE, low_memory=False)
    df = df.rename(columns={"year_": "anio"})
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df = df[(df["anio"] >= ANIO_INICIO) & (df["anio"] <= ANIO_FIN)]
    df["comuna"] = normalizar_comuna(df["comuna"])
    df.loc[df["comuna"].str.contains("Sin Informacion", case=False, na=False),
           "comuna"] = "Sin Informacion"

    casos = df.groupby(["comuna", "anio"]).size().reset_index(name="casos")
    casos["comuna"] = aplicar_equivalencias(casos["comuna"])
    return casos, df


def cargar_poblacion() -> pd.DataFrame:
    """El archivo real descargado viene en formato ANCHO: una fila por
    comuna, con columnas total_2018, total_2019, ..., total_2030 -- no en
    formato largo como se asumió inicialmente. Se transforma aquí."""
    print("[INFO] Cargando población por comuna (formato ancho)...")
    # El archivo descargado viene en codificación Latin-1 (típico de
    # exportaciones de Excel/GIS en Windows con acentos en español), no
    # UTF-8 -- se prueban ambas codificaciones por robustez.
    try:
        df = pd.read_csv(RUTA_POBLACION, encoding="utf-8")
    except UnicodeDecodeError:
        print("[INFO] UTF-8 falló, reintentando con codificación Latin-1...")
        df = pd.read_csv(RUTA_POBLACION, encoding="latin1")

    columnas_anio = [c for c in df.columns if c.startswith("total_")]
    df_largo = df.melt(
        id_vars=["nombre"],
        value_vars=columnas_anio,
        var_name="anio_col",
        value_name="poblacion",
    )
    df_largo["anio"] = df_largo["anio_col"].str.replace("total_", "").astype(int)
    df_largo["comuna"] = normalizar_comuna(df_largo["nombre"])
    df_largo["poblacion"] = pd.to_numeric(df_largo["poblacion"], errors="coerce")

    poblacion_total = df_largo.groupby(["comuna", "anio"])["poblacion"].sum().reset_index()
    return poblacion_total


def calcular_tasa_incidencia(casos: pd.DataFrame, poblacion: pd.DataFrame) -> pd.DataFrame:
    resultado = casos.merge(poblacion, on=["comuna", "anio"], how="left")

    # El dataset de población empieza en 2018 (no tiene 2017). Se usa la
    # población de 2018 como aproximación para 2017 -- supuesto razonable
    # dado que el cambio poblacional de un año a otro en una ciudad es
    # mínimo comparado con las variaciones de casos de dengue que se
    # analizan. Documentado explícitamente como limitación metodológica.
    poblacion_2018 = poblacion[poblacion["anio"] == 2018][["comuna", "poblacion"]]
    poblacion_2018 = poblacion_2018.rename(columns={"poblacion": "poblacion_2018_aprox"})
    resultado = resultado.merge(poblacion_2018, on="comuna", how="left")
    resultado["poblacion"] = resultado["poblacion"].fillna(resultado["poblacion_2018_aprox"])
    resultado = resultado.drop(columns=["poblacion_2018_aprox"])

    resultado["tasa_incidencia_100k"] = (
        resultado["casos"] / resultado["poblacion"] * 100_000
    )

    sin_poblacion = resultado["poblacion"].isnull().sum()
    if sin_poblacion > 0:
        print(f"[WARN] {sin_poblacion} filas sin dato de población "
              f"(revisar coincidencia de nombres de comuna entre datasets)")
        print(resultado[resultado["poblacion"].isnull()][["comuna", "anio"]].drop_duplicates())

    return resultado


def calcular_efecto_iceberg(df_dengue: pd.DataFrame) -> pd.DataFrame:
    """Proporción de casos graves/hospitalizados sobre el total, por año.
    Si esta proporción SUBE mientras el total de casos BAJA, es evidencia
    de que solo los casos que no se pueden ocultar (terminan en atención
    hospitalaria) siguen siendo captados -- patrón de subregistro."""
    df = df_dengue.copy()

    # pac_hos_ viene como texto (mezclado con valores "SD"), por eso se
    # compara contra el STRING "1", no el número 1 -- bug corregido tras
    # verificar que la comparación numérica siempre daba 0 (pac_hos_ se
    # carga como texto por la presencia de "SD" en la columna).
    # Codificación confirmada: 1 = hospitalizado, 2 = no hospitalizado.
    df["pac_hos_"] = df["pac_hos_"].astype(str).str.strip()
    df["hospitalizado"] = (df["pac_hos_"] == "1").astype(int)

    # Segundo indicador, independiente, para triangular: clas_dengue == "3"
    # (dengue grave, codificación estándar SIVIGILA: 1=sin signos de alarma,
    # 2=con signos de alarma, 3=grave). Mismo problema de tipo texto/"SD".
    df["clas_dengue"] = df["clas_dengue"].astype(str).str.strip()
    df["dengue_grave"] = (df["clas_dengue"] == "3").astype(int)

    resumen = df.groupby("anio").agg(
        total_casos=("id", "count"),
        casos_hospitalizados=("hospitalizado", "sum"),
        casos_graves=("dengue_grave", "sum"),
    ).reset_index()
    resumen["proporcion_hospitalizados"] = (
        resumen["casos_hospitalizados"] / resumen["total_casos"]
    )
    resumen["proporcion_graves"] = (
        resumen["casos_graves"] / resumen["total_casos"]
    )

    return resumen


def main():
    casos, df_dengue_completo = cargar_dengue_por_comuna_anio()

    try:
        poblacion = cargar_poblacion()
        incidencia = calcular_tasa_incidencia(casos, poblacion)
        incidencia.to_csv(RUTA_SALIDA_INCIDENCIA, index=False)
        print(f"[OK] Tasas de incidencia guardadas en {RUTA_SALIDA_INCIDENCIA}")
        print("\nTasa de incidencia promedio por año (todas las comunas):")
        print(incidencia.groupby("anio")["tasa_incidencia_100k"].mean())
    except FileNotFoundError:
        print(f"[WARN] No se encontró {RUTA_POBLACION}. "
              f"Descarga el dataset de población por comuna y vuelve a correr "
              f"este script para calcular tasas de incidencia. "
              f"Continuando solo con el análisis de efecto iceberg...")

    iceberg = calcular_efecto_iceberg(df_dengue_completo)
    iceberg.to_csv(RUTA_SALIDA_ICEBERG, index=False)
    print(f"\n[OK] Efecto iceberg guardado en {RUTA_SALIDA_ICEBERG}")
    print("\n=== Efecto iceberg por año ===")
    print(iceberg)
    print("\nInterpretación: si 'proporcion_hospitalizados' SUBE mientras")
    print("'total_casos' BAJA, es evidencia de subregistro (solo los casos")
    print("graves siguen siendo captados por el sistema).")


if __name__ == "__main__":
    main()

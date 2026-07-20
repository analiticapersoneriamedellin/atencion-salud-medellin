"""
consolidar_dengue_clima.py
Consolida los casos de dengue (SIVIGILA, Medellín) con el histórico climático
del IDEAM (temperatura + precipitación), agregando por semana epidemiológica
y comuna, y construyendo variables de rezago (lags) para el modelo predictivo.

VENTANA DE ANÁLISIS: 2017-2021 (5 años).
Justificación: aunque el dataset de dengue cubre 2008-2021 y la temperatura
tiene histórico desde 2005, la precipitación en las estaciones de Medellín
solo tiene cobertura real y consistente desde 2017 (ver docs/marco_metodologico.md
para el detalle completo de esta limitación, confirmada empíricamente).

Uso:
    cd src
    python consolidar_dengue_clima.py
"""

import pandas as pd
import numpy as np

RUTA_DENGUE = "../data/raw/sivigila_dengue.csv"
RUTA_TEMP = "../data/raw/ideam_temperatura_medellin_semanal.csv"
RUTA_PRECIP = "../data/raw/ideam_precipitacion_medellin_semanal.csv"
RUTA_SALIDA = "../data/processed/dengue_clima_consolidado.csv"

ANIO_INICIO = 2017
ANIO_FIN = 2021

# Rezagos a construir, en semanas. Basado en la biología del ciclo del
# mosquito Aedes aegypti: la precipitación necesita tiempo para generar
# criaderos (estancamiento de agua), y el virus necesita un período de
# incubación extrínseco en el mosquito sensible a la temperatura.
LAGS_SEMANAS = [2, 4]


def cargar_dengue() -> pd.DataFrame:
    print("[INFO] Cargando casos de dengue...")
    df = pd.read_csv(RUTA_DENGUE, low_memory=False)

    # Las columnas year_ y semana ya vienen listas en el dataset original
    df = df.rename(columns={"year_": "anio"})
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df["semana"] = pd.to_numeric(df["semana"], errors="coerce")

    df = df[(df["anio"] >= ANIO_INICIO) & (df["anio"] <= ANIO_FIN)]

    # NORMALIZACIÓN DE COMUNA: el dataset crudo tiene la misma comuna
    # escrita con distintas combinaciones de mayúsculas/minúsculas
    # (ej. "Doce de Octubre" vs "Doce De Octubre", "SIN INFORMACION" vs
    # "Sin informacion" vs "Sin Informacion"), lo que las trataría como
    # categorías separadas y distorsionaría el conteo real por comuna.
    # Se normaliza a Title Case y se consolida "sin información" en una
    # sola categoría estándar.
    df["comuna"] = df["comuna"].astype(str).str.strip().str.title()
    df.loc[df["comuna"].str.contains("Sin Informacion", case=False, na=False),
           "comuna"] = "Sin Informacion"

    print(f"[OK] Dengue filtrado a {ANIO_INICIO}-{ANIO_FIN}: {len(df)} casos")
    print(f"[OK] Comunas únicas tras normalizar: {df['comuna'].nunique()}")
    return df


def agregar_casos_por_semana_comuna(df_dengue: pd.DataFrame) -> pd.DataFrame:
    """Cuenta casos de dengue por año-semana-comuna (nivel de agregación
    del modelo: no se predice caso por caso, se predice volumen esperado
    por comuna y semana)."""
    agregado = (
        df_dengue.groupby(["anio", "semana", "comuna"])
        .size()
        .reset_index(name="casos_dengue")
    )
    print(f"[OK] Agregado a nivel semana-comuna: {len(agregado)} filas "
          f"({agregado['comuna'].nunique()} comunas distintas)")
    return agregado


def cargar_clima() -> pd.DataFrame:
    print("[INFO] Cargando clima semanal...")
    df_temp = pd.read_csv(RUTA_TEMP)
    df_precip = pd.read_csv(RUTA_PRECIP)

    # El clima es a nivel de CIUDAD (estaciones puntuales), no por comuna.
    # Se promedia entre estaciones si hay más de una reportando la misma semana.
    temp_semanal = (
        df_temp.groupby(["anio", "semana"])["temperatura_promedio"]
        .mean()
        .reset_index()
    )
    precip_semanal = (
        df_precip.groupby(["anio", "semana"])["precipitacion_acumulada"]
        .sum()
        .reset_index()
    )

    clima = temp_semanal.merge(precip_semanal, on=["anio", "semana"], how="outer")
    clima = clima[(clima["anio"] >= ANIO_INICIO) & (clima["anio"] <= ANIO_FIN)]
    clima = clima.sort_values(["anio", "semana"]).reset_index(drop=True)

    print(f"[OK] Clima consolidado {ANIO_INICIO}-{ANIO_FIN}: {len(clima)} semanas")
    return clima


def construir_lags(clima: pd.DataFrame) -> pd.DataFrame:
    """Agrega columnas de temperatura y precipitación rezagadas N semanas.
    IMPORTANTE: el shift se hace sobre la serie ORDENADA cronológicamente,
    asumiendo continuidad semana a semana -- si hay semanas faltantes en el
    clima, el lag podría no corresponder exactamente a "N semanas atrás en
    tiempo real" sino a "N filas atrás". Se documenta como limitación."""
    clima = clima.sort_values(["anio", "semana"]).reset_index(drop=True)

    for lag in LAGS_SEMANAS:
        clima[f"temperatura_lag{lag}"] = clima["temperatura_promedio"].shift(lag)
        clima[f"precipitacion_lag{lag}"] = clima["precipitacion_acumulada"].shift(lag)

    return clima


def main():
    df_dengue = cargar_dengue()
    casos = agregar_casos_por_semana_comuna(df_dengue)

    clima = cargar_clima()
    clima = construir_lags(clima)

    # Unir: cada comuna, en cada semana, recibe el mismo dato climático
    # de ciudad (limitación metodológica documentada -- ver marco_metodologico.md)
    consolidado = casos.merge(clima, on=["anio", "semana"], how="left")

    # Variable objetivo para predicción a 1 semana: casos de la semana siguiente
    consolidado = consolidado.sort_values(["comuna", "anio", "semana"])
    consolidado["casos_dengue_semana_siguiente"] = (
        consolidado.groupby("comuna")["casos_dengue"].shift(-1)
    )

    consolidado.to_csv(RUTA_SALIDA, index=False)

    print("\n" + "=" * 60)
    print(f"[OK] Consolidado final guardado en {RUTA_SALIDA}")
    print(f"     Total filas: {len(consolidado)}")
    print(f"     Comunas: {consolidado['comuna'].nunique()}")
    print(f"     Rango: {ANIO_INICIO}-{ANIO_FIN}")
    print(f"     Columnas: {list(consolidado.columns)}")
    print("=" * 60)

    # Verificación rápida de valores nulos en las variables clave del modelo
    columnas_modelo = ["casos_dengue", "temperatura_promedio", "precipitacion_acumulada",
                        "temperatura_lag2", "precipitacion_lag2",
                        "temperatura_lag4", "precipitacion_lag4",
                        "casos_dengue_semana_siguiente"]
    print("\nValores nulos por columna (revisar antes de modelar):")
    print(consolidado[columnas_modelo].isnull().sum())


if __name__ == "__main__":
    main()

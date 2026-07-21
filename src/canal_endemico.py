"""
canal_endemico.py
Construye el "canal endémico" de dengue para Medellín, siguiendo el método
de Marcelo Bortman (el mismo que usa oficialmente el INS colombiano para
vigilancia epidemiológica): banda de comportamiento histórico esperado por
semana epidemiológica, calculada como media +/- desviaciones estándar sobre
los valores transformados logarítmicamente (para normalizar la asimetría
típica de los conteos de enfermedades).

Zonas resultantes:
  - Éxito:    por debajo del límite inferior (mejor de lo esperado)
  - Seguridad: entre el límite inferior y la media (dentro de lo normal-bajo)
  - Alerta:    entre la media y el límite superior (normal-alto, vigilar)
  - Epidemia:  por encima del límite superior (brote)

LIMITACIÓN RECONOCIDA: el método de Bortman fue diseñado para usarse con
series históricas largas (10+ años). Aquí se dispone de solo 5 años
(2017-2021), lo que hace que la banda de confianza sea más ancha e
inestable de lo ideal. Se documenta como limitación, no se oculta.

Uso:
    cd src
    python canal_endemico.py
"""

import numpy as np
import pandas as pd

RUTA_DENGUE = "../data/raw/sivigila_dengue.csv"
RUTA_SALIDA = "../data/processed/canal_endemico.csv"

ANIO_INICIO = 2017
ANIO_FIN = 2021
ANIO_A_EVALUAR = 2021  # el año que se compara contra el canal histórico


def cargar_casos_semanales() -> pd.DataFrame:
    print("[INFO] Cargando casos de dengue...")
    df = pd.read_csv(RUTA_DENGUE, low_memory=False)
    df = df.rename(columns={"year_": "anio"})
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df["semana"] = pd.to_numeric(df["semana"], errors="coerce")
    df = df[(df["anio"] >= ANIO_INICIO) & (df["anio"] <= ANIO_FIN)]

    casos = df.groupby(["anio", "semana"]).size().reset_index(name="casos")

    # Asegurar que existan las 52 semanas para cada año, con 0 donde no hay
    # casos (importante: la ausencia de un caso es informativa, no un hueco)
    todas_semanas = pd.DataFrame(
        [(a, s) for a in range(ANIO_INICIO, ANIO_FIN + 1) for s in range(1, 53)],
        columns=["anio", "semana"]
    )
    casos = todas_semanas.merge(casos, on=["anio", "semana"], how="left")
    casos["casos"] = casos["casos"].fillna(0)

    return casos


def construir_canal_endemico(casos: pd.DataFrame, anio_evaluar: int) -> pd.DataFrame:
    """Calcula el canal histórico usando todos los años EXCEPTO el que se
    va a evaluar (para no comparar el año contra sí mismo)."""
    historico = casos[casos["anio"] != anio_evaluar].copy()

    # Transformación logarítmica (log(x+1) para manejar ceros), estándar
    # en el método de Bortman para normalizar la distribución
    historico["log_casos"] = np.log1p(historico["casos"])

    resumen = historico.groupby("semana")["log_casos"].agg(["mean", "std"]).reset_index()
    resumen["std"] = resumen["std"].fillna(0)  # semanas con poca variación histórica

    # Banda de confianza: media +/- 1.5 desviaciones estándar
    # (se usa 1.5 en vez del 2.0 clásico porque con solo 4 años de
    # histórico, 2 SD generaría bandas excesivamente anchas y poco útiles;
    # esta es una adaptación documentada, no el estándar original)
    resumen["limite_inferior_log"] = resumen["mean"] - 1.5 * resumen["std"]
    resumen["limite_superior_log"] = resumen["mean"] + 1.5 * resumen["std"]

    # Revertir la transformación logarítmica para volver a la escala de casos
    resumen["canal_medio"] = np.expm1(resumen["mean"])
    resumen["canal_inferior"] = np.expm1(resumen["limite_inferior_log"]).clip(lower=0)
    resumen["canal_superior"] = np.expm1(resumen["limite_superior_log"])

    return resumen[["semana", "canal_inferior", "canal_medio", "canal_superior"]]


def clasificar_zona(valor: float, inf: float, medio: float, sup: float) -> str:
    if valor < inf:
        return "Éxito"
    elif valor < medio:
        return "Seguridad"
    elif valor <= sup:
        return "Alerta"
    else:
        return "Epidemia"


def main():
    casos = cargar_casos_semanales()
    canal = construir_canal_endemico(casos, ANIO_A_EVALUAR)

    año_actual = casos[casos["anio"] == ANIO_A_EVALUAR][["semana", "casos"]]
    comparacion = año_actual.merge(canal, on="semana", how="left")

    comparacion["zona"] = comparacion.apply(
        lambda r: clasificar_zona(r["casos"], r["canal_inferior"], r["canal_medio"], r["canal_superior"]),
        axis=1
    )

    comparacion.to_csv(RUTA_SALIDA, index=False)

    print(f"\n[OK] Canal endémico guardado en {RUTA_SALIDA}")
    print(f"\n=== Clasificación de zonas para {ANIO_A_EVALUAR} ===")
    print(comparacion["zona"].value_counts())

    print(f"\n=== Semanas en zona de Epidemia o Alerta ({ANIO_A_EVALUAR}) ===")
    alerta = comparacion[comparacion["zona"].isin(["Epidemia", "Alerta"])]
    print(alerta[["semana", "casos", "canal_medio", "canal_superior", "zona"]])

    print("\nNOTA: con solo 4 años de histórico para construir el canal (2017-2020),")
    print("la banda de confianza es más ancha e inestable que con series largas (10+ años).")
    print("Se usó 1.5 desviaciones estándar en vez de 2.0 para compensar parcialmente,")
    print("documentado como adaptación metodológica explícita.")


if __name__ == "__main__":
    main()

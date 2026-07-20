"""
ingest_clima.py
Descarga el histórico REAL (no en tiempo real) de temperatura y precipitación
del IDEAM para Medellín, vía la API Socrata de datos.gov.co.

IMPORTANTE - lección aprendida durante la investigación de este proyecto:
Existen DOS tipos de datasets de estaciones del IDEAM en datos.gov.co:
  - "Datos de Estaciones de IDEAM y de Terceros" (resource_id 57sv-p2fu):
    SOLO tiempo real / observaciones recientes. NO sirve para históricos.
  - "Datos Hidrometeorológicos Crudos - Red de Estaciones" (temperatura:
    sbwg-7ju4, precipitación: s54a-sgyg): HISTÓRICO REAL, confirmado con
    datos desde 2005 hasta la fecha actual para la estación de Medellín.
Este script usa exclusivamente los datasets históricos correctos.

Uso:
    python ingest_clima.py
"""

import os
import time
import requests
import pandas as pd

BASE_URL = "https://www.datos.gov.co/resource/{resource_id}.json"
LIMIT_PER_REQUEST = 5000  # páginas más pequeñas = menos probabilidad de timeout
TIMEOUT_SEGUNDOS = 120
MAX_REINTENTOS = 3

# Confirmados manualmente durante la investigación de este proyecto:
DATASETS_CLIMA = {
    "temperatura": "sbwg-7ju4",
    "precipitacion": "s54a-sgyg",
}

MUNICIPIO_FILTRO = "MEDELLÍN"  # confirmado: así viene en mayúsculas con tilde
RUTA_SALIDA = "../data/raw"


def descargar_clima(variable: str, resource_id: str,
                     anio_inicio: int = 2005, anio_fin: int = 2026) -> pd.DataFrame | None:
    """Descarga el histórico completo de una variable climática para Medellín,
    AÑO POR AÑO (no con un solo offset gigante creciente).

    Lección aprendida: paginar con $offset que crece sin límite se vuelve
    cada vez más lento en el servidor (tiene que saltarse todas las filas
    anteriores en cada solicitud), causando timeouts en offsets altos
    (se observó falla consistente pasados los 700.000-800.000). Al filtrar
    por año con $where, cada año reinicia el offset en 0, evitando el
    problema por completo."""
    url = BASE_URL.format(resource_id=resource_id)
    todos_los_registros = []

    print(f"[INFO] Descargando histórico de '{variable}' para Medellín, año por año...")
    for anio in range(anio_inicio, anio_fin + 1):
        offset = 0
        filas_del_anio = 0
        while True:
            params = {
                "$limit": LIMIT_PER_REQUEST,
                "$offset": offset,
                "municipio": MUNICIPIO_FILTRO,
                "$where": f"fechaobservacion between '{anio}-01-01T00:00:00' "
                          f"and '{anio}-12-31T23:59:59'",
            }

            batch = None
            for intento in range(1, MAX_REINTENTOS + 1):
                try:
                    resp = requests.get(url, params=params, timeout=TIMEOUT_SEGUNDOS)
                    resp.raise_for_status()
                    batch = resp.json()
                    break
                except requests.RequestException as e:
                    print(f"[WARN] {anio} intento {intento}/{MAX_REINTENTOS} "
                          f"fallo en offset {offset}: {e}")
                    if intento < MAX_REINTENTOS:
                        time.sleep(3 * intento)
                    else:
                        print(f"[ERROR] {anio}: se agotaron los reintentos en offset {offset}.")

            if batch is None or not batch:
                break

            todos_los_registros.extend(batch)
            filas_del_anio += len(batch)
            offset += LIMIT_PER_REQUEST

            if len(batch) < LIMIT_PER_REQUEST:
                break
            time.sleep(0.3)

        print(f"       [{anio}] {filas_del_anio} filas")

    if not todos_los_registros:
        print(f"[WARN] '{variable}' devolvió 0 registros para Medellín.")
        return None

    df = pd.DataFrame(todos_los_registros)
    df["fechaobservacion"] = pd.to_datetime(df["fechaobservacion"])
    df = df.sort_values("fechaobservacion").reset_index(drop=True)

    print(f"[OK] '{variable}': {len(df)} filas totales, "
          f"desde {df['fechaobservacion'].min()} hasta {df['fechaobservacion'].max()}")

    return df


def agregar_a_semanal(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """Agrega las observaciones horarias/sub-horarias a nivel de semana
    epidemiológica, para poder cruzar con el dataset de dengue (que es
    semanal). Temperatura -> promedio semanal. Precipitación -> suma semanal."""
    df = df.copy()
    df["valorobservado"] = pd.to_numeric(df["valorobservado"], errors="coerce")
    df["anio"] = df["fechaobservacion"].dt.isocalendar().year
    df["semana"] = df["fechaobservacion"].dt.isocalendar().week

    if variable == "temperatura":
        agregado = df.groupby(["anio", "semana", "nombreestacion"])["valorobservado"].mean().reset_index()
        agregado = agregado.rename(columns={"valorobservado": "temperatura_promedio"})
    else:  # precipitacion
        agregado = df.groupby(["anio", "semana", "nombreestacion"])["valorobservado"].sum().reset_index()
        agregado = agregado.rename(columns={"valorobservado": "precipitacion_acumulada"})

    return agregado


def main():
    os.makedirs(RUTA_SALIDA, exist_ok=True)

    for variable, resource_id in DATASETS_CLIMA.items():
        df_crudo = descargar_clima(variable, resource_id)
        if df_crudo is None:
            continue

        # Guardar crudo (para trazabilidad, tal como se descargó)
        ruta_crudo = os.path.join(RUTA_SALIDA, f"ideam_{variable}_medellin_crudo.csv")
        df_crudo.to_csv(ruta_crudo, index=False)
        print(f"[OK] Crudo guardado en {ruta_crudo}")

        # Guardar agregado semanal (listo para cruzar con dengue)
        df_semanal = agregar_a_semanal(df_crudo, variable)
        ruta_semanal = os.path.join(RUTA_SALIDA, f"ideam_{variable}_medellin_semanal.csv")
        df_semanal.to_csv(ruta_semanal, index=False)
        print(f"[OK] Agregado semanal guardado en {ruta_semanal} ({len(df_semanal)} filas)")


if __name__ == "__main__":
    main()
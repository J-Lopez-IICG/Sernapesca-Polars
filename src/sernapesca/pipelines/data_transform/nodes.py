import polars as pl
import unicodedata
import re

def clean_column_name(name: str) -> str:
    name = unicodedata.normalize('NFKD', str(name)).encode('ASCII', 'ignore').decode('ASCII')
    name = name.lower().strip().replace(" ", "_").replace(".", "_").replace(";", "_")
    name = re.sub(r'[^a-z0-9_]', '', name)
    return name

def clean_data_polars(df: pl.DataFrame, **kwargs) -> pl.DataFrame:
    # 1. Limpiar nombres de columnas
    new_cols = {c: clean_column_name(c) for c in df.columns}
    df = df.rename(new_cols)

    # 2. Quitar espacios
    df = df.with_columns(pl.col(pl.Utf8).str.strip_chars())

    # 3. Forzar año
    if "ano" in df.columns:
        df = df.with_columns(pl.col("ano").cast(pl.Int64, strict=False))

    # 4. Homologar región
    if "region" in df.columns:
        df = df.with_columns(
            pl.col("region").cast(pl.Utf8).str.replace(r"\.0$", "")
        )

        # Buscamos el mapa de regiones dentro de kwargs
        mapa_regiones = kwargs.get("mapa_regiones")

        if mapa_regiones is not None:
            df = df.with_columns(
                pl.col("region").replace(mapa_regiones, default=pl.col("region"))
            )

        df = df.with_columns(pl.col("region").cast(pl.Int64, strict=False))

    # 5. Duplicados
    df = df.unique()

    print(f"--- ÉXITO: Polars procesó {df.height} filas ---")
    return df
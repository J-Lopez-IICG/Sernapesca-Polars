import polars as pl

def create_master_table(
    df_plantas: pl.DataFrame,
    df_desembarque: pl.DataFrame,
    df_materia: pl.DataFrame # Asumimos que esta ya viene unida o la usamos para el contexto
) -> pl.DataFrame:

    print("--- Capa Gold: Iniciando procesamiento---")

    # 1. Agregación externa (Sigue siendo necesaria porque viene de OTRA tabla)
    df_des_resumen = (
        df_desembarque
        .group_by(["ano", "region"])
        .agg([
            pl.col("toneladas").sum().alias("total_toneladas_desembarque_region"),
            pl.len().alias("n_operaciones_puerto_region")
        ])
    )

    # 2. Refactorización: Unimos y calculamos en un solo flujo
    df_gold = (
        df_plantas
        # Unimos solo lo que es externo (Desembarques)
        .join(df_des_resumen, on=["ano", "region"], how="left")

        # Limpiamos nulos en columnas numéricas para evitar errores en el cálculo
        .with_columns(
            pl.col(pl.Float64, pl.Int64).fill_null(0)
        )

        # EL PODER DE OVER:
        # Creamos la columna de "Total Regional" sin hacer un segundo Join
        .with_columns([
            pl.col("produccion")
              .sum()
              .over(["ano", "region", "materia_prima"])
              .alias("produccion_total_especie_region")
        ])

        # Ahora que tenemos el total al lado de cada fila, calculamos el %
        .with_columns(
            (pl.col("produccion") / pl.col("produccion_total_especie_region") * 100)
            .fill_nan(0)
            .alias("pct_participacion_planta")
        )
    )

    print(f"--- ÉXITO: Tabla Gold generada: {df_gold.shape} ---")
    return df_gold
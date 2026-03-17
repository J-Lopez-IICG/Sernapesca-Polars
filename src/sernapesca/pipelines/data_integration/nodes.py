import polars as pl

def create_master_table(
    df_plantas: pl.DataFrame,
    df_desembarque: pl.DataFrame,
    df_materia: pl.DataFrame
) -> pl.DataFrame:
    """
    Cruza las tres tablas limpias para crear la base maestra Gold.
    """
    print("--- INFO: Iniciando el cruce (JOIN) de tablas en Polars ---")

    # 1. Cruzar Plantas con Desembarque
    # Ajusta las columnas llaves según tu conocimiento del negocio
    df_master = df_plantas.join(
        df_desembarque,
        on=["ano", "region"], # Asumimos que coinciden en año y región
        how="left"
    )

    # 2. Cruzar el resultado con Materia Prima
    df_master = df_master.join(
        df_materia,
        left_on=["materia_prima"], # Columna en la tabla maestra (vende de Plantas)
        right_on=["materia_prima"], # Columna en df_materia
        how="left"
    )

    # 3. Limpieza final (Opcional, por si los joins generaron columnas duplicadas)
    # En Polars, si hay nombres duplicados, les añade "_right" por defecto.

    print(f"--- ÉXITO: Tabla Maestra creada con {df_master.height} filas y {df_master.width} columnas ---")

    return df_master
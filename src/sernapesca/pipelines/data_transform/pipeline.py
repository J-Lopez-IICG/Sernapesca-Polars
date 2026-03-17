from kedro.pipeline import Pipeline, node, pipeline
from .nodes import clean_data_polars

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=clean_data_polars,
                inputs="bd_plantas_raw",
                outputs="bd_plantas_silver",
                name="clean_plantas_node",
            ),
            node(
                func=clean_data_polars,
                inputs="bd_materia_prima_raw",
                outputs="bd_materia_prima_silver",
                name="clean_materia_prima_node",
            ),
            node(
                func=clean_data_polars,
                inputs={
                    "df": "bd_desembarque_raw",
                    "mapa_regiones": "params:mapa_regiones"
                },
                outputs="bd_desembarque_silver",
                name="clean_desembarque_node",
            ),
        ]
    )
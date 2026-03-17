from kedro.pipeline import Pipeline, node, pipeline
from .nodes import create_master_table

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=create_master_table,
                inputs=[
                    "bd_plantas_silver",      # Creado por el pipeline anterior
                    "bd_desembarque_silver",  # Creado por el pipeline anterior
                    "bd_materia_prima_silver" # Creado por el pipeline anterior
                ],
                outputs="master_table_gold",  # El destino final en el catálogo
                name="join_master_table_node",
            ),
        ]
    )
"""Project pipelines."""
from typing import Dict
from kedro.pipeline import Pipeline

# Importamos los dos pipelines que creaste
from sernapesca.pipelines import data_transform as dt
from sernapesca.pipelines import data_integration as di

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    # Instanciamos los pipelines
    data_transform_pipeline = dt.create_pipeline()
    data_integration_pipeline = di.create_pipeline()

    return {
        # Si corres "kedro run", suma los dos y los corre en orden
        "__default__": data_transform_pipeline + data_integration_pipeline,

        # Si corres "kedro run --pipeline=data_transform"
        "data_transform": data_transform_pipeline,

        # Si corres "kedro run --pipeline=data_integration"
        "data_integration": data_integration_pipeline,
    }
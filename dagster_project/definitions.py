# from dagster_project.jobs import gsheets_financial_with_dbt_job
# from dagster_project.assets import openmeteo_asset, dbt_meteo_data
# from dagster_project.jobs import open_meteo_job
# from dagster_project.jobs import geo_data_job
# from dagster_project.assets import get_geo_data, dbt_geo_data
from dagster_project.jobs import beverage_dim_job
from dagster_project.assets import (
    ingredients_table,
    alcoholic_table,
    beverages_table,
    glass_table,
    beverage_fact_data,
    dbt_beverage_data,
)
from dagster_project.sensors import dbt_sensor
from dagster_project.schedules import schedules

# from dagster_project.assets import gsheet_finance_data, dbt_models
from dotenv import load_dotenv
import os
from dagster_duckdb_pandas import DuckDBPandasIOManager

from dagster import Definitions, DagsterInstance
from dagster_dbt import DbtCliResource
from path_config import DBT_DIR

MotherDuck = os.getenv("MD")
if not MotherDuck:
    raise ValueError(
        "Environment variable 'MD' is not set. Set it to your MotherDuck connection string (e.g., md:?token=...)."
    )
# definitions.py

# Import Rick and Morty assets and jobs (active)
# from dagster_project.assets import rick_and_morty_asset, dbt_rick_and_morty_data
# from dagster_project.jobs import RickandMorty_job

# Uncomment and import other assets/jobs as needed:

# from dagster_project.assets import camon_dbt_assets

# from dagster_project.jobs import meals_dim_job

# Youtube
# from dagster_project.assets.youtube import youtube_pipeline
# from dagster_project.jobs import Youtube_Job


# Define the assets
all_assets = [
    ingredients_table,
    alcoholic_table,
    beverages_table,
    glass_table,
    beverage_fact_data,
    dbt_beverage_data,
]

# Register the job, sensor, and schedule in the Definitions
defs = Definitions(
    assets=all_assets,
    # Register only the airline job
    jobs=[beverage_dim_job],
    schedules=[schedules]  # ,
    # sensors=[camon_sensor]
    ,
    resources={
        # "io_manager": DuckDBPandasIOManager(database=MotherDuck),
        "dbt": DbtCliResource(project_dir=DBT_DIR, profiles_dir=DBT_DIR),
    },
)

# Execute the job immediately
if __name__ == "__main__":
    try:
        instance = DagsterInstance.get()
        job = defs.get_job_def("beverage_dim_job")
        result = job.execute_in_process(
            instance=instance,
            resources={
                "io_manager": DuckDBPandasIOManager(database=MotherDuck),
                "dbt": DbtCliResource(project_dir=DBT_DIR, profiles_dir=DBT_DIR),
            },
        )
        print("beverage_dim_job Job finished:", result)
    except Exception as e:
        print(f"Error executing job: {e}")

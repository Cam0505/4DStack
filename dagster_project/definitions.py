
from dagster_project.assets import openmeteo_asset, dbt_weather_models
from dagster_project.assets.dbt_assets import dbt_models, dbt_common_models
from dagster_project.jobs import open_meteo_job
from dagster_project.jobs import geo_data_job
from dagster_project.assets import get_geo_data, dbt_geo_models
from dagster_project.jobs import RickandMorty_job
from dagster_project.assets import rick_and_morty_asset, dbt_rick_and_morty_models
from dagster_project.sensors import dbt_sensor
from dagster_project.schedules import schedules

from dotenv import load_dotenv
import os
from dagster_duckdb_pandas import DuckDBPandasIOManager

from dagster import Definitions, DagsterInstance, mem_io_manager
from dagster_dbt import DbtCliResource
from path_config import DBT_DIR

MotherDuck = os.getenv("MD")
if not MotherDuck:
    raise ValueError(
        "Environment variable 'MD' is not set. Set it to your MotherDuck connection string (e.g., md:?token=...)."
    )

# Define the assets - include pipeline assets and their specific dbt models
all_assets = [
    # Raw data pipeline assets
    rick_and_morty_asset,
    get_geo_data,
    openmeteo_asset,
    # Specific dbt model assets for each pipeline
    dbt_rick_and_morty_models,
    dbt_geo_models,
    dbt_weather_models,
    # Common dbt models (like dim_date) that don't depend on source data
    dbt_common_models,
    # Global dbt asset (for any remaining models)
    # dbt_models,
]

# Register the job, sensor, and schedule in the Definitions
defs = Definitions(
    assets=all_assets,
    # Register only the airline job
    jobs=[RickandMorty_job, geo_data_job, open_meteo_job],
    schedules=[schedules]  # ,
    # sensors=[camon_sensor]
    ,
    resources={
        "io_manager": DuckDBPandasIOManager(database=MotherDuck),
        "mem_io_manager": mem_io_manager,
        "dbt": DbtCliResource(project_dir=DBT_DIR, profiles_dir=DBT_DIR),
    },
)

# Execute multiple jobs immediately
if __name__ == "__main__":
    try:
        instance = DagsterInstance.get()

        # Define shared resources
        shared_resources = {
            "io_manager": DuckDBPandasIOManager(database=MotherDuck),
            "mem_io_manager": mem_io_manager,
            "dbt": DbtCliResource(project_dir=DBT_DIR, profiles_dir=DBT_DIR),
        }

        # List of jobs to run
        # Add more job names here
        jobs_to_run = ["RickandMorty_job", "geo_data_job", "open_meteo_job"]

        for job_name in jobs_to_run:
            print(f"\n🚀 Starting {job_name}...")
            try:
                job = defs.get_job_def(job_name)
                result = job.execute_in_process(
                    instance=instance,
                    resources=shared_resources,
                )
                print(f"✅ {job_name} finished successfully: {result.success}")
            except Exception as e:
                print(f"❌ Error executing {job_name}: {e}")
                # Continue with next job instead of stopping
                continue

    except Exception as e:
        print(f"💥 Fatal error: {e}")

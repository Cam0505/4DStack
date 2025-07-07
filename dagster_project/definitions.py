
from dagster_project.assets import openmeteo_asset, dbt_meteo_data
from dagster_project.jobs import open_meteo_job
from dagster_project.jobs import geo_data_job
from dagster_project.assets import get_geo_data, dbt_geo_data
from dagster_project.jobs import RickandMorty_job
from dagster_project.assets import rick_and_morty_asset, dbt_rick_and_morty_data
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
# definitions.py

# Import Rick and Morty assets and jobs (active)


# Define the assets
all_assets = [
    rick_and_morty_asset, dbt_rick_and_morty_data,
    get_geo_data, dbt_geo_data, openmeteo_asset, dbt_meteo_data
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

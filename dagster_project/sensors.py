from dagster import RunRequest, SensorDefinition
<<<<<<<< HEAD:dagster_project/sensors.py
from dagster_project.jobs.dbt_job import run_dbt_assets
========
from dagster_cam.jobs.dbt_job import run_dbt_assets
>>>>>>>> 8ba1a8d (Rename of dagster section, shorter name, adding path config):dagster_cam/sensors.py

dbt_sensor = SensorDefinition(
    name="dbt_sensor",
    evaluation_fn=lambda _: [RunRequest(run_key=None, job=run_dbt_assets)],
    minimum_interval_seconds=60 * 5,
)

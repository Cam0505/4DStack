from dagster import RunRequest, SensorDefinition
from dagster_project.jobs.dbt_job import run_dbt_assets

dbt_sensor = SensorDefinition(
    name="dbt_sensor",
    evaluation_fn=lambda _: [RunRequest(run_key=None, job=run_dbt_assets)],
    minimum_interval_seconds=60 * 5,
)

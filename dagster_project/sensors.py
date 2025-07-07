from dagster import RunRequest, SensorDefinition
from dagster_project.jobs.dbt_job import dbt_job

dbt_sensor = SensorDefinition(
    name="dbt_sensor",
    evaluation_fn=lambda _: [RunRequest(run_key=None, job=dbt_job)],
    minimum_interval_seconds=60 * 5,
)

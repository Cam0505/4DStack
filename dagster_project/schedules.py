"""
To add a daily schedule that materializes your dbt assets, uncomment the following lines.
"""

from dagster import ScheduleDefinition
from dagster_project.jobs.dbt_job import dbt_job
from dagster_project.jobs.beverage_data_job import beverage_dim_job


schedules = ScheduleDefinition(
    job=dbt_job,
    cron_schedule="0 6 * * *",  # Daily at 6 AM
)

# At 10:00 on Monday.
Weekly_BEVERAGE_SCHEDULE = ScheduleDefinition(
    job=beverage_dim_job, cron_schedule="0 10 * * MON"
)

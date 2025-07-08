from dagster import job, define_asset_job
from dagster_project.assets.dbt_assets import dbt_models


dbt_job = define_asset_job(
    name="dbt_job",
    # Dagster auto-infers dependency on `geo_data`
    selection=[dbt_models]
)

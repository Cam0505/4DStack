from dagster import job, define_asset_job
from dagster_project.assets.dbt_assets import dbt_4DStack


dbt_job = define_asset_job(
    name="dbt_4DStack",
    # Dagster auto-infers dependency on `geo_data`
    selection=[dbt_4DStack]
)

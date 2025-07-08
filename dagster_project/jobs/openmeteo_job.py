from dagster import job, define_asset_job, AssetSelection
from dagster_project.assets.open_meteo import openmeteo_asset, dbt_weather_models


open_meteo_job = define_asset_job(
    name="open_meteo_job",
    # Select both the openmeteo asset and the dbt weather models asset
    selection=AssetSelection.assets(openmeteo_asset, dbt_weather_models)
)

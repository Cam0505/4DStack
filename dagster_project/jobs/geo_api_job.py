from dagster import job, define_asset_job, AssetSelection
from dagster_project.assets.GeoAPI import get_geo_data, dbt_geo_models


geo_data_job = define_asset_job(
    name="geo_data_job",
    # Select both the raw geo data asset and the dbt geo models asset
    selection=AssetSelection.assets(get_geo_data, dbt_geo_models)
)

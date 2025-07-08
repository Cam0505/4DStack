from dagster import job, define_asset_job, AssetSelection
from dagster_project.assets.rick_and_morty import rick_and_morty_asset, dbt_rick_and_morty_models


RickandMorty_job = define_asset_job(
    name="RickandMorty_job",
    # Select both the raw asset and the dbt asset for Rick and Morty
    selection=AssetSelection.assets(
        rick_and_morty_asset, dbt_rick_and_morty_models)
)

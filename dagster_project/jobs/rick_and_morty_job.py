from dagster import job, define_asset_job
from dagster_project.assets.rick_and_morty import rick_and_morty_asset, dbt_rick_and_morty_data


RickandMorty_job = define_asset_job(
    name="RickandMorty_job",
    # Dagster auto-infers dependency on `uv_asset`
    selection=[rick_and_morty_asset, dbt_rick_and_morty_data]
)

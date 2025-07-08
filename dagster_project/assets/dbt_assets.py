import os
from dagster import AssetExecutionContext
from path_config import DBT_DIR
from dagster_dbt import dbt_assets, DbtCliResource, DbtProject
dbt_project = DbtProject(
    project_dir=DBT_DIR,
    profiles_dir=DBT_DIR,
)


# Define paths
dbt = DbtCliResource(project_dir=os.fspath(DBT_DIR))


dbt_manifest_path = DBT_DIR.joinpath("target", "manifest.json")


@dbt_assets(manifest=dbt_manifest_path,
            io_manager_key="io_manager", name="dbt_models")
def dbt_models(context: AssetExecutionContext, dbt: DbtCliResource):
    """Run dbt build command and return result."""
    yield from dbt.cli(["build"], context=context).stream()


@dbt_assets(manifest=dbt_manifest_path,
            io_manager_key="io_manager", name="dbt_common_models")
def dbt_common_models(context: AssetExecutionContext, dbt: DbtCliResource):
    """Run shared/common dbt models like date dimensions."""
    # Run only common models that don't depend on source data
    common_models = ["dim_date"]

    context.log.info(f"Running common dbt models: {common_models}")
    yield from dbt.cli(["build", "--select"] + common_models, context=context).stream()

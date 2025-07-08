from dagster import asset, AssetExecutionContext
import os
# import requests
from dotenv import load_dotenv
from pathlib import Path
import dlt
import time
import subprocess
from dlt.pipeline.exceptions import PipelineNeverRan
from dlt.destinations.exceptions import DatabaseUndefinedRelation
from dlt.sources.helpers.rest_client.paginators import JSONLinkPaginator
from dlt.sources.helpers.rest_client.client import RESTClient
from path_config import ENV_FILE, DLT_PIPELINE_DIR, DBT_DIR

load_dotenv(dotenv_path="/workspaces/CamOnDagster/.env")

BASE_URL = "https://rickandmortyapi.com/api"

# Configuration for resources: endpoint -> primary key
RESOURCE_CONFIG: dict[str, str] = {
    "character": "id",
    "episode": "id",
    "location": "id"
}


def make_resource(table_name: str, primary_key: str, existing_count: int):

    @dlt.resource(name=table_name, write_disposition="merge", primary_key=primary_key)
    def _resource(context: AssetExecutionContext):
        state = dlt.current.source_state().setdefault(table_name, {
            "count": 0,
            "last_run_status": None
        })

        client = RESTClient(
            base_url=f"{BASE_URL}/",
            paginator=JSONLinkPaginator(
                next_url_path="info.next"
            )
        )

        # Only fetch first page to check count
        try:
            response = client.session.get(
                f"{BASE_URL}/{table_name}", timeout=15)
            response.raise_for_status()
            first_page = response.json()
            info = first_page.get("info", {})
            new_count = info.get("count", 0)
        except Exception as e:
            context.log.error(
                f"❌ Failed to fetch API count for `{table_name}`: {e}")
            state["last_run_status"] = "failed"
            raise

        if existing_count < state["count"]:
            context.log.info(
                f"⚠️ Table `{table_name}` row count dropped from {state['count']} to {existing_count}. Forcing reload.")
        elif new_count == state["count"]:
            context.log.info(f"🔁 SKIPPED LOAD: `{table_name}` — No new data.")
            state["last_run_status"] = "skipped_no_new_data"
            return

        context.log.info(
            f"✅ New data for `{table_name}`: {state['count']} ➝ {new_count}")

        state["count"] = new_count
        state["last_run_status"] = "success"
        context.log.info(
            f"📊 Loading `{table_name}` data from Rick and Morty API...")
        for page in client.paginate(table_name):
            yield page

    return _resource


@dlt.source
def rick_and_morty_source(context: AssetExecutionContext, current_counts):
    for endpoint, primary_key in RESOURCE_CONFIG.items():
        yield make_resource(endpoint, primary_key, current_counts.get(endpoint, 0))(context)


@asset(compute_kind="python", group_name="RickAndMorty", tags={"source": "RickAndMorty"}, io_manager_key="mem_io_manager")
def rick_and_morty_asset(context: AssetExecutionContext) -> bool:
    """Loads characters, episodes, and locations from Rick and Morty API using DLT."""
    context.log.info("🚀 Starting DLT pipeline for Rick and Morty API")

    pipeline = dlt.pipeline(
        pipeline_name="rick_and_morty_pipeline",
        destination=os.getenv("DLT_DESTINATION", "motherduck"),
        dataset_name="rick_and_morty_data",
        pipelines_dir=str(DLT_PIPELINE_DIR),
        dev_mode=False
    )

    row_counts_dict = {}
    try:
        row_counts = pipeline.dataset().row_counts().df()
        if row_counts is not None:
            row_counts_dict = dict(
                zip(row_counts["table_name"], row_counts["row_count"]))
    except PipelineNeverRan:
        context.log.warning(
            "⚠️ No previous runs found for this pipeline. Assuming first run.")
        row_counts_dict = {}
    except DatabaseUndefinedRelation:
        context.log.warning(
            "⚠️ Table doesn't exist. Assuming deletion.")
        row_counts_dict = {}
    except Exception as e:
        context.log.warning(
            f"⚠️ Could not get row counts: {e}. Assuming first run.")
        row_counts_dict = {}

    source = rick_and_morty_source(context, row_counts_dict)
    try:
        pipeline.run(source)

        statuses = [source.state.get(resource, {}).get(
            "last_run_status") for resource in RESOURCE_CONFIG.keys()]

        if all(s == "skipped_no_new_data" for s in statuses):
            context.log.info(
                "⏭️ All resources skipped — no data loaded.")
            return False
        elif all(s == "failed" for s in statuses):
            context.log.error(
                "💥 All resources failed to load — check API or network.")
            return False

        loaded_count = sum(1 for s in statuses if s == "success")
        context.log.info(f"✅ Number of resources loaded: {loaded_count}")

        return True
    except Exception as e:
        context.log.error(f"❌ Pipeline run failed: {e}")
        return False


@asset(deps=["rick_and_morty_asset"], group_name="RickAndMorty",
       tags={"source": "RickAndMorty"}, required_resource_keys={"dbt"}, io_manager_key="mem_io_manager")
def dbt_rick_and_morty_models(context: AssetExecutionContext, rick_and_morty_asset: bool) -> None:
    """Runs Rick and Morty specific dbt models after loading data."""

    if not rick_and_morty_asset:
        context.log.warning(
            "\n⚠️  WARNING: DBT RICK AND MORTY MODELS SKIPPED\n"
            "📉 No data was loaded from Rick and Morty API.\n"
            "🚫 Skipping dbt run for Rick and Morty models.\n"
        )
        return

    try:
        # Run all dbt models downstream from the Rick and Morty source (source:rick_and_morty+)
        context.log.info("Running dbt models from source:rick_and_morty+")
        dbt_cli = context.resources.dbt
        result = dbt_cli.cli(
            ["build", "--select", "source:rick_and_morty+"], raise_on_error=False)

        # Wait for completion and handle result
        exit_code = result.wait()

        if exit_code == 0:
            context.log.info(
                "✅ Rick and Morty dbt models completed successfully!")
        else:
            context.log.error(
                f"❌ Rick and Morty dbt models failed with exit code: {exit_code}")
            # Get stdout and stderr for debugging
            context.log.error(f"stdout: {result.stdout}")
            context.log.error(f"stderr: {result.stderr}")
            raise Exception(
                f"Rick and Morty dbt models failed with exit code: {exit_code}")

    except Exception as e:
        context.log.error(f"Rick and Morty dbt models failed: {e}")
        raise

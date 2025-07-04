# 4DStack

A containerized data engineering project combining [Dagster](https://dagster.io/), [dbt](https://www.getdbt.com/), and [DLT](https://docs.dltHub.com/) to orchestrate, transform, and manage modern data workflows. It uses [MotherDuck](https://motherduck.com/) as the data warehouse with serverless compute. 

## 🧱 Project Structure

<details>

<summary><strong>📁 (click to expand)</strong></summary>

```text
CamOnDagsterDbt/
├── cam_on_dagster_dbt/           # Dagster jobs, assets, schedules, sensors, and definitions
│   ├── assets/                   # All asset definitions grouped by data source
│   ├── jobs/                     # Dagster job definitions
│   ├── schedules.py              # Dagster schedules
│   ├── sensors.py                # Dagster sensors
│   ├── definitions.py            # Central Dagster Definitions object
│   └── __init__.py               # Package initializer
├── dbt/                          # dbt models and configs
│   ├── models/                   # dbt models
│   ├── macros/                   # Custom macros
│   ├── dbt_project.yml           # dbt project configuration
│   └── profiles.yml              # dbt profile (excluded from git)
├── .devcontainer/                # Dev container setup
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── devcontainer.json
├── .github/workflows/            # GitHub Actions CI workflows
│   ├── docs.yml                  # Auto Generate DBT Docs
│   └── ci.yml                    # Automatic CI, builds when changes occur to dbt
├── docker-compose.yml            # Main Docker Compose file
├── requirements.txt              # Python dependencies
├── workspace.yaml                # Dagster workspace configuration
├── dagster.yaml                  # Dagster project configuration
└── README.md                     # Project documentation
```

</details>


### ⚙️ Stack

- 🔄 Dagster for workflow orchestration and asset management

- 📊 dbt for data modeling and transformations

- ⚙️ Data Load Tool (DLT) for incremental pipeline automation

- 🦆 Mother Duck for cloud analytics database

- ✔️ Great Expectations for data testing and validation

### Features

- Multi-source data ingestion pipelines: Google Sheets, TheCocktailDB, OpenLibrary, Rick and Morty API  
- Modular asset definitions and jobs for maintainability  
- Configured schedules and sensors to automate pipeline runs  
- Centralized definitions to easily manage asset and job dependencies  
- Integration of Great Expectations for data quality validation  
- Environment configurations prepared for local and containerized execution  

### MotherDuck Migration and Future Orchestration with Dagster Cloud

The project has recently migrated from local DuckDB to MotherDuck, a cloud-native SQL lakehouse platform, to leverage scalable and performant data warehousing capabilities. This migration positions the project to benefit from a managed, serverless infrastructure that simplifies data storage and query execution.

Additionally, there are plans to implement Dagster Cloud for orchestration, which will provide a robust, cloud-based workflow management system. This will enable scalable scheduling, monitoring, and observability of data pipelines, complementing the move to MotherDuck.

This approach ensures the project is future-proofed with a fully managed, cloud-first data stack, improving reliability, scalability, and ease of maintenance while retaining infrastructure-as-code best practices for smooth deployment and governance.

### Next Steps
 
- Enhance data quality checks with Great Expectations integration  
- Expand pipeline coverage with additional APIs and datasets


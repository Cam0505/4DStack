#!/bin/bash
set -e

# Change to the project directory
cd /workspaces/4DStack

# Explicitly set DAGSTER_HOME to ensure it's correct
export DAGSTER_HOME="/workspaces/4DStack/dagster_home"

# Start Postgres service using docker compose
echo "Starting Postgres service with docker compose..."
docker compose up -d postgres

# Wait for Postgres to be ready
echo "Waiting for Postgres to be ready..."
until docker exec $(docker compose ps -q postgres) pg_isready -U dagster > /dev/null 2>&1; do
    sleep 1
done

echo "Postgres is ready."


# Only install if Chromium browser binary is missing
if [ ! -f /home/vscode/.cache/ms-playwright/chromium-*/chrome-linux/chrome ]; then
    echo "Chromium browser not found, installing..."
    python -m playwright install chromium
else
    echo "Chromium browser already installed."
fi

# Start Dagster dev in the background
echo "Starting Dagster dev server..."
dagster dev &

echo "Startup complete."
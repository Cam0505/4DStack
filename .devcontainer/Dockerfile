FROM mcr.microsoft.com/devcontainers/python:3.11

# Install essential system dependencies and Playwright requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    wget \
    unzip \
    # Playwright system dependencies
    libnss3-dev \
    libatk-bridge2.0-dev \
    libdrm2 \
    libxkbcommon-dev \
    libxcomposite-dev \
    libxdamage-dev \
    libxrandr-dev \
    libgbm-dev \
    libxss1 \
    libasound2-dev \
    libatspi2.0-0 \
    libgtk-3-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .


# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (do this as root before switching to vscode user)
RUN python -m playwright install chromium

# Copy only dbt dependency files to leverage Docker cache
COPY dbt/packages.yml dbt/dbt_project.yml ./dbt/

# Run dbt deps to install dbt dependencies
RUN cd dbt && dbt deps

# Copy the rest of your application code
COPY . .

# Ensure startup script is executable and has Unix line endings
RUN chmod +x .devcontainer/startup.sh && \
    sed -i 's/\r$//' .devcontainer/startup.sh

# Set working directory to match compose file
WORKDIR /workspaces/4DStack

USER vscode

# syntax=docker/dockerfile:1
FROM selenium/standalone-all-browsers:nightly

WORKDIR /app

# Install python
# RUN apt-get update && \
#     apt-get install -y python3 python3-pip && \
#     rm -rf /var/lib/apt/lists/*

# Install uv
# RUN pip install --no-cache-dir uv

# Copy pyproject.toml and related files for dependency installation
# COPY backend/pyproject.toml .

# Install dependencies using uv
# RUN uv sync
# Copy application source
COPY backend/ .

RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app", "--log-level", "info"]
# syntax=docker/dockerfile:1
FROM python:latest

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy pyproject.toml and related files for dependency installation
COPY backend/pyproject.toml .

# Install dependencies using uv
RUN uv pip install --system -e .

# Copy application source
COPY backend/ .

# Expose port
EXPOSE 8000

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app", "--log-level", "info"]
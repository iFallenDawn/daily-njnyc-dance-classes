# syntax=docker/dockerfile:1
FROM selenium/standalone-all-browsers:nightly

WORKDIR /app

# set timezone to est
ENV TZ=America/New_York

# Copy application source
COPY backend/ .

# Install uv
RUN pip install --no-cache-dir uv

# copy uv files to requirements.txt
RUN uv pip compile pyproject.toml --output-file requirements.txt

# install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--reload-dir", "/app", "--log-level", "info"]
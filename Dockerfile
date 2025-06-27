FROM python:3.12-slim

# Set environment variables
ENV UV_COMPILE_BYTECODE=1 \
    UV_PROJECT_ENVIRONMENT="/opt/python/.local" \
    PATH="/opt/python/.local/bin:$PATH"

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Create a non-root user and set permissions
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

# Copy entrypoint script
COPY --chown=appuser:appuser docker-entrypoint.sh /app/docker-entrypoint.sh
RUN chmod +x /app/docker-entrypoint.sh

# Copy the rest of the application
COPY --chown=appuser:appuser . /app/

# Install dependencies using uv in the virtual environment
RUN uv sync --active

# Change ownership of the venv to the appuser
RUN chown -R appuser:appuser /opt/python/.local

RUN ls -alh

# Expose port
EXPOSE 8000

# USER appuser

# Use entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]

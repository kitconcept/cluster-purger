# syntax=docker/dockerfile:1
FROM python:3.11-slim as python-base

LABEL maintainer="kitconcept GmbH <info@kitconcept.com>" \
      org.label-schema.name="cluster-purger" \
      org.label-schema.description="Purge multiple instances of Varnish inside a cluster" \
      org.label-schema.vendor="kitconcept GmbH" \
      org.opencontainers.image.source="https://github.com/kitconcept/cluster-purger"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Run Poetry without interactions
ENV POETRY_NO_INTERACTION=1

# Install the Poetry virtualenv inside the project
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Install wget (to run healthchecks), dnsutils (debugging)
# Install Poetry
# Create appuser
RUN <<EOT
    apt-get update
    apt-get -y upgrade
    apt-get install -y --no-install-recommends dnsutils wget
    apt-get clean -y
    useradd --system -m -d /app -U -u 500 appuser
    chown -R 500:500 /app
    python -m pip install poetry
EOT

# Set /app as working directory
WORKDIR /app

# Copy project files to the container
COPY --chown=500:500 cluster_purger /app/cluster_purger
COPY --chown=500:500 pyproject.toml poetry.lock README.md /app/

# Install Poetry
RUN <<EOT
    poetry install --without test
EOT

# Expose port 80
EXPOSE 80

# User appuser
USER appuser

# prepend poetry and venv to path
ENV PATH="/app/.venv/bin:$PATH"

# Set healthcheck to port 8080
HEALTHCHECK --interval=5s --timeout=5s --start-period=30s CMD [ -n "$LISTEN_PORT" ] || LISTEN_PORT=80 ; wget -q http://127.0.0.1:"$LISTEN_PORT"/ok -O - | grep Ok || exit 1

# Run uvicorn
CMD ["uvicorn", "cluster_purger.app:app", "--host", "0.0.0.0", "--port", "80"]

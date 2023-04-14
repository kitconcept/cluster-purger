#!/bin/bash
set -e

echo "======================================================================================="
if [ -z "${OTEL_EXPORTER_OTLP_ENDPOINT}" ]; then
  echo "Starting cluster-purger"
  OTEL=""
else
  echo "Starting cluster-purger with opentelemetry support"
  OTEL="opentelemetry-instrument"
fi
echo "======================================================================================="


exec $OTEL uvicorn cluster_purger.app:app --host 0.0.0.0 --port 80

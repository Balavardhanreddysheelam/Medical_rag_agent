#!/bin/sh
set -e

QDRANT_STORAGE_DIR=${QDRANT_STORAGE_DIR:-/data/qdrant}
mkdir -p "$QDRANT_STORAGE_DIR"

echo "Starting Qdrant service..."
qdrant --storage-root "$QDRANT_STORAGE_DIR" --http-port 6333 --grpc-port 6334 &
QDRANT_PID=$!

cleanup() {
  echo "Stopping Qdrant..."
  kill "$QDRANT_PID"
}
trap cleanup INT TERM

# Wait a moment for Qdrant to come online
sleep 3

echo "Starting FastAPI server..."
uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"


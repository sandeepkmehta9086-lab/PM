#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
echo "Starting backend via Docker Compose..."
docker-compose up --build
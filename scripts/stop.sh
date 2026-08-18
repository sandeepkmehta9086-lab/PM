#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
echo "Stopping backend via Docker Compose..."
docker-compose down
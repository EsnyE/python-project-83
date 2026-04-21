#!/usr/bin/env bash
set -e

echo "Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

echo "Installing project dependencies..."
make install

echo "Waiting for database to be ready..."

if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL is not set"
    exit 1
fi

echo "Running database migrations..."
PGCONNECT_TIMEOUT=10 psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f database.sql

echo "Build completed successfully!"
#!/usr/bin/env bash
set -e

echo "Installing uv package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

echo "Installing project dependencies..."
make install

echo "Running database migrations..."
psql -a -d $DATABASE_URL -f database.sql

echo "Build completed successfully!"
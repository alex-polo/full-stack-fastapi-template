#!/usr/bin/env sh
set -e

if [ ! -f .env.local ]; then
  echo "Error: .env.production not found in project root" >&2
  exit 1
fi


exec docker compose \
    --env-file .env.production \
    -f compose.yml \
    -f compose.prod.yml \
    up --build
#!/usr/bin/env sh
set -e
set -x

if [ ! -f .env.local ]; then
  echo "Error: .env not found in project root" >&2
  exit 1
fi


exec docker compose \
    --env-file .env \
    -f compose.yml \
    -f compose.override.yml \
    up --build --watch
#!/usr/bin/env bash

set -e
set -x


if [[ "$ENVIRONMENT" == "local" ]] || [[ "$ENVIRONMENT" == "staging" ]]; then
    echo "Generate JWT certificates"
    ./scripts/generate_jwt_keys.sh
elif [[ "$ENVIRONMENT" == "production" ]]; then
    echo "Verify JWT certificates exist in production"
    if [[ ! -f "./certificates/jwt-private.pem" ]] || [[ ! -f "./certificates/jwt-public.pem" ]]; then
        echo "ERROR: JWT keys are missing in production. Please generate them manually." >&2
        exit 1
    fi
else
    echo "ERROR: Invalid ENVIRONMENT value: '$ENVIRONMENT'. Expected: local, staging, or production." >&2
    exit 1
fi


echo "Waiting for database to start"
python await_db.py

echo "Run database migrations"
alembic upgrade head

echo "Create initial data in DB"
python initial.py

exec "$@"
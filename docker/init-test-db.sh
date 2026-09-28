#!/bin/sh
set -eu

: "${POSTGRES_TEST_DB:?POSTGRES_TEST_DB must be set}"

psql \
    --username "$POSTGRES_USER" \
    --dbname "$POSTGRES_DB" \
    --set=test_db="$POSTGRES_TEST_DB" \
    --set=ON_ERROR_STOP=1 <<'EOSQL'
SELECT format('CREATE DATABASE %I', :'test_db')
WHERE NOT EXISTS (
    SELECT FROM pg_database WHERE datname = :'test_db'
)\gexec
EOSQL

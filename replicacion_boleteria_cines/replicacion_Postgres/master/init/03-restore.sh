#!/bin/bash
set -e
PGPASSWORD=INTERLUDE44 pg_restore -U kleynerbuzz -h localhost -p 5432 -d "$POSTGRESQL_DATABASE" --no-owner --no-acl -v /docker-entrypoint-initdb.d/Boleteria_Cines_Postgres.dump

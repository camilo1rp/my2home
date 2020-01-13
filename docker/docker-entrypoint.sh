#!/bin/bash
set -e

# read docker secrets into env variables
export SUPERUSER_PASSWORD=$(cat /run/secrets/superuser_password)
export DB_PASSWORD=$(cat /run/secrets/db_password)
export SECRET_KEY=$(cat /run/secrets/secret_key)

# run db migrations (retry on error)
while ! python3 /opt/my2home/manage.py migrate 2>&1; do
	sleep 5
done

# start daphene
daphne -b seed7 -p 8003 --root-path /opt/my2home/ myhome.asgi:application
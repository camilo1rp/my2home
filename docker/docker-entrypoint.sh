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

# run python3 manage.py collectstatic
python3 /opt/my2home/manage.py collectstatic --noinput

#move to seed_7 directory
cd /opt/my2home/

# start daphene
daphne -b my2home -p 8003 seed_7.asgi:application
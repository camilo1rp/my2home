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

# create superuser
create_superuser="
import django
django.setup()
from django.contrib.auth.models import User
try:
    User.objects.create_superuser('$DJANGO_SUPERUSER_NAME', '$DJANGO_SUPERUSER_MAIL', '$DJANGO_SUPERUSER_PASS')
except Exception:
    pass
"
create_superuser() {
    if [ -z "$DJANGO_SUPERUSER_NAME" ] || [ -z "$DJANGO_SUPERUSER_MAIL" ] || [ -z "$DJANGO_SUPERUSER_PASS" ]; then
        echo "Environment variables for database not set, not creating superuser."
    else
        echo "Creating superuser"
        python3 -c "$create_superuser"
    fi
}


# run python3 manage.py collectstatic
python3 /opt/my2home/manage.py collectstatic --noinput

#move to seed_7 directory
cd /opt/my2home/

# start daphene
daphne -b my2home -p 8080 myhome.asgi:application

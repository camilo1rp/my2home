#!/bin/bash
set -e

# read docker secrets into env variables
export DJANGO_SUPERUSER_PASSWORD=$(cat /run/secrets/django_superuser_password)
export DJANGO_SUPERUSER_MAIL=$(cat /run/secrets/django_superuser_mail)
export DB_PASSWORD=$(cat /run/secrets/db_password)
export SECRET_KEY=$(cat /run/secrets/secret_key)

# run db migrations (retry on error)
while ! python3 /opt/my2home/manage.py migrate 2>&1; do
	sleep 5
done

# Create Superuser if required
if [ "$DJANGO_SKIP_SUPERUSER" == "true" ]; then
  echo "↩️ Skip creating the superuser"
else
  if [ -z ${DJANGO_SUPERUSER_NAME+x} ]; then
    SUPERUSER_NAME='admin'
  fi
  if [ -z ${DJANGO_SUPERUSER_EMAIL+x} ]; then
    SUPERUSER_EMAIL='admin@example.com'
  fi
  if [ -z ${DJANGO_SUPERUSER_PASSWORD+x} ]; then
    if [ -f "/run/secrets/django_superuser_password" ]; then
      SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD
    else
      SUPERUSER_PASSWORD='admin'
    fi
  fi

  ./manage.py shell --interface python3 << END
from django.contrib.auth.models import User
if not User.objects.filter(username='${DJANGO_SUPERUSER_NAME}'):
    u=User.objects.create_superuser('${DJANGO_SUPERUSER_NAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}')
END
  echo "💡 Superuser Username: ${DJANGO_SUPERUSER_NAME}, E-Mail: ${DJANGO_SUPERUSER_EMAIL}"
fi


# run python3 manage.py collectstatic
python3 /opt/my2home/manage.py collectstatic --noinput

#move to seed_7 directory
cd /opt/my2home/

# start daphene
daphne -b my2home -p 8080 myhome.asgi:application

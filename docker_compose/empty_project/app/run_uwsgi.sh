#!/usr/bin/env bash

set -e

FILE=/opt/app/created

if [ -f "$FILE" ]; then
    python manage.py collectstatic --noinput && \
    yes | python manage.py makemigrations --merge && \
    python manage.py migrate --fake movies 0001 --noinput && \
    python manage.py migrate --noinput && \
    python manage.py createsuperuser --noinput || echo superuser exist && \
    python /mnt/sqlite_to_postgres/load_data.py
    touch /opt/app/created
fi

chown www-data:www-data /var/log

uwsgi --strict --ini /opt/app/uwsgi.ini

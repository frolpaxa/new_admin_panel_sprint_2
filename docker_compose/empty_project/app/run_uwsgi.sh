#!/usr/bin/env bash

set -e

while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
done 

python manage.py collectstatic --noinput && \
python manage.py migrate --fake movies 0001 --noinput && \
python manage.py migrate --noinput && \
python manage.py createsuperuser --noinput || echo superuser exist && \
python /mnt/sqlite_to_postgres/load_data.py

chown www-data:www-data /var/log

uwsgi --strict --ini /opt/app/uwsgi.ini

#!/usr/bin/env bash

set -e

python manage.py collectstatic --noinput
python manage.py makemigrations --merge
python manage.py migrate --noinput
python manage.py createsuperuser --noinput

chown www-data:www-data /var/log

uwsgi --strict --ini /opt/app/uwsgi.ini

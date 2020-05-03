#!/usr/bin/ash

python manage.py wait_for_database

python manage.py migrate

exec uwsgi --ini /opt/warsawlo/uwsgi.ini
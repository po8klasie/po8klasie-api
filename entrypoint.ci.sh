#!/usr/bin/ash

black . --check

python manage.py test --noinput
#!/usr/bin/ash

python manage.py wait_for_database

echo "🚨 Running linter"

black . --check

echo "✅ Running tests"

python manage.py test --noinput
#!/usr/bin/ash

echo "🚨 Running linters"

flake8
black . --check


python manage.py wait_for_database


echo "🗃️ Checking migrations"

python manage.py makemigrations --check --dry-run --no-input

echo "✅ Running tests"

python manage.py test --noinput
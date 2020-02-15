release: python manage.py migrate
web: python manage.py collectstatic --noinput
web: gunicorn warsawlo.wsgi --log-file -
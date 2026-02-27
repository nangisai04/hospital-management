web: gunicorn hospital.wsgi
# run migrations and collect static assets on each release
release: python manage.py migrate && python manage.py collectstatic --noinput

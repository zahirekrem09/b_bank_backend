release: python manage.py makemigrations authentication
release: python manage.py makemigrations ticket
release: python manage.py migrate --no-input
web: gunicorn bbank.wsgi

#!/bin/sh

echo "Waiting for database..."

python manage.py migrate --noinput

echo "Database migrations completed."

exec python manage.py runserver 0.0.0.0:8000
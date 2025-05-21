#!/bin/sh

# Exit on error
set -e

# Run DB migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn taskmanagement.wsgi:application --bind 0.0.0.0:8000

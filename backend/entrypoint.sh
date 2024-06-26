#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate
echo "Your auth token"
python manage.py adduser
# Start server
echo "Starting server"
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
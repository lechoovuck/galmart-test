#!/bin/bash

echo "Starting the server..."


until pg_isready -h "$DATABASE_HOST_PRIMARY" -p "$DATABASE_PORT" -U "$DATABASE_USER"; do
  echo "Waiting for PostgreSQL at $DATABASE_HOST_PRIMARY:$DATABASE_PORT..."
  sleep 2
done

if [[ "$*" == *"runserver"* ]]; then

echo "Making migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser created')
else:
    print('Superuser already exists')
"

echo "Loading mock data..."
python manage.py loaddata mock_data.json || echo "File mock_data.json not found, skipping..."

fi

echo "Starting development server..."
exec "$@"

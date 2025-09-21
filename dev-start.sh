#!/usr/bin/env bash
set -e

echo "🚀 Starting development server..."

# Wait for database
echo "Waiting for database..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  sleep 1
done
echo "Database is ready!"

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser if it doesn't exist (email-based)
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(email='admin@example.com').exists() or User.objects.create_superuser(email='admin@example.com', password='admin123')" | python manage.py shell || true

# Start Tailwind watcher in background
echo "Starting Tailwind CSS watcher..."
python manage.py tailwind start --poll &

# Start Django development server
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000
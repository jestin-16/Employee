#!/bin/sh
set -e

echo "=== [DevOps Container Virtualization] Initializing Web Service ==="

# Wait for MySQL database if host is specified
if [ -n "$DB_HOST" ] && [ "$DB_HOST" != "localhost" ] && [ "$DB_HOST" != "127.0.0.1" ]; then
    echo "Waiting for MySQL database at $DB_HOST:${DB_PORT:-3306}..."
    while ! nc -z "$DB_HOST" "${DB_PORT:-3306}" 2>/dev/null && ! python -c "import socket; s = socket.socket(); s.settimeout(2); s.connect(('$DB_HOST', int('${DB_PORT:-3306}'))); s.close()" 2>/dev/null; do
        echo "Database unavailable. Retrying in 2 seconds..."
        sleep 2
    done
    echo "MySQL Database is up and accepting connections!"
fi

echo "Applying Django database migrations..."
python manage.py migrate --noinput

echo "Collecting static assets for Nginx offloading..."
python manage.py collectstatic --noinput --clear || true

echo "Seeding initial virtualization & administrative demo data..."
python seed_data.py || true

echo "Starting Gunicorn WSGI Production Server on 0.0.0.0:8000..."
exec gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -


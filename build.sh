#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py create_deploy_superuser || true
python manage.py migrate
exec gunicorn ecommerce.wsgi --bind 0.0.0.0:${PORT:-8000}
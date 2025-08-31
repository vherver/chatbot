#!/bin/sh
echo "==> Compile Django localization messages"
django-admin compilemessages

echo "==> Run Django migrations"
python manage.py migrate

echo "==> Run Django server"
python manage.py runserver 0.0.0.0:8000
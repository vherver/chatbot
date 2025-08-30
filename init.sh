echo "==> Compile Django localization messages"

echo "==> Compile Django localization messages"
django-admin compilemessages
echo "==> Run Django migrations"
python manage.py migrate
echo "==> Run Django manage.py"
python manage.py runserver 0.0.0.0:8000


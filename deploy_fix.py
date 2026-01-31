import os
import django
from django.core.management import call_command

# Set production settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

# Run migrations
call_command("migrate", interactive=False)

# Collect static files
call_command("collectstatic", interactive=False, verbosity=0)

# Create superuser if it doesn't exist
from django.contrib.auth import get_user_model
User = get_user_model()

SUPERUSER_PASSWORD = os.environ.get("SUPERUSER_PASSWORD", "changeme123")

if not User.objects.filter(is_staff=True).exists():
    User.objects.create_superuser(
        username="maks_kozzz777",
        email="maksym.kozlovskyi150210@gmail.com",
        password=SUPERUSER_PASSWORD
    )
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
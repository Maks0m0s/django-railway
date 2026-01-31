import os
import django

# Make sure this points to your production settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(is_staff=True).exists():
    User.objects.create_superuser(
        username="maks_kozzz777",
        email="maksym.kozlovskyi150210@gmail.com",
        password="esferitadegauss1985"
    )
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
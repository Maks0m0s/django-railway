import os
import django
import time
import psycopg2
from django.core.management import call_command
from django.db.utils import OperationalError

# ==============================
# Settings
# ==============================
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django.setup()

# ==============================
# Wait for Postgres
# ==============================
DB_HOST = os.environ.get("PGHOST")
DB_NAME = os.environ.get("PGDATABASE")
DB_USER = os.environ.get("PGUSER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
DB_PORT = os.environ.get("PGPORT", 5432)

print("Waiting for database to be ready...")

while True:
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
        )
        conn.close()
        print("Database is ready!")
        break
    except OperationalError:
        print("Database not ready, retrying in 3 seconds...")
        time.sleep(3)

# ==============================
# Run migrations
# ==============================
try:
    print("Running migrations...")
    call_command("migrate", interactive=False)
except Exception as e:
    print(f"Error running migrations: {e}")

# ==============================
# Collect static files
# ==============================
try:
    print("Collecting static files...")
    call_command("collectstatic", interactive=False, verbosity=0)
except Exception as e:
    print(f"Error collecting static files: {e}")

# ==============================
# Create superuser if not exists
# ==============================
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

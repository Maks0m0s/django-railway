from django.contrib.auth.models import User
from main.services.email_service import send_registration_email, send_update_ac_email
from main.services.dashboard_service import create_dashboard, delete_dashboard
from django.contrib.auth import update_session_auth_hash

from main.services.settings_service import create_profile_settings


def register(validated_data):
    user = User(
        username=validated_data["username"],
        email=validated_data.get("email", ""),
        first_name=validated_data.get("first_name", ""),
        last_name=validated_data.get("last_name", ""),
    )
    user.set_password(validated_data["password"])
    user.save()

    create_dashboard(user)

    create_profile_settings(user)

    send_registration_email(user)

    return user

def delete_account(request):
    user = request.user

    delete_dashboard(user)

    user.delete()          # delete from DB

def update_account(request):
    user = request.user

    username = request.POST.get('username', '').strip()
    email = request.POST.get('email', '').strip()
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    current_password = request.POST.get('current_password', '')
    new_password = request.POST.get('new_password', '').strip()

    # --- VALIDATION ---
    if not username:
        return {'result': False, 'error': 'Username is required'}

    if not email or '@' not in email:
        return {'result': False, 'error': 'Invalid email'}

    if not current_password:
        return {'result': False, 'error': 'Current password is required'}

    if not user.check_password(current_password):
        return {'result': False, 'error': 'Current password is incorrect'}

    # --- UPDATE FIELDS ---
    user.username = username
    user.email = email
    user.first_name = first_name
    user.last_name = last_name

    # --- UPDATE PASSWORD (optional) ---
    if new_password:
        user.set_password(new_password)
        update_session_auth_hash(request, user)

    user.save()

    send_update_ac_email(user)

    return {'result': True}


def get_admin():
    admin = User.objects.filter(is_staff=True).first()
    return admin
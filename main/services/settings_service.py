from main.models import ProfileSettings

def create_profile_settings(user):
    settings = ProfileSettings.objects.create(user=user, is_public=True, hide_email=False)
    settings.save()

def get_settings(user):
    settings = ProfileSettings.objects.filter(user=user).first()
    return settings


def update_settings(user, data):
    settings, _ = ProfileSettings.objects.get_or_create(user=user)

    account_type = data.get('account_type', '')
    hide_email = data.get('hide_email') == 'on'

    if account_type == 'public':
        settings.is_public = True
    elif account_type == 'private':
        settings.is_public = False

    settings.hide_email = hide_email
    settings.save()

    return {
        'result': True,
        'settings': settings
    }
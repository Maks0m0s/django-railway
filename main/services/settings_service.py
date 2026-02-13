from main.models import ProfileSettings


def get_settings(user):
    settings, _ = ProfileSettings.objects.get_or_create(user=user)
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
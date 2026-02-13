from main.models import ProfileSettings

def create_profile_settings(user):
    # just create the object, no need to save again
    ProfileSettings.objects.create(user=user, is_public=True, hide_email=False)

def get_settings(user):
    # ensures settings always exist
    settings, _ = ProfileSettings.objects.get_or_create(user=user)
    return settings

def update_settings(user, data):
    settings, _ = ProfileSettings.objects.get_or_create(user=user)

    account_type = data.get('account_type', '')
    hide_email = data.get('hide_email') == 'on'

    settings.is_public = account_type == 'public'
    settings.hide_email = hide_email
    settings.save()

    return {'result': True, 'settings': settings}
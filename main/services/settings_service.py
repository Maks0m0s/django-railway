from main.models import Settings

def create_profile_settings(user):
    # just create the object, no need to save again
    try:
        Settings.objects.create(user=user, is_public=True, hide_email=False)
    except Exception as ex:
        print(f"Couldn't create profile settings obj. Error : {ex}")

def get_settings(user):
    # ensures settings always exist
    try:
        settings, _ = Settings.objects.get_or_create(user=user)
        return settings
    except Exception as ex:
        print(f"Couldn't get profile settings obj. Error : {ex}")

def update_settings(user, data):
    settings, _ = Settings.objects.get_or_create(user=user)

    account_type = data.get('account_type', '')
    hide_email = data.get('hide_email') == 'on'

    settings.is_public = account_type == 'public'
    settings.hide_email = hide_email
    settings.save()

    return {'result': True, 'settings': settings}
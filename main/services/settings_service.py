from main.models import ProfileSettings

def get_settings(request):
    settings = request.user.settings
    if not settings:
        settings = ProfileSettings.objects.create(user=request.user)
    return settings

def update_settings(request):
    settings = request.user.settings
    if not settings:
        return {'result':False, 'error':"Profile Settings doesn't exist"}

    account_type = request.POST.get('account_type', '')
    hide_email = request.POST.get('hide_email')

    is_public = settings.is_public

    if account_type == 'public' and is_public == False:
        is_public = True
    elif account_type == 'private' and is_public == True:
        is_public = False

    settings.is_public = is_public
    settings.hide_email = hide_email
    settings.save()

    return {'result':True, 'settings':settings}
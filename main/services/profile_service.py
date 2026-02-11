from main.models import ProfileLink

def add_profile_link(request):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')
    user = request.user

    if not name or not name.strip():
        return {'result':False, 'error':"Link's name not inserted."}

    if not url or not url.strip():
        return {'result':False, 'error':"Link's url not inserted."}

    ProfileLink.objects.create(
        name=name,
        url=url,
        user=user
    )
    return {'result':True}

def delete_profile_link(link_id):
    link = ProfileLink.objects.get(id=link_id)
    if not link:
        return {'result': False, 'error': "Link not found."}

    link.delete()
    return {'result': True}
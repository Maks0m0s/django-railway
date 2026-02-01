from main.models import Dashboard, Project, Link, Photo

def create_project(request):
    name = request.POST.get('name')
    description = request.POST.get('description', '')
    link_names = request.POST.getlist('link_name[]')
    link_urls = request.POST.getlist('link_url[]')
    uploaded_photos = request.FILES.getlist('photos[]')
    try:
        print(uploaded_photos)
    except:
        print(len(uploaded_photos))

    if not name or not name.strip():
        return {'result': False, 'error': 'Project name is required'}

    dashboard, _ = Dashboard.objects.get_or_create(user=request.user)

    if dashboard.projects.filter(name=name).exists():
        return {'result': False, 'error': 'Project name already exists'}

    project = Project.objects.create(
        user=request.user,
        name=name,
        description=description,
    )

    # CREATE LINKS
    for ln, url in zip(link_names, link_urls):
        if ln.strip() and url.strip():
            link_obj = Link.objects.create(name=ln.strip(), url=url.strip())
            project.links.add(link_obj)

    # UPLOAD PHOTOS (FIXED)
    for photo_file in uploaded_photos:
        if not photo_file.name:
            photo_file.name = f'image_{photo_file.size}.png'

        try:
            photo_obj = Photo.objects.create(photo=photo_file)
            project.photos.add(photo_obj)
        except Exception as e:
            print(f"Error saving photo: {e}")

    dashboard.projects.add(project)

    return {'result': True, 'dashboard': dashboard}


def update_project(request, pk):
    project = get_project(request.user, pk)
    if not project:
        return {'result': False, 'error': 'Project not found'}

    name = request.POST.get('name')
    description = request.POST.get('description', '')
    link_names = request.POST.getlist('link_name[]')
    link_urls = request.POST.getlist('link_url[]')
    uploaded_photos = request.FILES.getlist('photos[]')
    delete_photo_ids = request.POST.getlist('delete_photos[]')

    if not name or not name.strip():
        return {'result': False, 'error': 'Project name is required'}

    project.name = name
    project.description = description
    project.save()

    # DELETE PHOTOS (FIXED)
    if delete_photo_ids:
        photos_to_delete = project.photos.filter(id__in=delete_photo_ids)
        for photo in photos_to_delete:
            project.photos.remove(photo)
            photo.delete()

    # ADD NEW PHOTOS (FIXED)
    for photo_file in uploaded_photos:
        if not photo_file.name:
            photo_file.name = f'image_{photo_file.size}.png'

        try:
            photo_obj = Photo.objects.create(photo=photo_file)
            project.photos.add(photo_obj)
        except Exception as e:
            print(f"Error saving photo: {e}")

    # UPDATE LINKS
    project.links.clear()
    for ln, url in zip(link_names, link_urls):
        if ln.strip() and url.strip():
            link_obj = Link.objects.create(name=ln.strip(), url=url.strip())
            project.links.add(link_obj)

    dashboard = Dashboard.objects.get(user=request.user)
    return {'result': True, 'dashboard': dashboard}


def get_project(user, pk):
    return Project.objects.filter(id=pk, user=user).first()


def delete_project(request, pk):
    project = get_project(request.user, pk)
    if not project:
        return {'result': False, 'error': 'Project not found'}

    project.delete()
    dashboard = Dashboard.objects.get(user=request.user)
    return {'result': True, 'dashboard': dashboard}
from django.shortcuts import render, get_object_or_404
from main.models import Photo

def photo_detail(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    return render(request, 'main/photo_detail.html', {'photo': photo})
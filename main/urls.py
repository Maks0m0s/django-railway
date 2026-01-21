from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main.api.home_views import HomeViewSet
from main.api.about_views import AboutViewSet


urlpatterns = [
    path('', HomeViewSet.as_view({'get': 'list'}), name='home'),
    path('about/', AboutViewSet.as_view({'get':'list'}), name='about')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
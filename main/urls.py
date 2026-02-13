from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main.views import photo_detail
from main.api.home_views import HomeViewSet
from main.api.about_views import AboutViewSet
from main.api.auth_views import AuthViewSet
from main.api.profile_views import ProfileViewSet
from main.api.project_views import ProjectViewSet
from main.api.search_views import SearchViewSet
from main.api.feedback_views import ProjectFeedbackViewSet
from main.api.settings_views import SettingsViewSet

login_views = AuthViewSet.as_view({'get':'login', 'post':'login'})
register_views = AuthViewSet.as_view({'get':'register', 'post':'register'})
logout_views = AuthViewSet.as_view({'get':'logout'})
delete_ac_views = AuthViewSet.as_view({'post':'delete'})
update_ac_views = AuthViewSet.as_view({'get':'update', 'post':'update'})

search_users = SearchViewSet.as_view({'get':'search'})

urlpatterns = [
    path('', HomeViewSet.as_view({'get': 'list'}), name='home'),
    path('about/', AboutViewSet.as_view({'get':'list'}), name='about'),
    path('photo/<int:photo_id>/', photo_detail, name='photo-detail'),

    path('auth/login/', login_views, name='auth-login'),
    path('auth/register/', register_views, name='auth-register'),
    path('auth/logout/', logout_views, name='auth-logout'),
    path('auth/delete/', delete_ac_views, name='auth-delete'),
    path('auth/update/', update_ac_views, name='auth-update'),

    path('profile/', ProfileViewSet.as_view({'get':'list'}), name='profile'),
    path('users/<int:pk>/', ProfileViewSet.as_view({'get':'user_profile'}), name='user-profile'),
    path('users/<int:user_id>/project/<int:pk>/', ProjectViewSet.as_view({'get':'user_project'}), name='user-project'),
    path('users/<int:user_id>/project/<int:pk>/add-comment/', ProjectFeedbackViewSet.as_view({'post':'add_comment'}), name='add-comment'),
    path('users/<int:user_id>/project/<int:project_id>/delete-comment/<int:pk>/', ProjectFeedbackViewSet.as_view({'post': 'delete_comment'}),
         name='delete-comment'),
    path('users/<int:user_id>/project/<int:pk>/toggle-like/', ProjectFeedbackViewSet.as_view({'post':'toggle_like'}), name='toggle-like'),
    path('users/<int:pk>/dashboard/', ProjectViewSet.as_view({'get':'user_dashboard'}), name='user-dashboard'),

    path('dashboard/', ProjectViewSet.as_view({'get':'list'}), name='dashboard'),
    path('project/<int:pk>/', ProjectViewSet.as_view({'get':'retrieve'}), name='project'),
    path('create-project/', ProjectViewSet.as_view({'get':'create_project', 'post':'create_project'}), name='create-project'),
    path('update-project/<int:pk>/', ProjectViewSet.as_view({'get': 'update_project', 'post': 'update_project'}), name='update-project'),
    path('delete-project/<int:pk>/', ProjectViewSet.as_view({'post': 'delete_project'}), name='delete-project'),

    path('profile/add-link/', ProfileViewSet.as_view({'post':'add_profile_link'}), name='add-profile-link'),
    path('profile/delete-link/<int:pk>/', ProfileViewSet.as_view({'post': 'delete_profile_link'}), name='delete-profile-link'),

    path('search/', search_users, name='search'),
    path('admin-profile/', AuthViewSet.as_view({'get':'get_admin'}), name='get-admin'),

    path('settings/', SettingsViewSet.as_view({'get':'list'}), name='settings'),
    path('settings/update/', SettingsViewSet.as_view({'post':'update_settings'}), name='update-settings')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
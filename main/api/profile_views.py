from rest_framework import viewsets, permissions
from django.shortcuts import render
from rest_framework.decorators import action
from django.contrib.auth.models import User
from main.authentication import is_auth

from main.services.dashboard_service import get_dashboard
from main.permissions import IsAuthenticatedOrRedirect

class ProfileViewSet(viewsets.ViewSet):

    # default permission (fallback)
    permission_classes = [IsAuthenticatedOrRedirect]

    def get_permissions(self):
        # Make user_profile public
        if self.action == 'user_profile':
            return [permissions.AllowAny()]
        return [IsAuthenticatedOrRedirect()]

    def list(self, request):
        is_auth(request)
        # Only authenticated users can see their own profile
        dashboard = get_dashboard(request.user)
        projects = dashboard.projects.all() if dashboard else []
        return render(request, 'main/profile.html', {'projects': projects})

    @action(detail=True, methods=['get'], url_path='user_profile')
    def user_profile(self, request, pk=None):
        # Get the user whose profile is being viewed
        profile_user = User.objects.get(id=pk)

        # Get that user's projects/dashboard
        dashboard = get_dashboard(profile_user)  # pass profile_user, not request.user
        projects = dashboard.projects.all() if dashboard else []

        return render(
            request,
            'main/user_profile.html',
            {
                'profile_user': profile_user,
                'projects': projects
            }
        )
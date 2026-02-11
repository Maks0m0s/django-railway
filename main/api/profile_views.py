from rest_framework import viewsets, permissions
from django.shortcuts import render
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework.response import Response


from main.services.dashboard_service import get_dashboard
from main.permissions import IsAuthenticatedOrRedirect

from main.services.profile_service import add_profile_link, delete_profile_link

class ProfileViewSet(viewsets.ViewSet):

    # default permission (fallback)
    permission_classes = [IsAuthenticatedOrRedirect]

    def get_permissions(self):
        # Make user_profile public
        if self.action == 'user_profile':
            return [permissions.AllowAny()]
        return [IsAuthenticatedOrRedirect()]

    def list(self, request):
        if not request.user.is_authenticated:
            return redirect("auth-login")
        # Only authenticated users can see their own profile
        links = request.user.profile_links.all()
        dashboard = get_dashboard(request.user)
        projects = dashboard.projects.all() if dashboard else []
        return render(request, 'main/profile.html', {'links':links, 'projects': projects})

    @action(detail=False, methods=['post'], url_path='add_profile_link')
    def add_profile_link(self, request):
        result = add_profile_link(request)
        if result['result']:
            self.list(request)
        return Response(
            {'error': result['error']},
            template_name="main/error.html",
            status=404
        )

    @action(detail=True, methods=['post'], url_path='delete_profile_link')
    def delete_profile_link(self, request, pk=None):
        result = delete_profile_link(pk)
        if result['result']:
            self.list(request)
        return Response(
            {'error': result['error']},
            template_name="main/error.html",
            status=404
        )

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
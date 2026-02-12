from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from django.contrib.auth.models import User
from main.services.dashboard_service import get_dashboard
from main.permissions import IsAuthenticatedOrRedirect

from main.services.profile_service import add_profile_link, delete_profile_link

from django.shortcuts import render, redirect, get_object_or_404


class ProfileViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticatedOrRedirect]

    def get_permissions(self):
        if self.action == 'user_profile':
            return [permissions.AllowAny()]
        return [IsAuthenticatedOrRedirect()]

    def list(self, request):
        links = request.user.profile_links.all()
        dashboard = get_dashboard(request.user)
        projects = dashboard.projects.all() if dashboard else []

        return render(request, 'main/profile.html', {
            'links': links,
            'projects': projects
        })

    @action(detail=False, methods=['post'], url_path='add_profile_link')
    def add_profile_link(self, request):
        result = add_profile_link(request)

        if result['result']:
            return redirect("profile")

        return render(
            request,
            "main/error.html",
            {"error": result["error"]},
            status=400
        )

    @action(detail=True, methods=['post'], url_path='delete_profile_link')
    def delete_profile_link(self, request, pk=None):
        result = delete_profile_link(pk)

        if result['result']:
            return redirect("profile")

        return render(
            request,
            "main/error.html",
            {"error": result["error"]},
            status=400
        )

    @action(detail=True, methods=['get'], url_path='user_profile')
    def user_profile(self, request, pk=None):
        profile_user = get_object_or_404(User, id=pk)

        dashboard = get_dashboard(profile_user)
        projects = dashboard.projects.all() if dashboard else []
        links = profile_user.profile_links.all()

        return render(
            request,
            'main/user_profile.html',
            {
                'profile_user': profile_user,
                'links':links,
                'projects': projects
            }
        )
from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.shortcuts import redirect

from main.services.dashboard_service import get_dashboard
from main.services.project_service import create_project, update_project, delete_project, get_project
from main.models import Dashboard

from main.permissions import IsAuthenticatedOrRedirect

class ProjectViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrRedirect]
    renderer_classes = [TemplateHTMLRenderer]

    def get_permissions(self):
        # Make user_profile public
        if self.action == 'user_project' or self.action == 'user_dashboard':
            return [permissions.AllowAny()]
        return [IsAuthenticatedOrRedirect()]

    # ===== PROJECT DASHBOARD =====
    def list(self, request):
        dashboard = Dashboard.objects.filter(user=request.user).first()
        return Response(
            {'dashboard': dashboard},
            template_name="main/dashboard.html"
        )

    # ===== PROJECT DETAILS =====
    def retrieve(self, request, pk=None):
        project = get_project(request.user, pk)
        if not project:
            return Response(
                {'error': 'Project not found'},
                template_name="main/error.html",
                status=404
            )

        return Response(
            {'project': project},
            template_name="main/project.html"
        )

    # ===== CREATE PROJECT =====
    @action(detail=False, methods=['get', 'post'], url_path='create')
    def create_project(self, request):
        if request.method == 'POST':
            result = create_project(request)

            if result['result']:
                return Response({'dashboard':result['dashboard']}, template_name="main/dashboard.html")

            return Response(
                {'error': result['error']},
                template_name="main/project_create.html"
            )

        return Response({}, template_name="main/project_create.html")

    # ===== UPDATE PROJECT =====
    @action(detail=True, methods=['get', 'post'], url_path='update')
    def update_project(self, request, pk=None):
        if request.method == 'POST':
            result = update_project(request, pk)

            if result['result']:
                return Response({'dashboard':result['dashboard']}, template_name="main/dashboard.html")

            return Response(
                {'error': result['error']},
                template_name="main/project_update.html"
            )

        project = get_project(request.user, pk)
        return Response(
            {'project': project},
            template_name="main/project_update.html"
        )

    # ===== DELETE PROJECT =====
    @action(detail=True, methods=['post'], url_path='delete')
    def delete_project(self, request, pk=None):
        result = delete_project(request, pk)

        if result['result']:
            return Response({'dashboard': result['dashboard']}, template_name="main/dashboard.html")

        return Response(
            {'error': result['error']},
            template_name="main/error.html"
        )

    @action(detail=True, methods=['get'], url_path='user_project')
    def user_project(self, request, user_id, pk=None):
        profile_user = User.objects.get(id=user_id)
        project = get_project(profile_user, pk)

        if project:
            return Response({'project':project, 'profile_user':profile_user}, template_name="main/user_project.html")

        return Response(
            {'error': 'Project not found'},
            template_name="main/error.html",
            status=404
        )

    @action(detail=True, methods=['get'], url_path='user_dashboard')
    def user_dashboard(self, request, pk=None):
        profile_user = User.objects.get(id=pk)
        dashboard = get_dashboard(profile_user)

        if dashboard:
            return Response({'dashboard': dashboard, 'profile_user': profile_user}, template_name="main/user_dashboard.html")

        return Response(
            {'error': 'Dashboard not found'},
            template_name="main/error.html",
            status=404
        )
from rest_framework import viewsets, permissions
from main.permissions import IsAuthenticatedOrRedirect
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import render

from main.services import settings_service, feedback_service

class SettingsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrRedirect]

    def list(self, request):
        settings = settings_service.get_settings(request)
        comments = feedback_service.get_comments(request)
        likes = feedback_service.get_likes(request)
        return render(request, 'main/settings.html', {'settings':settings, 'comment_history':comments, 'like_history':likes})

    def update(self, request):
        result = settings_service.update_settings(request)
        if result['result']:
            comments = feedback_service.get_comments(request)
            likes = feedback_service.get_likes(request)
            return render(request, 'main/settings.html', {'settings': result['settings'], 'comment_history':comments, 'like_history':likes})

        return render(
            request,
            "main/error.html",
            {"error": result["error"]},
            status=400
        )
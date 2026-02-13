from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from main.permissions import IsAuthenticatedOrRedirect
from main.services import settings_service, feedback_service


class SettingsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrRedirect]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "main/settings.html"

    def _get_context(self, user, settings=None):
        if not settings:
            settings = settings_service.get_settings(user)

        return {
            "settings": settings,
            "comment_history": feedback_service.get_comments(user),
            "like_history": feedback_service.get_likes(user),
        }

    def list(self, request):
        return Response(self._get_context(request.user))

    @action(detail=False, methods=["post"])
    def update_settings(self, request):
        result = settings_service.update_settings(request.user, request.data)

        if result["result"]:
            return Response(
                self._get_context(request.user, result["settings"])
            )

        return Response(
            {"error": result["error"]},
            template_name="main/error.html",
            status=400,
        )
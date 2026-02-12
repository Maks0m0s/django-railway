from rest_framework import viewsets, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action

from main.permissions import IsAuthenticatedOrRedirect
from main.services.feedback_service import add_project_comment, delete_project_comment, toggle_like


def render_feedback_response(result):
    """
    DRY helper for returning consistent feedback responses.
    """
    if result.get('result'):
        return Response(
            {'project': result.get('project'), 'profile_user': result.get('profile_user')},
            template_name="main/user_project.html"
        )

    return Response(
        {'error': result.get('error', 'Unknown error')},
        template_name="main/error.html",
        status=result.get('status', status.HTTP_400_BAD_REQUEST)
    )


class ProjectFeedbackViewSet(viewsets.ViewSet):
    """
    Handles project comments and likes.
    """
    permission_classes = [IsAuthenticatedOrRedirect]
    renderer_classes = [TemplateHTMLRenderer]

    @action(detail=True, methods=['post'], url_path='add_comment')
    def add_comment(self, request, user_id=None, pk=None):
        result = add_project_comment(request, user_id, pk)
        return render_feedback_response(result)

    @action(detail=True, methods=['post'], url_path='delete_comment')
    def delete_comment(self, request, user_id=None, project_id=None, pk=None):
        result = delete_project_comment(user_id, project_id, pk)
        return render_feedback_response(result)

    @action(detail=True, methods=['post'], url_path='toggle_like')
    def toggle_like(self, request, user_id=None, pk=None):
        result = toggle_like(request, user_id, pk)
        return render_feedback_response(result)
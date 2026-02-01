from rest_framework import viewsets, permissions
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.decorators import action

from main.services.feedback_service import add_project_comment, delete_project_comment, toggle_like
from main.permissions import IsAuthenticatedOrRedirect

class ProjectFeedbackViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrRedirect]
    renderer_classes = [TemplateHTMLRenderer]

    @action(detail=True, methods=['post'], url_path='add_comment')
    def add_comment(self, request, user_id=None, pk=None):
        result = add_project_comment(request, user_id, pk)
        if result['result']:
            return Response({'project':result['project'], 'profile_user':result['profile_user']}, template_name="main/user_project.html")

        return Response(
            {'error': f"{result['error']}"},
            template_name="main/error.html",
            status=404
        )

    @action(detail=True, methods=['post'], url_path='delete_comment')
    def delete_comment(self, request, user_id=None, project_id=None, pk=None):
        result = delete_project_comment(user_id, project_id, pk)
        if result['result']:
            return Response({'project':result['project'], 'profile_user':result['profile_user']}, template_name="main/user_project.html")

        return Response(
            {'error': f"{result['error']}"},
            template_name="main/error.html",
            status=404
        )

    @action(detail=True, methods=['post'], url_path='toggle_like')
    def toggle_like(self, request, user_id=None, pk=None):
        result = toggle_like(request, user_id, pk)
        if result['result']:
            return Response({'project':result['project'], 'profile_user':result['profile_user']}, template_name="main/user_project.html")
        return Response(
            {'error': f"{result['error']}"},
            template_name="main/error.html",
            status=404
        )

# class UserFeedbackViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticatedOrRedirect]
#     renderer_classes = [TemplateHTMLRenderer]
#
#     @action(detail=True, methods=['post'], url_path='add_comment')
#     def add_comment(self, request, user_id=None, pk=None):
#         result = add_user_comment(request, user_id, pk)
#         if result['result']:
#             return Response({'projects': result['projects'], 'profile_user': result['profile_user']},
#                             template_name="main/user_project.html")
#
#         return Response(
#             {'error': "Comment wasn't saved"},
#             template_name="main/error.html",
#             status=404
#         )
#
#     @action(detail=True, methods=['post'], url_path='delete_comment')
#     def delete_comment(self, request, user_id=None, project_id=None, pk=None):
#         result = delete_user_comment(request, user_id, project_id, pk)
#         if result['result']:
#             return Response({'projects': result['projects'], 'profile_user': result['profile_user']},
#                             template_name="main/user_project.html")
#
#         return Response(
#             {'error': "Comment wasn't deleted"},
#             template_name="main/error.html",
#             status=404
#         )
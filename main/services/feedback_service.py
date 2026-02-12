from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status

from main.models import Comment, Project
from main.services.project_service import get_project
from main.services.email_service import send_project_comment_email


def add_project_comment(request, user_id, pk):
    """
    Adds a comment to a project.
    """
    try:
        profile_user = User.objects.get(id=user_id)
        project = get_project(profile_user, pk)
    except User.DoesNotExist:
        return {'result': False, 'error': 'User not found', 'status': status.HTTP_404_NOT_FOUND}
    except Project.DoesNotExist:
        return {'result': False, 'error': 'Project not found', 'status': status.HTTP_404_NOT_FOUND}

    text = request.POST.get('text', '').strip()
    if not text:
        return {'result': False, 'error': 'Comment cannot be empty', 'status': status.HTTP_400_BAD_REQUEST}

    comment = Comment.objects.create(
        project=project,
        user=request.user,
        text=text
    )

    send_project_comment_email(profile_user, project, comment)

    return {'result': True, 'project': project, 'profile_user': profile_user}


def delete_project_comment(user_id, project_id, pk):
    """
    Deletes a comment from a project.
    """
    try:
        profile_user = User.objects.get(id=user_id)
        project = get_project(profile_user, project_id)
        comment = Comment.objects.get(id=pk)
    except User.DoesNotExist:
        return {'result': False, 'error': 'User not found', 'status': status.HTTP_404_NOT_FOUND}
    except Project.DoesNotExist:
        return {'result': False, 'error': 'Project not found', 'status': status.HTTP_404_NOT_FOUND}
    except Comment.DoesNotExist:
        return {'result': False, 'error': 'Comment not found', 'status': status.HTTP_404_NOT_FOUND}

    comment.delete()
    return {'result': True, 'project': project, 'profile_user': profile_user}


def toggle_like(request, user_id, pk):
    """
    Toggles like/unlike on a project by the requesting user.
    """
    try:
        profile_user = User.objects.get(id=user_id)
        project = Project.objects.get(id=pk)
    except User.DoesNotExist:
        return {'result': False, 'error': 'User not found', 'status': status.HTTP_404_NOT_FOUND}
    except Project.DoesNotExist:
        return {'result': False, 'error': 'Project not found', 'status': status.HTTP_404_NOT_FOUND}

    if request.user in project.likes.all():
        project.likes.remove(request.user)
    else:
        project.likes.add(request.user)

    return {'result': True, 'project': project, 'profile_user': profile_user}
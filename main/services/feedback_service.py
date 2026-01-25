from django.contrib.auth.models import User
from main.models import Comment
from main.services.project_service import get_project
from main.services.email_service import send_project_comment_email

def add_project_comment(request, user_id, pk):
    profile_user = User.objects.get(id=user_id)
    project = get_project(profile_user, pk)

    if not project:
        return {'result':False, 'error':'Project not found'}

    text = request.POST.get('text')

    if not text or not text.strip():
        return {'result': True, 'profile_user': profile_user, 'project': project}

    comment = Comment.objects.create(
        project=project,
        user=request.user,
        text=text
    )

    send_project_comment_email(profile_user, project, comment)

    return {'result':True, 'profile_user':profile_user, 'project':project}

def delete_project_comment(user_id, project_id, pk):
    profile_user = User.objects.get(id=user_id)
    project = get_project(profile_user, project_id)
    comment = Comment.objects.filter(id=pk)

    if not project:
        return {'result':False, 'error':'Project not found'}

    if not comment:
        return {'result': False, 'error':'Comment not found'}

    comment.delete()
    return {'result':True, 'profile_user':profile_user, 'project':project}

def add_user_comment(request, user_id, pk):
    return

def delete_user_comment(request, user_id, project_id, pk):
    return
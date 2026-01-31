from django.core.mail import send_mail
from django.conf import settings

def send_registration_email(user):
    if not settings.DEFAULT_FROM_EMAIL:
        print('No DEFAULT_FROM_EMAIL Set')
        return
    print(f"Sending registration email to {user.username}")

    subject = "Welcome to World Of Code!"
    message = f"""
    Hi {user.first_name or user.username},

    Your account has been successfully created!

    Username: {user.username}
    Email: {user.email}
    First Name: {user.first_name}
    Last Name : {user.last_name}

    Thank you for registering.
    """
    recipient = [user.email]

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient,
        fail_silently=False,
    )

def send_update_ac_email(user):
    if not settings.DEFAULT_FROM_EMAIL:
        print('No DEFAULT_FROM_EMAIL Set')
        return

    subject = "Your Account was Updated!"
    message = f"""
        Hi {user.first_name or user.username},

        Your account has been successfully updated!

        Your updated personal information:
        
        Username: {user.username}
        Email: {user.email}
        First Name: {user.first_name}
        Last Name : {user.last_name}

        Thank you for your time !
        """
    recipient = [user.email]

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient,
        fail_silently=True,
    )

def send_project_comment_email(user, project, comment):
    if not settings.DEFAULT_FROM_EMAIL:
        print('No DEFAULT_FROM_EMAIL Set')
        return

    subject = f"{project.name} was Commented!"
    message = f"""
            Hi {user.first_name or user.username},

            Your project called {project.name} has been just commented!

            New comment from {comment.user.username}:\n
            - {comment.text}\n
            \t\t({comment.created_at})
            
            Thank you for your time !
            """
    recipient = [user.email]

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient,
        fail_silently=True,
    )
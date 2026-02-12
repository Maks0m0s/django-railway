import textwrap
from django.core.mail import send_mail
from django.conf import settings

def send_registration_email(user):
    if not settings.DEFAULT_FROM_EMAIL:
        print("No DEFAULT_FROM_EMAIL set")
        return

    print(f"Sending registration email to {user.username} ({user.email})")

    subject = "Welcome to World Of Code!"
    message = textwrap.dedent(f"""
        Hi {user.first_name or user.username},

        Your account has been successfully created!

        Username: {user.username}
        Email: {user.email}
        First Name: {user.first_name}
        Last Name: {user.last_name}

        Thank you for registering.
    """)

    recipient = [user.email]

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient,
            fail_silently=True,  # will raise exception if fails
        )
        print("Registration email sent successfully!")
    except Exception as e:
        print("Error sending registration email:", e)


def send_update_ac_email(user):
    if not settings.DEFAULT_FROM_EMAIL:
        print("No DEFAULT_FROM_EMAIL set")
        return

    subject = "Your Account was Updated!"
    message = textwrap.dedent(f"""
        Hi {user.first_name or user.username},

        Your account has been successfully updated!

        Your updated personal information:

        Username: {user.username}
        Email: {user.email}
        First Name: {user.first_name}
        Last Name: {user.last_name}

        Thank you for your time!
    """)

    recipient = [user.email]

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient,
            fail_silently=True,
        )
        print("Account update email sent successfully!")
    except Exception as e:
        print("Error sending account update email:", e)


def send_project_comment_email(user, project, comment):
    if not settings.DEFAULT_FROM_EMAIL:
        print("No DEFAULT_FROM_EMAIL set")
        return

    subject = f"{project.name} was Commented!"
    message = textwrap.dedent(f"""
        Hi {user.first_name or user.username},

        Your project called '{project.name}' has just received a comment!

        New comment from {comment.user.username}:
        - {comment.text}
        ({comment.created_at})

        Thank you for your time!
    """)

    recipient = [user.email]

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient,
            fail_silently=True,
        )
        print("Project comment email sent successfully!")
    except Exception as e:
        print("Error sending project comment email:", e)
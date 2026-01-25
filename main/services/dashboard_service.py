from main.models import Dashboard

def create_dashboard(user):
    dashboard = Dashboard.objects.create(
        user=user,
    )
    dashboard.projects.set([])
    dashboard.save()
    return dashboard

def get_dashboard(user):
    dashboard = Dashboard.objects.filter(user=user).first()
    if dashboard:
        return dashboard
    else:
        return None

def delete_dashboard(user):
    dashboard = Dashboard.objects.filter(user=user)
    if dashboard:
        dashboard.delete()
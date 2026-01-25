from rest_framework.permissions import BasePermission

class IsAuthenticatedOrRedirect(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True

        # mark request so middleware can catch it
        request._redirect_to_login = True
        return False
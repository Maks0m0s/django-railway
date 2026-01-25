from django.shortcuts import redirect
from django.urls import reverse

class RedirectToLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if getattr(request, '_redirect_to_login', False):
            return redirect(reverse('auth-login'))

        return response

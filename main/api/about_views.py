from rest_framework import viewsets, permissions
from django.shortcuts import render

class AboutViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        return render(request, 'main/about.html', {})
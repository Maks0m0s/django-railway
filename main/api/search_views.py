from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

class SearchViewSet(viewsets.ViewSet):
    renderer_classes = [JSONRenderer]
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def search(self, request):
        q = request.GET.get('q', '').strip()

        if len(q) < 2:
            return Response({'results': []})

        users = User.objects.filter(username__icontains=q)[:10]

        return Response({
            'results': [
                {
                    'id': u.id,
                    'username': u.username,
                    'first_name': u.first_name,
                    'last_name': u.last_name,
                } for u in users
            ]
        })

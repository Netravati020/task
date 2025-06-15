
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.cache import cache
from .models import UserActivityLog
from .serializers import UserActivityLogSerializer, StatusUpdateSerializer

class UserActivityLogViewSet(viewsets.ModelViewSet):
    queryset = UserActivityLog.objects.all()
    serializer_class = UserActivityLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = UserActivityLog.objects.filter(user=self.request.user)
        action = self.request.query_params.get('action')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')

        if action:
            queryset = queryset.filter(action=action)
        if start and end:
            queryset = queryset.filter(timestamp__range=[start, end])
        return queryset

    def perform_create(self, serializer):
        instance = serializer.save(user=self.request.user)
        # Invalidate cache
        cache_key = f"user_activity_{self.request.user.id}"
        cache.delete(cache_key)

    def list(self, request, *args, **kwargs):
        cache_key = f"user_activity_{request.user.id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=60)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        log = self.get_object()
        serializer = StatusUpdateSerializer(log, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

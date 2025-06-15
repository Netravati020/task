from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserActivityLogViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register(r'logs', UserActivityLogViewSet, basename='logs')

urlpatterns = [
    path('', include(router.urls)),
]


schema_view = get_schema_view(
    openapi.Info(title="Activity API", default_version='v1'),
    public=True,
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

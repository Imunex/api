from rest_framework import routers
from api import views
from rest_framework import permissions
from django.urls import include, path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
schema_view = get_schema_view(
   openapi.Info(
      title="Imunex API",
      default_version='v1.0.0',
      description="Welcome to the API Documentation. Keep in mind that the endpoint of activate-device are only for clients with 2FA feature",
   ),
   public=False,
   permission_classes=[permissions.IsAuthenticated]
)


urlpatterns = [
   #  path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include(router.urls)),
    path('fingerprint', views.UserViewSet.as_view({'post': 'create'}), name='login-fingerprint'),
]

from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


# Create the schema view for swagger
schema_view = get_schema_view(
    openapi.Info(
        title="URL Shortener API",
        default_version='v1',
        description="API for shortening URLs and retrieving original URLs",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui(
         'swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('', include('urlshortener.urls')),


]

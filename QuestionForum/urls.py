"""QuestionForum URL Configuration"""

from django.contrib import admin
from django.urls import path, include

from django_registration.backends.one_step.views import RegistrationView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url


schema_view_swagger = get_schema_view(
    openapi.Info(
        title="QuestionForum API",
        default_version='v1',
        description="These are the API Endpoints for QuestionForum which can be used to add Questions and Answers regarding them.",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kuckianchetan98@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

schema_view_redoc = get_schema_view(
    openapi.Info(
        title="QuestionForum API",
        default_version='v1',
        description="These are the API Endpoints for QuestionForum which can be used to add Questions and Answers regarding them.\n Swagger Endpoint: http://3.131.97.125:8000/swagger/",
        # terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kuckianchetan98@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path("api/", include("users.api.urls")),

    path("api/", include("questions.api.urls")),

    path("api-auth/", include("rest_framework.urls")),
    path("api/rest-auth/", include("rest_auth.urls")),
    path("api/rest-auth/registration/",
         include("rest_auth.registration.urls")),
         
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view_swagger.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view_swagger.with_ui('swagger',
                                                   cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view_redoc.with_ui('redoc',
                                               cache_timeout=0), name='schema-redoc'),
]

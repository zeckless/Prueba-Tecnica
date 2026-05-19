from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("community.urls")),
    path("api/biblioteca/", include("biblioteca.urls")),
]

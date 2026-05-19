from django.urls import path

from . import views


urlpatterns = [
    path("health/", views.health),
    path("overview/", views.overview),
    path("prompts/", views.prompts),
    path("resources/", views.resources),
    path("discussions/", views.discussions),
]

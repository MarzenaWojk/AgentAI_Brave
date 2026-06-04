from django.urls import path

from .views import healthcheck, homepage

urlpatterns = [
    path("", homepage, name="homepage"),
    path("health/", healthcheck, name="healthcheck"),
]
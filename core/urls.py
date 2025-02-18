from django.urls import path

from .views import home, about, service

app_name = "core"
urlpatterns = [
    path("", home, name="home"),
    path(
        "about/",
        about,
        name="about",
    ),
    path("service/", service, name="service"),
]

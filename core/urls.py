from django.urls import path
from django.views.generic import TemplateView

from .views import home, about

app_name = "core"
urlpatterns = [
    path("", home, name="home"),
    path(
        "about/",
        about,
        name="about",
    ),
    path(
        "service/",
        TemplateView.as_view(template_name="core/service.html"),
        name="service",
    ),
]

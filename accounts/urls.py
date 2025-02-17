from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    register,
    TeacherList,
    TeacherDetail,
    SecretaryList,
    SecretaryDetail,
    MeView,
    CustomTokenBlacklistView,
)

app_name = "accounts"
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh", TokenRefreshView.as_view(), name="refresh"),
    path("logout", CustomTokenBlacklistView.as_view(), name="logout"),
    path("me", MeView.as_view(), name="me"),
    # URLs para Professores
    path("professores/", TeacherList.as_view(), name="teacher_list"),
    path("professores/<int:pk>/", TeacherDetail.as_view(), name="teacher_detail"),
    # URLs para Secretários
    path("secretarios/", SecretaryList.as_view(), name="secretary_list"),
    path("secretarios/<int:pk>/", SecretaryDetail.as_view(), name="secretary_detail"),
]

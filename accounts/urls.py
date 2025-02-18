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
    login_view,
    logout_view,
)

app_name = "accounts"
urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),  # Novo login
    path("logout/", logout_view, name="logout"),  # Novo logout
    path("token/", TokenObtainPairView.as_view(), name="token"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("blacklist/", CustomTokenBlacklistView.as_view(), name="blacklist"),
    path("me/", MeView.as_view(), name="me"),
    # URLs para Professores
    path("professores/", TeacherList.as_view(), name="teacher_list"),
    path("professores/<int:pk>/", TeacherDetail.as_view(), name="teacher_detail"),
    # URLs para Secretários
    path("secretarios/", SecretaryList.as_view(), name="secretary_list"),
    path("secretarios/<int:pk>/", SecretaryDetail.as_view(), name="secretary_detail"),
]
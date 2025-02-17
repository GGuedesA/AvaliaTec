from django.shortcuts import render, redirect
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from .forms import RegisterForm
from .models import Usuario
from .serializers import UsuarioSerializer
from .permissions import UsuarioPermission


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("admin:login")
    return render(request, "accounts/register.html", {"form": form})


# ==================== Listagem de Professores ===============
class TeacherList(APIView):
    permission_classes = [UsuarioPermission]

    def get(self, request):
        """Retorna uma lista de professores filtrados pelo nome."""
        q = request.query_params.get("search", "")
        teachers = Usuario.objects.filter(
            role=Usuario.RoleChoices.TEACHER, name__icontains=q
        )
        serializer = UsuarioSerializer(teachers, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Cria um novo professor."""
        data = request.data.copy()
        data["role"] = Usuario.RoleChoices.TEACHER  # Define o papel como professor
        serializer = UsuarioSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                return Response(
                    {"detail": "Usuário com este CPF já existe."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"detail": "Erro ao processar a solicitação."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request):
        """Atualiza os dados do professor logado."""
        if request.user.role != Usuario.RoleChoices.TEACHER:
            return Response(
                {"detail": "Acesso negado."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = UsuarioSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        """Remove o professor logado."""
        if request.user.role != Usuario.RoleChoices.TEACHER:
            return Response(
                {"detail": "Acesso negado."}, status=status.HTTP_403_FORBIDDEN
            )

        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherDetail(APIView):
    def get(self, request, pk):
        """Retorna os detalhes de um professor."""
        teacher = get_object_or_404(Usuario, pk=pk, role=Usuario.RoleChoices.TEACHER)
        serializer = UsuarioSerializer(teacher)
        return Response(serializer.data)


# ==================== Listagem de Secretários ===============
class SecretaryList(APIView):
    permission_classes = [UsuarioPermission]

    def get(self, request):
        """Retorna uma lista de secretários filtrados pelo nome."""
        q = request.query_params.get("search", "")
        secretaries = Usuario.objects.filter(
            role=Usuario.RoleChoices.SECRETARY, name__icontains=q
        )
        serializer = UsuarioSerializer(secretaries, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Cria um novo secretário."""
        data = request.data.copy()
        data["role"] = Usuario.RoleChoices.SECRETARY  # Define o papel como secretário
        serializer = UsuarioSerializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                return Response(
                    {"detail": "Usuário com este CPF já existe."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"detail": "Erro ao processar a solicitação."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def put(self, request):
        """Atualiza os dados do secretário logado."""
        if request.user.role != Usuario.RoleChoices.SECRETARY:
            return Response(
                {"detail": "Acesso negado."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = UsuarioSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        """Remove o secretário logado."""
        if request.user.role != Usuario.RoleChoices.SECRETARY:
            return Response(
                {"detail": "Acesso negado."}, status=status.HTTP_403_FORBIDDEN
            )

        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SecretaryDetail(APIView):
    def get(self, request, pk):
        """Retorna os detalhes de um secretário."""
        secretary = get_object_or_404(
            Usuario, pk=pk, role=Usuario.RoleChoices.SECRETARY
        )
        serializer = UsuarioSerializer(secretary)
        return Response(serializer.data)


class MeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print(f"User type: {type(request.user)}")  # Para verificar o tipo
        print(f"User: {request.user}")  # Para verificar os dados do usuário

        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)


class CustomTokenBlacklistView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return Response(status=status.HTTP_205_RESET_CONTENT)

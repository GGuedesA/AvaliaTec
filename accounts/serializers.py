from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenBlacklistSerializer,
)
from django.contrib.auth.hashers import make_password
from .models import Usuario
from administrative.models import Coordination  # Importando Coordination corretamente


class UsuarioSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(
        required=True, min_length=3, max_length=100, source="name"
    )
    cpf = serializers.CharField(required=True, min_length=11, max_length=11)
    role = serializers.ChoiceField(choices=Usuario.RoleChoices.choices, required=True)
    password_confirmation = serializers.CharField(write_only=True)

    # Campo opcional, obrigatório apenas se role="secretary"
    fk_coordination = serializers.PrimaryKeyRelatedField(
        queryset=Coordination.objects.all(), required=False
    )

    class Meta:
        model = Usuario
        fields = (
            "id",
            "nome",
            "email",
            "cpf",
            "role",
            "fk_coordination",
            "created_at",
            "updated_at",
            "password",
            "password_confirmation",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

    def validate(self, data):
        """Valida se as senhas conferem e se um secretário tem coordenação."""
        if data.get("password") != data.get("password_confirmation"):
            raise serializers.ValidationError(
                {"password_confirmation": "As senhas não são iguais."}
            )

        # Se o usuário for secretário, a coordenação é obrigatória
        if (
            data.get("role") == Usuario.RoleChoices.SECRETARY
            and "fk_coordination" not in data
        ):
            raise serializers.ValidationError(
                {
                    "fk_coordination": "Secretários devem estar vinculados a uma coordenação."
                }
            )

        return data

    def create(self, validated_data):
        """Cria um usuário, garantindo que a senha esteja criptografada."""
        validated_data.pop("password_confirmation")  # Remover campo auxiliar
        validated_data["password"] = make_password(validated_data["password"])

        user = super().create(validated_data)

        # Se for admin, configuramos o superusuário
        if user.role == Usuario.RoleChoices.ADMIN:
            user.is_superuser = True
            user.is_staff = True
            user.save()

        return user

    def update(self, instance, validated_data):
        """Atualiza o usuário, garantindo criptografia de senha se alterada."""
        validated_data.pop("password_confirmation", None)  # Remover campo auxiliar

        if "password" in validated_data:
            instance.password = make_password(validated_data.pop("password"))

        return super().update(instance, validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["token"] = data.pop("access")
        data["refresh_token"] = data.pop("refresh")
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh_token = serializers.CharField(required=True)
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = attrs.pop("refresh_token")
        data = super().validate(attrs)
        data["token"] = data.pop("access")
        data["refresh_token"] = data.pop("refresh")
        return data


class CustomTokenBlacklistSerializer(TokenBlacklistSerializer):
    refresh_token = serializers.CharField(required=True)
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = attrs.pop("refresh_token")
        return super().validate(attrs)

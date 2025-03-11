from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager


class Usuario(AbstractBaseUser, PermissionsMixin):
    class RoleChoices(models.TextChoices):
        ADMIN = "admin", "Administrador"
        TEACHER = "teacher", "Teacher"
        SECRETARY = "secretary", "Secretary"

    name = models.CharField(max_length=100, blank=True, null=True)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True, max_length=255)

    role = models.CharField(
        max_length=50, choices=RoleChoices.choices, default=RoleChoices.ADMIN
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        "auth.Group", related_name="usuario_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="usuario_permissions", blank=True
    )

    fk_coordination = models.ForeignKey(
        "administrative.Coordination",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="secretarios",
    )

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.role == self.RoleChoices.ADMIN:
            self.is_superuser = True
            self.is_staff = True

            # Gerar nome de usuário baseado no campo "name"
            if self.name:
                name_parts = self.name.split()
                if len(name_parts) >= 2:
                    username = f"{name_parts[0]}.{name_parts[1]}"
                else:
                    username = name_parts[0]
                # Garantindo que não haja espaços e tudo em minúsculas
                self.username = username.lower()
            else:
                self.username = self.cpf  # Default to CPF if name is not provided

        super().save(*args, **kwargs)

    def get_full_name(self):
        return self.name

    def __str__(self):
        return f"{self.cpf} ({self.get_role_display()})"
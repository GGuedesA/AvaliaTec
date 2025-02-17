from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, cpf, email, password=None, **extra_fields):
        """Cria e retorna um usuário normal."""
        if not cpf:
            raise ValueError("O campo CPF é obrigatório.")
        if not email:
            raise ValueError("O campo Email é obrigatório.")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        """Cria e retorna um superusuário (admin)."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuário deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuário deve ter is_superuser=True.")

        return self.create_user(cpf, email, password, **extra_fields)

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, cpf, email, password=None, **extra_fields):
        """Cria e retorna um usuário normal."""
        if not cpf:
            raise ValueError("O CPF deve ser fornecido")
        if not email:
            raise ValueError("O email deve ser fornecido")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('name', 'Admin')  # Provide a default name

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(cpf, email, password, **extra_fields)

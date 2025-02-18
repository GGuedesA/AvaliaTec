from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    cpf = forms.CharField(required=True)
    name = forms.CharField(required=True)

    role = forms.ChoiceField(
        choices=Usuario.RoleChoices.choices,  # Adicionando o campo para escolher o tipo de usuário
        required=True,
        label="Tipo de Usuário",
    )

    class Meta:
        model = Usuario
        fields = ("name", "cpf", "email", "role", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Um usuario com este email ja existe")
        return email

    def clean_cpf(self):
        cpf = self.cleaned_data["cpf"]
        if Usuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Um usuario com este cpf ja existe")
        return cpf


class LoginForm(forms.Form):
    cpf = forms.CharField(required=True, label="CPF")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Senha")

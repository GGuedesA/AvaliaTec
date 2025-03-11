from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from administrative.models import Coordination


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    cpf = forms.CharField(required=True)
    name = forms.CharField(required=True)

    role = forms.ChoiceField(
        choices=Usuario.RoleChoices.choices,  # Adicionando o campo para escolher o tipo de usuário
        required=True,
        label="Tipo de Usuário",
    )

    fk_coordination = forms.ModelChoiceField(
        queryset=Coordination.objects.all(),
        required=False,
        label="Coordenação",
    )

    class Meta:
        model = Usuario
        fields = (
            "name",
            "cpf",
            "email",
            "role",
            "fk_coordination",
            "password1",
            "password2",
        )

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

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        fk_coordination = cleaned_data.get("fk_coordination")

        if role == "secretary" and not fk_coordination:
            self.add_error(
                "fk_coordination", "Coordenação é obrigatória para secretários."
            )


class LoginForm(forms.Form):
    cpf = forms.CharField(required=True, label="CPF")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Senha")

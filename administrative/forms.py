from django import forms
from django.core.exceptions import ValidationError
from .models import Block, Coordination, Room, Banca, AgendamentoSala


class BlockForm(forms.ModelForm):
    class Meta:
        model = Block
        fields = ["name"]


class CoordinationForm(forms.ModelForm):
    class Meta:
        model = Coordination
        fields = ["name", "blocks"]


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "block"]


class BancaForm(forms.ModelForm):
    class Meta:
        model = Banca
        fields = [
            "tipo",  # Mova "tipo" para o início
            "orientador",
            "co_orientador",
            "professores_banca",
            "presidente",  # Adicione o campo presidente
            "sala",
            "alunos_nomes",
            "tema",
            "data",
            "horario_inicio",
            "horario_fim",
            "status",
            "coordination",
        ]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
            "horario_inicio": forms.TimeInput(attrs={"type": "time"}),
            "horario_fim": forms.TimeInput(attrs={"type": "time"}),
        }
    def clean(self):
        cleaned_data = super().clean()
        sala = cleaned_data.get("sala")
        data = cleaned_data.get("data")
        horario_inicio = cleaned_data.get("horario_inicio")
        horario_fim = cleaned_data.get("horario_fim")

        # Ignorar validação de conflito se for a mesma banca
        if self.instance.pk:
            bancas_conflitantes = Banca.objects.filter(
                sala=sala,
                data=data,
            ).exclude(pk=self.instance.pk)
        else:
            bancas_conflitantes = Banca.objects.filter(
                sala=sala,
                data=data,
            )

        if bancas_conflitantes.exists():
            raise ValidationError("Já existe uma banca agendada para esta sala nesta data.")

        return cleaned_data


class AgendamentoSalaForm(forms.ModelForm):
    class Meta:
        model = AgendamentoSala
        fields = [
            "professor",
            "sala",
            "materia",
            "data",
            "horario_inicio",
            "horario_fim",
        ]

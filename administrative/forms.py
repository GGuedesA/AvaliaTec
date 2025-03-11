from django import forms
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
            "orientador",
            "co_orientador",
            "professores_banca",
            "sala",
            "alunos_nomes",
            "tema",
            "tipo",
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

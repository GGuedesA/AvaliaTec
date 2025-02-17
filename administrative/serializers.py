from rest_framework import serializers
from datetime import datetime
from accounts.models import Usuario
from administrative.models import Banca, Coordination, Room, AgendamentoSala


class BancaSerializer(serializers.ModelSerializer):
    fk_professores_banca = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(role=Usuario.RoleChoices.TEACHER),
        required=False,
    )
    fk_coordination = serializers.PrimaryKeyRelatedField(
        queryset=Coordination.objects.all(),
        required=True,  # Agora é obrigatório
    )
    fk_sala = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), required=False
    )
    alunos_nomes = serializers.CharField(required=False)
    tema = serializers.CharField(required=False)
    tipo_banca = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    data_aula = serializers.DateField(required=False)
    horario_inicio = serializers.TimeField(required=False)
    horario_fim = serializers.TimeField(required=False)

    class Meta:
        model = Banca
        fields = [
            "id",
            "fk_orientador",
            "fk_professores_banca",
            "fk_co_orientadores",
            "fk_sala",
            "alunos_nomes",
            "tema",
            "tipo_banca",
            "fk_coordination",  # Apenas a coordenação é referenciada
            "status",
            "data_aula",
            "horario_inicio",
            "horario_fim",
        ]

    def validate_fk_professores_banca(self, value):
        if len(value) < 2 or len(value) > 3:
            raise serializers.ValidationError(
                "O número de professores da banca deve ser entre 2 e 3."
            )
        return value

    def validate_alunos_nomes(self, value):
        nomes = value.split(",")
        if len(nomes) < 1 or len(nomes) > 5:
            raise serializers.ValidationError(
                "O número de alunos deve ser entre 1 e 5."
            )
        return value

    def validate(self, data):
        """Validação personalizada para garantir que não haja conflitos de agendamento de sala"""
        fk_sala = data.get("fk_sala")
        data_aula = data.get("data_aula")
        horario_inicio = data.get("horario_inicio")
        horario_fim = data.get("horario_fim")

        # Verificar se a sala está ocupada
        conflicting_bancas = Banca.objects.filter(
            fk_sala=fk_sala,
            data_aula=data_aula,
        ).exclude(id=self.instance.id if self.instance else None)

        for banca in conflicting_bancas:
            existing_start = datetime.combine(banca.data_aula, banca.horario_inicio)
            existing_end = datetime.combine(banca.data_aula, banca.horario_fim)
            new_start = datetime.combine(data_aula, horario_inicio)
            new_end = datetime.combine(data_aula, horario_fim)

            # Verifica se os horários se sobrepõem
            if new_start < existing_end and new_end > existing_start:
                raise serializers.ValidationError(
                    f"A sala '{fk_sala}' já está ocupada no horário solicitado."
                )

        return data


class AgendamentoSalaSerializer(serializers.ModelSerializer):
    professor = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(role=Usuario.RoleChoices.TEACHER), required=True
    )
    sala = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), required=True
    )
    materia = serializers.CharField(required=True)
    data = serializers.DateField(required=True)
    horario_inicio = serializers.TimeField(required=True)
    horario_fim = serializers.TimeField(required=True)
    status = serializers.ChoiceField(
        choices=AgendamentoSala.StatusAgendamento.choices, required=False
    )

    class Meta:
        model = AgendamentoSala
        fields = [
            "id",
            "professor",
            "sala",
            "materia",
            "data",
            "horario_inicio",
            "horario_fim",
            "status",
        ]

    def validate(self, data):
        """Validação personalizada para garantir que não haja conflitos de agendamento de sala"""
        sala = data.get("sala")
        data_aula = data.get("data")
        horario_inicio = data.get("horario_inicio")
        horario_fim = data.get("horario_fim")

        # Verificar se a sala está ocupada
        conflitos = AgendamentoSala.objects.filter(
            sala=sala,
            data=data_aula,
        ).exclude(id=self.instance.id if self.instance else None)

        for agendamento in conflitos:
            existing_start = datetime.combine(
                agendamento.data, agendamento.horario_inicio
            )
            existing_end = datetime.combine(agendamento.data, agendamento.horario_fim)
            new_start = datetime.combine(data_aula, horario_inicio)
            new_end = datetime.combine(data_aula, horario_fim)

            # Verifica se os horários se sobrepõem
            if new_start < existing_end and new_end > existing_start:
                raise serializers.ValidationError(
                    f"A sala '{sala}' já está ocupada no horário solicitado."
                )

        return data

    def validate_professor(self, value):
        """Valida se o professor selecionado é realmente um 'teacher'"""
        if value.role != Usuario.RoleChoices.TEACHER:
            raise serializers.ValidationError("O usuário não é um professor.")
        return value

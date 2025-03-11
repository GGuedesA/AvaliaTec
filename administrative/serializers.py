from rest_framework import serializers
from datetime import datetime
from accounts.models import Usuario
from administrative.models import Banca, Coordination, Room, AgendamentoSala, Block


class BancaSerializer(serializers.ModelSerializer):
    orientador = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(role=Usuario.RoleChoices.TEACHER)
    )
    co_orientador = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(role=Usuario.RoleChoices.TEACHER),
        allow_null=True,
        required=False,
    )
    professores_banca = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(role=Usuario.RoleChoices.TEACHER),
        many=True,
    )

    sala = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    sala_detalhes = serializers.SerializerMethodField()

    tipo = serializers.ChoiceField(choices=Banca.TipoBanca.choices)
    tipo_label = serializers.SerializerMethodField()

    coordination = serializers.PrimaryKeyRelatedField(
        queryset=Coordination.objects.all()
    )
    coordination_detalhes = serializers.SerializerMethodField()

    block = serializers.PrimaryKeyRelatedField(queryset=Block.objects.all())
    block_detalhes = serializers.SerializerMethodField()

    class Meta:
        model = Banca
        fields = [
            "id",
            "orientador",
            "co_orientador",
            "professores_banca",
            "sala",
            "sala_detalhes",
            "alunos_nomes",
            "tema",
            "tipo",
            "tipo_label",
            "coordination",
            "coordination_detalhes",
            "status",
            "data",
            "horario_inicio",
            "horario_fim",
            "block",
            "block_detalhes",
        ]

    def get_sala_detalhes(self, obj):
        """Retorna detalhes da sala para facilitar a exibição"""
        return (
            {
                "id": obj.sala.id,
                "name": obj.sala.name,
                "block": obj.sala.block.name,
            }
            if obj.sala
            else None
        )

    def get_tipo_label(self, obj):
        """Retorna a representação legível do tipo"""
        return obj.get_tipo_display() if obj.tipo else None

    def get_coordination_detalhes(self, obj):
        """Retorna detalhes da coordenação"""
        return (
            {
                "id": obj.coordination.id,
                "name": obj.coordination.name,
            }
            if obj.coordination
            else None
        )

    def get_block_detalhes(self, obj):
        """Retorna detalhes do bloco"""
        return (
            {
                "id": obj.block.id,
                "name": obj.block.name,
            }
            if obj.block
            else None
        )


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


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = ["id", "name"]


class CoordinationSerializer(serializers.ModelSerializer):
    blocks = BlockSerializer(many=True)  # Relacionamento ManyToMany com Block

    class Meta:
        model = Coordination
        fields = ["id", "name", "blocks"]


class RoomSerializer(serializers.ModelSerializer):
    block = BlockSerializer()  # Relacionamento ForeignKey com Block

    class Meta:
        model = Room
        fields = ["id", "name", "block"]

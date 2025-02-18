from django.db import models
from accounts.models import Usuario
from django.core.exceptions import ValidationError


class Block(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Coordination(models.Model):
    name = models.CharField(max_length=100, unique=True)
    blocks = models.ManyToManyField(Block, related_name="coordinations")

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=50, unique=True)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name="rooms")

    def __str__(self):
        return f"{self.name} ({self.block.name})"


class Banca(models.Model):
    class TipoBanca(models.TextChoices):
        ESTAGIO = "estagio", "Estágio"
        TCC = "tcc", "TCC"

    class StatusBanca(models.TextChoices):
        ANALISE = "analise", "Em Análise"
        ACEITA = "aceita", "Aceita"
        ANDAMENTO = "andamento", "Em Andamento"
        FINALIZADA = "finalizada", "Finalizada"

    orientador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="bancas_orientador",
        limit_choices_to={"role": Usuario.RoleChoices.TEACHER},
    )
    co_orientador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bancas_co_orientador",
        limit_choices_to={"role": Usuario.RoleChoices.TEACHER},
    )
    professores_banca = models.ManyToManyField(
        Usuario,
        related_name="bancas_professores",
        limit_choices_to={"role": Usuario.RoleChoices.TEACHER},
    )
    sala = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="bancas")
    alunos_nomes = models.TextField(
        help_text="Insira os nomes dos alunos, separados por vírgula."
    )
    tema = models.CharField(max_length=255)
    tipo = models.CharField(max_length=10, choices=TipoBanca.choices)
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    status = models.CharField(
        max_length=10, choices=StatusBanca.choices, default=StatusBanca.ANALISE
    )
    coordination = models.ForeignKey(Coordination, on_delete=models.CASCADE)

    def clean(self):
        from datetime import datetime

        data_inicio = datetime.combine(self.data, self.horario_inicio)
        data_fim = datetime.combine(self.data, self.horario_fim)

        conflitos = Banca.objects.filter(sala=self.sala, data=self.data).exclude(
            id=self.id
        )

        for banca in conflitos:
            existing_start = datetime.combine(banca.data, banca.horario_inicio)
            existing_end = datetime.combine(banca.data, banca.horario_fim)
            if data_inicio < existing_end and data_fim > existing_start:
                raise ValidationError("A sala já está ocupada neste horário.")

    def __str__(self):
        return f"{self.tema} - {self.get_tipo_display()}"

class AgendamentoSala(models.Model):
    class StatusAgendamento(models.TextChoices):
        ANALISE = "analise", "Em Análise"
        CONFIRMADO = "confirmado", "Confirmado"
        ANDAMENTO = "andamento", "Em Andamento"
        FINALIZADA = "finalizada", "Finalizada"

    professor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="agendamentos",
        limit_choices_to={"role": Usuario.RoleChoices.TEACHER},
    )
    sala = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name="agendamentos"
    )
    materia = models.CharField(max_length=100)
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    status = models.CharField(
        max_length=10,
        choices=StatusAgendamento.choices,
        default=StatusAgendamento.ANALISE,
    )

    def clean(self):
        from django.core.exceptions import ValidationError
        from datetime import datetime

        data_inicio = datetime.combine(self.data, self.horario_inicio)
        data_fim = datetime.combine(self.data, self.horario_fim)

        conflitos = AgendamentoSala.objects.filter(
            sala=self.sala, data=self.data
        ).exclude(id=self.id)

        for agendamento in conflitos:
            existing_start = datetime.combine(
                agendamento.data, agendamento.horario_inicio
            )
            existing_end = datetime.combine(agendamento.data, agendamento.horario_fim)
            if data_inicio < existing_end and data_fim > existing_start:
                raise ValidationError("A sala já está ocupada neste horário.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Aula de {self.materia} - {self.professor.name}"

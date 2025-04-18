# Generated by Django 5.1.6 on 2025-02-18 05:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administrative", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="block",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="coordination",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name="Room",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "block",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rooms",
                        to="administrative.block",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Banca",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "alunos_nomes",
                    models.TextField(
                        help_text="Insira os nomes dos alunos, separados por vírgula."
                    ),
                ),
                ("tema", models.CharField(max_length=255)),
                (
                    "tipo",
                    models.CharField(
                        choices=[("estagio", "Estágio"), ("tcc", "TCC")], max_length=10
                    ),
                ),
                ("data", models.DateField()),
                ("horario_inicio", models.TimeField()),
                ("horario_fim", models.TimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("analise", "Em Análise"),
                            ("aceita", "Aceita"),
                            ("andamento", "Em Andamento"),
                            ("finalizada", "Finalizada"),
                        ],
                        default="analise",
                        max_length=10,
                    ),
                ),
                (
                    "co_orientador",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={"role": "teacher"},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="bancas_co_orientador",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "coordination",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="administrative.coordination",
                    ),
                ),
                (
                    "orientador",
                    models.ForeignKey(
                        limit_choices_to={"role": "teacher"},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bancas_orientador",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "professores_banca",
                    models.ManyToManyField(
                        help_text="Deve haver entre 3 e 5 professores na banca.",
                        limit_choices_to={"role": "teacher"},
                        related_name="bancas_professores",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sala",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bancas",
                        to="administrative.room",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AgendamentoSala",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("materia", models.CharField(max_length=100)),
                ("data", models.DateField()),
                ("horario_inicio", models.TimeField()),
                ("horario_fim", models.TimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("analise", "Em Análise"),
                            ("confirmado", "Confirmado"),
                            ("andamento", "Em Andamento"),
                            ("finalizada", "Finalizada"),
                        ],
                        default="analise",
                        max_length=10,
                    ),
                ),
                (
                    "professor",
                    models.ForeignKey(
                        limit_choices_to={"role": "teacher"},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="agendamentos",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "sala",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="agendamentos",
                        to="administrative.room",
                    ),
                ),
            ],
        ),
    ]

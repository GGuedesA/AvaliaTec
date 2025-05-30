# Generated by Django 5.1.6 on 2025-03-11 07:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administrative", "0003_alter_banca_professores_banca"),
    ]

    operations = [
        migrations.AddField(
            model_name="banca",
            name="block",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bancas",
                to="administrative.block",
            ),
            preserve_default=False,
        ),
    ]

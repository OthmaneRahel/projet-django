# Generated by Django 5.2 on 2025-05-04 17:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPatient', '0009_messages_secretaire_medecin_vu_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages_secretaire_medecin',
            name='destination',
            field=models.CharField(default=False, max_length=30),
        ),
        migrations.AddField(
            model_name='messages_secretaire_medecin',
            name='source',
            field=models.CharField(default=False, max_length=30),
        ),
        migrations.AlterField(
            model_name='messages_secretaire_medecin',
            name='date_denvoi',
            field=models.DateField(default=datetime.datetime(2025, 5, 4, 17, 5, 32, 990336, tzinfo=datetime.timezone.utc)),
        ),
    ]

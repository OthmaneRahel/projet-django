# Generated by Django 5.2 on 2025-05-05 20:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPatient', '0013_alter_messages_secretaire_medecin_date_denvoi_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facture',
            name='note_supplemtaire',
            field=models.TextField(default=False, max_length=150),
        ),
        migrations.AlterField(
            model_name='facture',
            name='dateFacture',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 5, 20, 25, 49, 812894, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='messages_secretaire_medecin',
            name='date_denvoi',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 5, 20, 25, 49, 815055, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='rapportmedicalpatient',
            name='date_rapport',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 5, 20, 25, 49, 815510, tzinfo=datetime.timezone.utc)),
        ),
    ]

# Generated by Django 5.2 on 2025-05-06 15:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionPatient', '0018_facture_rendezvous_rapportmedicalpatient_rendezvous_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrateur',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='admin/'),
        ),
        migrations.AlterField(
            model_name='facture',
            name='dateFacture',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 6, 15, 51, 3, 73600, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='medecin',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='medecin/'),
        ),
        migrations.AlterField(
            model_name='messages_secretaire_medecin',
            name='date_denvoi',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 6, 15, 51, 3, 78286, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='patient',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='patient/'),
        ),
        migrations.AlterField(
            model_name='rapportmedicalpatient',
            name='date_rapport',
            field=models.DateTimeField(default=datetime.datetime(2025, 5, 6, 15, 51, 3, 79760, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='secretaire',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='secretaire/'),
        ),
    ]

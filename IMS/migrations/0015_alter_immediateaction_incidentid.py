# Generated by Django 5.1.5 on 2025-06-04 06:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0014_remove_incident_ticket_immediateactions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='immediateaction',
            name='incidentid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ImmediateActions', to='IMS.incident_ticket'),
        ),
    ]

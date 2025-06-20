# Generated by Django 5.1.5 on 2025-06-04 10:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0018_alter_incident_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident_ticket',
            name='Status',
            field=models.ManyToManyField(null=True, related_name='TicketStatus', through='IMS.StatusTime', to='IMS.status'),
        ),
        migrations.AlterField(
            model_name='statustime',
            name='Statusid',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='IMS.status'),
        ),
    ]

# Generated by Django 5.1.5 on 2025-05-28 09:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('IMS', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='Role',
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]

# Generated by Django 4.2 on 2023-10-18 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('businessApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timecard',
            name='work_time',
            field=models.FloatField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.0.8 on 2024-08-07 07:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("collectors", "0008_alter_source_url"),
        ("django_celery_beat", "0018_improve_crontab_helptext"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="source",
            name="periodicity",
        ),
        migrations.RemoveField(
            model_name="source",
            name="periodicity_value",
        ),
        migrations.AddField(
            model_name="source",
            name="task",
            field=models.ForeignKey(
                blank=True,
                help_text="Celery periodic task",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="django_celery_beat.periodictask",
            ),
        ),
        migrations.AlterField(
            model_name="accesskey",
            name="key",
            field=models.CharField(help_text="Key name", max_length=100),
        ),
        migrations.AlterField(
            model_name="accesskey",
            name="value",
            field=models.CharField(help_text="Key value", max_length=100),
        ),
    ]

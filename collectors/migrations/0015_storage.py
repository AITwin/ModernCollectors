# Generated by Django 5.0.8 on 2024-08-07 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("collectors", "0014_remove_source_periodicity_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Storage",
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
                    "provider",
                    models.CharField(
                        choices=[("AZURE", "Azure"), ("GOOGLE", "Google")],
                        default="AZURE",
                        max_length=6,
                    ),
                ),
                ("credentials", models.TextField()),
                ("container_name", models.CharField(max_length=100)),
                ("default", models.BooleanField(default=False)),
            ],
        ),
    ]

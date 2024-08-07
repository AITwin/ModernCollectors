# Generated by Django 5.0.8 on 2024-08-07 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Source",
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
                ("name", models.CharField(max_length=100)),
                (
                    "periodicity",
                    models.CharField(
                        choices=[
                            ("S", "Secondly"),
                            ("T", "Minutely"),
                            ("H", "Hourly"),
                            ("D", "Daily"),
                            ("W", "Weekly"),
                            ("M", "Monthly"),
                            ("Y", "Yearly"),
                        ],
                        default="T",
                        max_length=1,
                    ),
                ),
                (
                    "periodicity_value",
                    models.IntegerField(
                        default=1,
                        help_text="Value of periodicity, for example 5 for every 5 minutes in case of minutely periodicity",
                    ),
                ),
                (
                    "method",
                    models.CharField(
                        choices=[
                            ("GET", "GET"),
                            ("POST", "POST"),
                            ("PUT", "PUT"),
                            ("PATCH", "PATCH"),
                            ("DELETE", "DELETE"),
                        ],
                        default="GET",
                        max_length=6,
                    ),
                ),
                ("url", models.URLField(blank=True, null=True)),
                ("headers", models.JSONField(blank=True, null=True)),
                ("query_params", models.JSONField(blank=True, null=True)),
                ("body", models.JSONField(blank=True, null=True)),
            ],
        ),
    ]

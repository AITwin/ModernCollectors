# Generated by Django 5.0.8 on 2024-08-07 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("collectors", "0015_storage"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Storage",
            new_name="StorageInstance",
        ),
    ]

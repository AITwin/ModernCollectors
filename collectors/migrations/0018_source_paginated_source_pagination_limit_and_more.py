# Generated by Django 5.0.8 on 2024-08-07 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("collectors", "0017_source_extension"),
    ]

    operations = [
        migrations.AddField(
            model_name="source",
            name="paginated",
            field=models.BooleanField(
                default=False,
                help_text="Is the data paginated, if so, the pagination fields must be filled",
            ),
        ),
        migrations.AddField(
            model_name="source",
            name="pagination_limit",
            field=models.IntegerField(
                default=100, help_text="Limit of records per page"
            ),
        ),
        migrations.AddField(
            model_name="source",
            name="pagination_offset_key",
            field=models.CharField(
                blank=True,
                help_text="Key to get the offset of the next page",
                max_length=100,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="source",
            name="pagination_result_key",
            field=models.CharField(
                blank=True,
                help_text="Key to get the list of records",
                max_length=100,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="source",
            name="pagination_total_count",
            field=models.CharField(
                blank=True,
                help_text="Key to get the total count of records",
                max_length=100,
                null=True,
            ),
        ),
    ]

from django.core.exceptions import ValidationError
from django.db import models


def validate_package_list(value):
    if not isinstance(value, list):
        raise ValidationError("Packages must be a list")

    for package in value:
        if not isinstance(package, str):
            raise ValidationError("Each package must be a string")

    # Prevent code injection, only allow package names
    for package in value:
        if not package.isidentifier():
            raise ValidationError(
                "Invalid package name, are you trying to inject code?"
            )


def validate_storage_slug(value):
    if not value.isidentifier():
        raise ValidationError("Invalid storage slug, must be a valid identifier")

    # Check all lowercase and alpha
    if not value.islower():
        raise ValidationError("Invalid storage slug, must be all lowercase")

    if not value.replace("-", "").isalpha():
        raise ValidationError(
            "Invalid storage slug, must be all alphabetic characters and hyphens"
        )


class SourceGroup(models.Model):
    """
    Model representing a group of sources.
    """

    name = models.CharField(max_length=100, help_text="Name of the group")

    storage_slug = models.CharField(
        max_length=100,
        help_text="Slug of the storage to prefix the data with (format: lowercase, hyphens)",
    )

    def __str__(self):
        return self.name + " /" + self.storage_slug


class SourceHeaders(models.Model):
    name = models.CharField(max_length=100, help_text="Name of the header")

    headers = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name


class Source(models.Model):
    """
    Model representing a source of data for the collector system.
    """

    group = models.ForeignKey(
        "SourceGroup",
        help_text="Group of the source",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
    )

    name = models.CharField(max_length=100, help_text="Name of the source")

    storage_slug = models.CharField(
        max_length=100,
        help_text="Slug of the storage to prefix the data with (format: lowercase, hyphens)",
    )

    enabled = models.BooleanField(default=True)

    class Periodicity(models.TextChoices):
        SECONDLY = "S", "Secondly"
        MINUTELY = "T", "Minutely"
        HOURLY = "H", "Hourly"
        DAILY = "D", "Daily"
        WEEKLY = "W", "Weekly"
        MONTHLY = "M", "Monthly"
        YEARLY = "Y", "Yearly"

    interval_schedule = models.ForeignKey(
        "django_celery_beat.IntervalSchedule",
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        help_text="Celery interval schedule",
    )

    task = models.ForeignKey(
        "django_celery_beat.PeriodicTask",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Celery periodic task",
    )

    class Method(models.TextChoices):
        GET = "GET", "GET"
        POST = "POST", "POST"
        PUT = "PUT", "PUT"
        PATCH = "PATCH", "PATCH"
        DELETE = "DELETE", "DELETE"

    method = models.CharField(
        max_length=6,
        choices=Method.choices,
        default=Method.GET,
    )

    url = models.URLField(max_length=512)

    extension = models.CharField(
        max_length=100,
        help_text="File extension to save the data with (json, csv, etc.)",
        default="json",
    )

    access_key = models.ForeignKey(
        "AccessKey",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Access key for the source if required it will be injected either in headers or query params",
    )

    source_headers = models.ForeignKey(
        "SourceHeaders",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Headers to send with the request",
    )

    query_params = models.JSONField(blank=True, null=True)

    body = models.JSONField(blank=True, null=True)

    paginated = models.BooleanField(
        default=False,
        help_text="Is the data paginated, if so, the pagination fields must be filled",
    )

    pagination_limit = models.IntegerField(
        default=100,
        help_text="Limit of records per page",
    )

    pagination_total_count = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Key to get the total count of records",
    )
    pagination_offset_key = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Key to get the offset of the next page",
    )
    pagination_result_key = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Key to get the list of records",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["storage_slug", "group"], name="unique_name_group"
            ),
        ]


class AccessKey(models.Model):
    """
    Model representing an access key for a source.
    """

    name = models.CharField(
        max_length=100, help_text="Name of the access key", unique=True
    )
    key = models.CharField(max_length=100, help_text="Key name")
    value = models.CharField(max_length=100, help_text="Key value")

    def __str__(self):
        return f"{self.name} [{self.key}]"


class StorageInstance(models.Model):
    """
    Model representing a cloud storage provider
    """

    class Provider(models.TextChoices):
        AZURE = "AZURE", "Azure"
        GOOGLE = "GOOGLE", "Google"

    provider = models.CharField(
        max_length=6,
        choices=Provider.choices,
        default=Provider.AZURE,
    )

    credentials = models.TextField()

    container_name = models.CharField(max_length=100)

    default = models.BooleanField(default=False)

    def __str__(self):
        return self.provider + " /" + self.container_name

    def save(self, *args, **kwargs):
        if self.default:
            StorageInstance.objects.exclude(pk=self.pk).update(default=False)
        super().save(*args, **kwargs)

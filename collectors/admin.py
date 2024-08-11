import unfold.admin
from django.contrib import admin
from django_celery_beat.models import (
    PeriodicTask,
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
)

from collectors.models import (
    Source,
    AccessKey,
    SourceGroup,
    StorageInstance,
    SourceHeaders,
)

# Unregister all django beat admin models
admin.site.unregister(
    [PeriodicTask, IntervalSchedule, CrontabSchedule, SolarSchedule, ClockedSchedule]
)


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(unfold.admin.ModelAdmin):
    list_display = ("name", "task", "enabled", "last_run_at", "total_run_count")

    search_fields = ("name", "task")


@admin.register(SourceGroup)
class SourceGroupAdmin(unfold.admin.ModelAdmin):
    list_display = ("name",)

    search_fields = ("name",)


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(unfold.admin.ModelAdmin):
    list_display = ("every", "period")

    search_fields = ("every", "period")


@admin.register(SourceHeaders)
class SourceHeadersAdmin(unfold.admin.ModelAdmin):
    list_display = ("name",)

    search_fields = ("name",)


@admin.register(Source)
class SourceAdmin(unfold.admin.ModelAdmin):
    list_display = ("group", "name", "interval_schedule", "enabled")

    list_filter = ("group", "enabled")

    list_editable = ("enabled",)

    autocomplete_fields = ("access_key", "group", "interval_schedule", "source_headers")

    readonly_fields = ("task",)


@admin.register(AccessKey)
class AccessKeyAdmin(unfold.admin.ModelAdmin):
    list_display = ("name","key",)

    search_fields = ("name", "key",)


@admin.register(StorageInstance)
class StorageInstanceAdmin(unfold.admin.ModelAdmin):
    list_display = ("provider", "container_name", "default")

    list_filter = ("provider", "default")

    list_editable = ("default",)

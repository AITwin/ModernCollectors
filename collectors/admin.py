from datetime import datetime, timedelta

import unfold.admin
from django.contrib import admin
from django_celery_beat.models import (
    PeriodicTask,
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
)
from django_celery_results.models import TaskResult
from unfold.decorators import display, action

from collectors.models import (
    Source,
    AccessKey,
    SourceGroup,
    StorageInstance,
    SourceHeaders,
)
from collectors.tasks import collect

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
    list_display = (
        "group",
        "name",
        "interval_schedule",
        "is_sane",
        "success_count_in_past_7_days",
        "error_count_in_past_7_days",
        "enabled",
    )

    actions = ["run_now"]

    list_filter = ("group", "enabled")

    list_editable = ("enabled",)

    autocomplete_fields = ("access_key", "group", "interval_schedule", "source_headers")

    readonly_fields = ("task",)

    @action(description="Run now")
    def run_now(self, request, queryset):
        for source in queryset:
            collect.delay(source.id)

        self.message_user(request, f"{len(queryset)} sources have been scheduled to run now.")

        return None

    @display(description="Error (7d)")
    def error_count_in_past_7_days(self, obj):
        if obj.task is None:
            return 0
        return TaskResult.objects.filter(
            periodic_task_name=obj.task.name,
            status="FAILURE",
            date_done__gte=datetime.now() - timedelta(days=7),
        ).count()

    @display(description="Success (7d)")
    def success_count_in_past_7_days(self, obj):
        if obj.task is None:
            return 0
        return TaskResult.objects.filter(
            periodic_task_name=obj.task.name,
            status="SUCCESS",
            date_done__gte=datetime.now() - timedelta(days=7),
        ).count()

    @display(description="Is sane", boolean=True)
    def is_sane(self, obj):
        if obj.task is None:
            return False
        return not TaskResult.objects.filter(
            periodic_task_name=obj.task.name,
            status="FAILURE",
            date_done__gte=datetime.now() - timedelta(days=7),
        ).exists()


@admin.register(AccessKey)
class AccessKeyAdmin(unfold.admin.ModelAdmin):
    list_display = (
        "name",
        "key",
    )

    search_fields = (
        "name",
        "key",
    )


@admin.register(StorageInstance)
class StorageInstanceAdmin(unfold.admin.ModelAdmin):
    list_display = ("provider", "container_name", "default")

    list_filter = ("provider", "default")

    list_editable = ("default",)

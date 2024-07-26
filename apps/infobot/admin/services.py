from django.contrib import admin

from apps.infobot.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_at", "updated_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

from django.contrib import admin

from apps.infobot.models import Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "created_at")
    search_fields = ("name", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

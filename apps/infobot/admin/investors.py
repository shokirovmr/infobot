from django.contrib import admin

from apps.infobot.models import Investor


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

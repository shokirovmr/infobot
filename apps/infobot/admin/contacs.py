from django.contrib import admin

from apps.infobot.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "phone",
        "message",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")
    search_fields = ("name", "email", "phone", "message")
    list_per_page = 20
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

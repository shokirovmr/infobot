from django.contrib import admin

from apps.infobot.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "created_at", "updated_at")
    search_fields = ("title", "description")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

from django.contrib import admin

from apps.infobot.models import FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "answer", "created_at")
    search_fields = ("question", "answer")
    list_per_page = 20
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

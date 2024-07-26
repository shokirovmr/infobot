from django.contrib import admin

from apps.infobot.models import CompanyInfo


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "address", "created_at", "phone")
    search_fields = ("name", "phone")
    list_per_page = 20
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

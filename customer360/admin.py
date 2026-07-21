from django.contrib import admin
from .models import Communication


@admin.register(Communication)
class CommunicationAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "email",
        "phone",
        "channel",
        "direction",
        "created_at",
    )

    search_fields = (
        "customer_name",
        "email",
        "phone",
    )

    list_filter = (
        "channel",
        "direction",
        "created_at",
    )

    ordering = ("-created_at",)
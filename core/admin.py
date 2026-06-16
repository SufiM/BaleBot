from django.contrib import admin
from .models import PlatformUser, BotInteraction, CommandStat
from datetime import timedelta
from django.utils import timezone


admin.site.site_header = "Bale Bot Admin"
admin.site.site_title = "Bale Admin"
admin.site.index_title = "Dashboard"


class ActiveLast24hFilter(admin.SimpleListFilter):
    title = "active in last 24h"
    parameter_name = "active_24h"

    def lookups(self, request, model_admin):
        return (("yes", "Yes"), ("no", "No"))

    def queryset(self, request, queryset):
        cutoff = timezone.now() - timedelta(hours=24)
        if self.value() == "yes":
            return queryset.filter(last_seen__gte=cutoff)
        if self.value() == "no":
            return queryset.filter(last_seen__lt=cutoff)
        return queryset


@admin.register(PlatformUser)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "bale_user_id",
        "username",
        "first_seen",
        "last_seen",
        "is_active_24h",
    )

    search_fields = (
        "bale_user_id",
        "username",
    )

    list_filter = (ActiveLast24hFilter, "first_seen", "last_seen")
    ordering = ("-last_seen",)

    def is_active_24h(self, obj):
        return obj.last_seen >= timezone.now() - timedelta(hours=24)

    is_active_24h.boolean = True
    is_active_24h.short_description = "Active in last 24h"




@admin.register(BotInteraction)
class InteractionAdmin(admin.ModelAdmin):

    list_display = (
        "bot_name",
        "user",
        "command",
        "created_at",
    )

    list_filter = (
        "bot_name",
        "command",
    )


@admin.register(CommandStat)
class CommandStatAdmin(admin.ModelAdmin):

    list_display = (
        "bot_name",
        "command",
        "count",
    )

    ordering = ("-count",)
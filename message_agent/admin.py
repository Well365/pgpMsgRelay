from django.contrib import admin
from .models import PGPMessage

@admin.register(PGPMessage)
class PGPMessageAdmin(admin.ModelAdmin):
    list_display = ('short_id', 'created_at', 'expiry_minutes', 'one_time_view', 'has_been_viewed')
    search_fields = ('short_id', 'note')
    list_filter = ('created_at', 'expiry_minutes', 'one_time_view', 'has_been_viewed')
    readonly_fields = ('short_id', 'created_at')

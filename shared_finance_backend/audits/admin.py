from django.contrib import admin
from .models import AuditLog, Consent


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'content_object', 'timestamp', 'ip_address')
    list_filter = ('action', 'timestamp', 'content_type')
    search_fields = ('user__username', 'action', 'ip_address')
    readonly_fields = ('timestamp', 'old_values', 'new_values', 'metadata')
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        return False  # Audit logs should only be created by signals


@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = ('user', 'purpose', 'audience', 'is_active', 'expires_at', 'created_at')
    list_filter = ('purpose', 'audience', 'is_active', 'created_at')
    search_fields = ('user__username', 'consent_token')
    readonly_fields = ('consent_token', 'created_at')
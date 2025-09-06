from django.contrib import admin
from .models import LedgerEntry, Payment


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = ('from_member', 'to_member', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('from_member__username', 'to_member__username', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ledger_entry', 'method', 'amount', 'status', 'created_at')
    list_filter = ('method', 'status', 'created_at')
    search_fields = ('payment_ref', 'ledger_entry__from_member__username')
    readonly_fields = ('created_at', 'updated_at')
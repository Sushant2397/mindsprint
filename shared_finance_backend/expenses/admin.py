from django.contrib import admin
from .models import Expense, ExpenseSplit


class ExpenseSplitInline(admin.TabularInline):
    model = ExpenseSplit
    extra = 0


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'payer', 'total_amount', 'group', 'category', 'date', 'is_settled')
    list_filter = ('category', 'is_settled', 'date', 'group__name')
    search_fields = ('vendor', 'description', 'payer__username', 'group__name')
    readonly_fields = ('created_at', 'updated_at', 'total_amount')
    inlines = [ExpenseSplitInline]
    date_hierarchy = 'date'


@admin.register(ExpenseSplit)
class ExpenseSplitAdmin(admin.ModelAdmin):
    list_display = ('expense', 'member', 'amount_owed', 'split_type', 'is_paid')
    list_filter = ('split_type', 'is_paid', 'created_at')
    search_fields = ('expense__vendor', 'member__username')
    readonly_fields = ('created_at',)
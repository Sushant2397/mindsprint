from django.contrib import admin
from .models import Group, GroupMember, FairnessPolicy


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_type', 'owner', 'currency', 'is_active', 'created_at')
    list_filter = ('group_type', 'is_active', 'currency', 'created_at')
    search_fields = ('name', 'description', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'group', 'role', 'share_factor', 'is_active', 'joined_at')
    list_filter = ('role', 'is_active', 'income_bracket', 'joined_at')
    search_fields = ('user__username', 'group__name')
    readonly_fields = ('joined_at',)


@admin.register(FairnessPolicy)
class FairnessPolicyAdmin(admin.ModelAdmin):
    list_display = ('group', 'policy_type', 'is_active', 'created_at', 'created_by')
    list_filter = ('policy_type', 'is_active', 'created_at')
    search_fields = ('group__name', 'created_by__username')
    readonly_fields = ('created_at',)
from rest_framework import serializers
from .models import Group, GroupMember, FairnessPolicy
from users.serializers import UserSerializer


class GroupMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = GroupMember
        fields = ['id', 'user', 'user_id', 'role', 'share_factor', 'income_bracket', 
                 'joined_at', 'is_active']
        read_only_fields = ['id', 'joined_at']


class GroupSerializer(serializers.ModelSerializer):
    members = GroupMemberSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    owner_id = serializers.IntegerField(write_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'group_type', 'owner', 'owner_id',
                 'settings', 'currency', 'billing_cycle', 'gst_mode', 'is_active',
                 'created_at', 'updated_at', 'members', 'member_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'member_count']
    
    def get_member_count(self, obj):
        return obj.members.filter(is_active=True).count()


class FairnessPolicySerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = FairnessPolicy
        fields = ['id', 'group', 'policy_type', 'parameters', 'is_active',
                 'created_at', 'created_by']
        read_only_fields = ['id', 'created_at']


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'description', 'group_type', 'settings', 'currency',
                 'billing_cycle', 'gst_mode']
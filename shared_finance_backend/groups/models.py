from django.db import models
from django.contrib.auth import get_user_model
import json

User = get_user_model()


class Group(models.Model):
    """Group model for expense sharing groups"""
    
    GROUP_TYPES = [
        ('roommates', 'Roommates'),
        ('society', 'Society Committee'),
        ('club', 'Club/Organization'),
        ('family', 'Family'),
        ('friends', 'Friends'),
        ('business', 'Business'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    group_type = models.CharField(max_length=20, choices=GROUP_TYPES, default='other')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups')
    settings = models.JSONField(default=dict, blank=True)
    currency = models.CharField(max_length=3, default='INR')
    billing_cycle = models.CharField(max_length=20, default='monthly')
    gst_mode = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.group_type})"
    
    class Meta:
        db_table = 'groups_group'


class GroupMember(models.Model):
    """Group membership model"""
    
    ROLES = [
        ('owner', 'Owner'),
        ('treasurer', 'Treasurer'),
        ('auditor', 'Auditor'),
        ('member', 'Member'),
    ]
    
    INCOME_BRACKETS = [
        ('low', 'Low Income'),
        ('medium', 'Medium Income'),
        ('high', 'High Income'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    role = models.CharField(max_length=20, choices=ROLES, default='member')
    share_factor = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    income_bracket = models.CharField(max_length=20, choices=INCOME_BRACKETS, default='medium')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.user.username} in {self.group.name} ({self.role})"
    
    class Meta:
        db_table = 'groups_groupmember'
        unique_together = ['group', 'user']


class FairnessPolicy(models.Model):
    """Fairness policy for settlement calculations"""
    
    POLICY_TYPES = [
        ('equal_split', 'Equal Split'),
        ('income_based', 'Income Based'),
        ('custom_share', 'Custom Share'),
        ('proportional', 'Proportional to Expenses'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='fairness_policies')
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES)
    parameters = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.group.name} - {self.policy_type}"
    
    class Meta:
        db_table = 'groups_fairnesspolicy'
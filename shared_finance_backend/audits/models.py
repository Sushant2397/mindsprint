from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class AuditLog(models.Model):
    """Immutable audit log for tracking all changes"""
    
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('payment_initiated', 'Payment Initiated'),
        ('payment_completed', 'Payment Completed'),
        ('settlement_computed', 'Settlement Computed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=30, choices=ACTION_CHOICES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    old_values = models.JSONField(default=dict, blank=True)
    new_values = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.action} by {self.user} at {self.timestamp}"
    
    class Meta:
        db_table = 'audits_auditlog'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['content_type', 'object_id']),
        ]


class Consent(models.Model):
    """Consent model for data sharing (Account Aggregator simulation)"""
    
    PURPOSES = [
        ('expense_analysis', 'Expense Analysis'),
        ('settlement_calculation', 'Settlement Calculation'),
        ('group_insights', 'Group Insights'),
        ('payment_processing', 'Payment Processing'),
    ]
    
    AUDIENCES = [
        ('group_members', 'Group Members'),
        ('group_owner', 'Group Owner'),
        ('system', 'System'),
        ('third_party', 'Third Party'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consents')
    purpose = models.CharField(max_length=30, choices=PURPOSES)
    audience = models.CharField(max_length=20, choices=AUDIENCES)
    scope = models.JSONField(default=dict, blank=True)
    consent_token = models.CharField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Consent for {self.purpose} by {self.user.username}"
    
    class Meta:
        db_table = 'audits_consent'
        ordering = ['-created_at']
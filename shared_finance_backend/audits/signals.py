from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import AuditLog
from groups.models import Group, GroupMember, FairnessPolicy
from expenses.models import Expense, ExpenseSplit
from payments.models import LedgerEntry, Payment

User = get_user_model()


def create_audit_log(instance, action, user=None, old_values=None, new_values=None, request=None):
    """Helper function to create audit log entries"""
    if request:
        ip_address = getattr(request, 'META', {}).get('REMOTE_ADDR')
        user_agent = getattr(request, 'META', {}).get('HTTP_USER_AGENT', '')
    else:
        ip_address = None
        user_agent = ''
    
    AuditLog.objects.create(
        user=user,
        action=action,
        content_object=instance,
        old_values=old_values or {},
        new_values=new_values or {},
        ip_address=ip_address,
        user_agent=user_agent
    )


# Group signals
@receiver(post_save, sender=Group)
def group_audit(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    create_audit_log(instance, action, user=instance.owner)


@receiver(post_delete, sender=Group)
def group_delete_audit(sender, instance, **kwargs):
    create_audit_log(instance, 'delete', user=instance.owner)


# GroupMember signals
@receiver(post_save, sender=GroupMember)
def group_member_audit(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    create_audit_log(instance, action, user=instance.user)


@receiver(post_delete, sender=GroupMember)
def group_member_delete_audit(sender, instance, **kwargs):
    create_audit_log(instance, 'delete', user=instance.user)


# Expense signals
@receiver(post_save, sender=Expense)
def expense_audit(sender, instance, created, **kwargs):
    action = 'create' if created else 'update'
    create_audit_log(instance, action, user=instance.payer)


@receiver(post_delete, sender=Expense)
def expense_delete_audit(sender, instance, **kwargs):
    create_audit_log(instance, 'delete', user=instance.payer)


# Payment signals
@receiver(post_save, sender=Payment)
def payment_audit(sender, instance, created, **kwargs):
    action = 'payment_initiated' if created else 'payment_completed' if instance.status == 'completed' else 'update'
    create_audit_log(instance, action, user=instance.ledger_entry.from_member)
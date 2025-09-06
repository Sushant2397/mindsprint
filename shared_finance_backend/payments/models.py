from django.db import models
from django.contrib.auth import get_user_model
from expenses.models import Expense

User = get_user_model()


class LedgerEntry(models.Model):
    """Ledger entry for tracking debts between users"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('disputed', 'Disputed'),
    ]
    
    from_member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='debts')
    to_member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='credits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ref_expense = models.ForeignKey(Expense, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.from_member.username} owes {self.to_member.username} ₹{self.amount}"
    
    class Meta:
        db_table = 'payments_ledgerentry'
        ordering = ['-created_at']


class Payment(models.Model):
    """Payment model for tracking actual payments"""
    
    PAYMENT_METHODS = [
        ('UPI_DEEPLINK', 'UPI Deep Link'),
        ('UPI_AUTOPAY', 'UPI Auto Pay'),
        ('MANUAL', 'Manual Transfer'),
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    ledger_entry = models.ForeignKey(LedgerEntry, on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_ref = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    upi_deeplink = models.URLField(blank=True, null=True)
    webhook_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment of ₹{self.amount} via {self.method} - {self.status}"
    
    class Meta:
        db_table = 'payments_payment'
        ordering = ['-created_at']
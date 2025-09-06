from django.db import models
from django.contrib.auth import get_user_model
from groups.models import Group

User = get_user_model()


class Expense(models.Model):
    """Expense model for tracking shared expenses"""
    
    CATEGORIES = [
        ('food', 'Food & Dining'),
        ('transport', 'Transportation'),
        ('utilities', 'Utilities'),
        ('rent', 'Rent & Accommodation'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('travel', 'Travel'),
        ('other', 'Other'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_expenses')
    amount_subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    amount_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vendor = models.CharField(max_length=200, blank=True)
    gstin = models.CharField(max_length=15, blank=True)
    invoice_no = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default='other')
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    receipt_file = models.FileField(upload_to='receipts/', blank=True, null=True)
    ocr_data = models.JSONField(default=dict, blank=True)
    is_settled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def total_amount(self):
        return self.amount_subtotal + self.amount_tax
    
    def __str__(self):
        return f"{self.vendor or 'Expense'} - ₹{self.total_amount} ({self.group.name})"
    
    class Meta:
        db_table = 'expenses_expense'
        ordering = ['-date']


class ExpenseSplit(models.Model):
    """Expense split model for dividing expenses among group members"""
    
    SPLIT_TYPES = [
        ('equal', 'Equal Split'),
        ('percentage', 'Percentage'),
        ('amount', 'Fixed Amount'),
        ('share_factor', 'Share Factor'),
    ]
    
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='splits')
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_splits')
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2)
    split_type = models.CharField(max_length=20, choices=SPLIT_TYPES, default='equal')
    metadata = models.JSONField(default=dict, blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.member.username} owes ₹{self.amount_owed} for {self.expense}"
    
    class Meta:
        db_table = 'expenses_expensesplit'
        unique_together = ['expense', 'member']
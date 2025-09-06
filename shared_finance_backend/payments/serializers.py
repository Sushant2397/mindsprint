from rest_framework import serializers
from .models import LedgerEntry, Payment
from users.serializers import UserSerializer
from expenses.serializers import ExpenseSerializer


class LedgerEntrySerializer(serializers.ModelSerializer):
    from_member = UserSerializer(read_only=True)
    to_member = UserSerializer(read_only=True)
    ref_expense = ExpenseSerializer(read_only=True)
    
    class Meta:
        model = LedgerEntry
        fields = ['id', 'from_member', 'to_member', 'amount', 'status',
                 'ref_expense', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    ledger_entry = LedgerEntrySerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'ledger_entry', 'method', 'payment_ref', 'status',
                 'amount', 'upi_deeplink', 'webhook_data', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'webhook_data']


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['ledger_entry', 'method', 'amount']
    
    def create(self, validated_data):
        # Set status to pending by default
        validated_data['status'] = 'pending'
        return super().create(validated_data)